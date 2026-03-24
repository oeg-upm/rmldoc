(function(){
  const toc = document.getElementById("tmToc");
  const btn = document.getElementById("tmTocToggle");
  const links = Array.from(document.querySelectorAll("#tmTocList a"));

  function setCollapsed(collapsed){
    if (!toc || !btn) return;
    toc.classList.toggle("is-collapsed", collapsed);
    btn.textContent = collapsed ? "Expand" : "Collapse";
    btn.setAttribute("aria-expanded", collapsed ? "false" : "true");
    try { localStorage.setItem("tmTocCollapsed", collapsed ? "1" : "0"); } catch(e) {}
  }

  if (toc && btn){
    let saved = null;
    try { saved = localStorage.getItem("tmTocCollapsed"); } catch(e) {}
    if (saved === "1") setCollapsed(true);
    btn.addEventListener("click", () => setCollapsed(!toc.classList.contains("is-collapsed")));
  }

  const targets = links
    .map(a => document.getElementById(a.getAttribute("href").slice(1)))
    .filter(Boolean);

  if (!targets.length) return;

  const idToLink = new Map(links.map(a => [a.getAttribute("href").slice(1), a]));

  function setActive(id){
    links.forEach(a => a.classList.remove("is-active"));
    const a = idToLink.get(id);
    if (a) a.classList.add("is-active");
  }

  const obs = new IntersectionObserver((entries) => {
    const visible = entries
      .filter(e => e.isIntersecting)
      .sort((a,b) => (b.intersectionRatio || 0) - (a.intersectionRatio || 0))[0];
    if (visible?.target?.id) setActive(visible.target.id);
  }, {
    root: null,
    threshold: [0.15, 0.35, 0.55],
    rootMargin: "-15% 0px -70% 0px"
  });

  targets.forEach(t => obs.observe(t));

  if (location.hash) setActive(location.hash.slice(1));
  else setActive(targets[0].id);
})();

(function() {
  const payload = window.__RML_PAYLOAD__;
  const maps = payload.maps;
  const containers = payload.containers;
  const instances = [];
  const GTFS_BASE = "{{ gtfs_terms_base }}";

  function formatLabel(text, maxLen = 35) {
    if (!text || text.length <= maxLen) return text;
    const words = String(text).split(/([/-])/);
    let result = '';
    let currentLine = '';
    words.forEach(word => {
      if ((currentLine + word).length > maxLen) {
        result += currentLine + '\n';
        currentLine = word;
      } else {
        currentLine += word;
      }
    });
    return result + currentLine;
  }

  function gtfsHrefIfType(pred, objRaw) {
    if (pred !== 'a') return null;
    const m = /^gtfs:([A-Za-z0-9_]+)$/.exec(String(objRaw || '').trim());
    if (!m) return null;
    return GTFS_BASE + m[1];
  }

  function buildElements(m) {
    const elements = [];
    const subjHref = m.subject_linkable ? (m.subject_href || null) : null;

    elements.push({
      data: {
        id: 's',
        label: formatLabel(m.subject, 50),
        full: String(m.subject_raw || m.subject || ''),
        href: subjHref,
        isLink: subjHref ? 1 : 0
      }
    });

    (m.predicates || []).forEach((item, i) => {
      const objFull = String(item.o_raw || item.o_display || '');
      const objLabel = String(item.o_base || item.o_display || objFull);

      let href = null;
      if (item.o_linkable && item.o_href) href = item.o_href;
      else href = gtfsHrefIfType(String(item.p || ''), objLabel) || null;

      elements.push({
        data: {
          id: 'o' + i,
          label: formatLabel(objLabel, 28),
          full: objFull,
          href: href,
          isLink: href ? 1 : 0
        }
      });

      elements.push({
        data: { source: 's', target: 'o' + i, label: String(item.p || '') }
      });
    });

    return elements;
  }

  function computeDiagramHeight(nPredicates) {
    const topPad = 90;
    const bottomPad = 60;
    const perRow = 90;
    const minH = 360;
    const maxH = 1200;
    const h = topPad + bottomPad + Math.max(1, nPredicates) * perRow;
    return Math.max(minH, Math.min(maxH, h));
  }

  function makeLayout(nPredicates, heightPx) {
    const leftX = 120;
    const rightX = 680;
    const topY = 110;
    const bottomY = Math.max(topY + 120, heightPx - 90);
    const count = Math.max(1, nPredicates);
    const step = (bottomY - topY) / (count - 1 || 1);
    const subjectY = (topY + bottomY) / 2;

    return {
      name: 'grid',
      cols: 2,
      transform: (node) => {
        if (node.id() === 's') return { x: leftX, y: subjectY };
        if (count === 1) return { x: rightX, y: subjectY };
        const idx = parseInt(node.id().replace('o',''), 10);
        return { x: rightX, y: topY + (idx * step) };
      }
    };
  }

  const cyStyle = [
    { selector: 'node', style: {
      'shape': 'round-rectangle',
      'background-color': '#fff4dd',
      'border-width': 1,
      'border-color': '#e0d5ba',
      'label': 'data(label)',
      'text-valign': 'center',
      'text-halign': 'center',
      'text-wrap': 'wrap',
      'font-family': 'monospace',
      'font-size': '12px',
      'width': 'label',
      'height': 'label',
      'padding': '15px'
    }},
    { selector: 'edge', style: {
      'width': 1,
      'line-color': '#333',
      'target-arrow-shape': 'triangle',
      'curve-style': 'straight',
      'label': 'data(label)',
      'font-size': '10px',
      'text-background-color': '#e2d1f9',
      'text-background-opacity': 1,
      'text-background-padding': '3px',
      'edge-text-rotation': 'none'
    }},
    { selector: 'node[isLink = 1]', style: {
      'border-color': '#b99cff',
      'background-color': '#fff',
      'border-width': 2,
      'cursor': 'pointer'
    }}
  ];

  function attachTooltip(cy) {
    const container = cy.container();
    const viz = container.closest('.viz-container');
    if (!viz) return;

    let tip = viz.querySelector('.cy-tooltip');
    if (!tip) {
      tip = document.createElement('div');
      tip.className = 'cy-tooltip';
      viz.appendChild(tip);
    }

    function showTip(text, x, y) {
      tip.textContent = text;
      tip.style.display = 'block';
      tip.style.left = (x + 12) + 'px';
      tip.style.top  = (y + 12) + 'px';
    }

    function hideTip() {
      tip.style.display = 'none';
      tip.textContent = '';
    }

    const MIN_LEN = 40;

    cy.on('mouseover', 'node', (evt) => {
      const n = evt.target;
      const full = (n.data('full') || '').toString();
      if (!full || full.length < MIN_LEN) return;
      const rp = n.renderedPosition();
      showTip(full, rp.x, rp.y);
    });

    cy.on('mouseout', 'node', hideTip);
    cy.on('drag', 'node', hideTip);
    cy.on('zoom pan', hideTip);
  }

  function initAll() {
    Object.keys(containers).forEach((tmId) => {
      const cyDivId = containers[tmId];
      const el = document.getElementById(cyDivId);
      const m = maps[tmId];
      if (!el || !m) return;

      // ---------------------------------------------------------
      // 1. GRAFO PRINCIPAL (SPO - RDF TRIPLES)
      // ---------------------------------------------------------
      const viz = el.closest('.viz-container');
      const n = (m.predicates || []).length;

      const neededH = computeDiagramHeight(n);
      if (viz) viz.style.height = neededH + "px";

      const cy = cytoscape({
        container: el,
        elements: buildElements(m),
        style: cyStyle, // Usamos tu estilo por defecto
        layout: makeLayout(n, neededH)
      });

      cy.on('tap', 'node[isLink = 1]', (evt) => {
        const href = evt.target.data('href');
        if (href) window.open(href, '_blank', 'noopener');
      });

      attachTooltip(cy);
      cy.fit(null, 50);

      // Guardamos la instancia indicando que es de tipo 'spo'
      instances.push({ cy: cy, tmId: tmId, type: 'spo' });

// ---------------------------------------------------------
      // 2. GRAFOS DE JOIN CONDITIONS
      // ---------------------------------------------------------
      if (m.joins && m.joins.length > 0) {
        m.joins.forEach((j) => {
          const joinEl = document.getElementById(j.container_id);
          if (!joinEl) return;

          const joinViz = joinEl.closest('.viz-container');

          // USAMOS LA MISMA LÓGICA DE ESPACIO QUE LOS GRAFOS NORMALES
          // Le pasamos '1' porque es una sola relación (un 'edge')
          const joinH = computeDiagramHeight(1);
          if (joinViz) joinViz.style.height = joinH + "px";

          const joinElements = [
            // Cambiamos el 50 por 28, que es la misma medida que usan los objetos del RDF triples
            { data: { id: 's', label: formatLabel(j.s_template, 28), full: j.s_template } },
            { data: { id: 't', label: formatLabel(j.o_template, 28), full: j.o_template } },
            { data: { source: 's', target: 't', label: j.predicate ? j.predicate : `equal(${j.child}, ${j.parent})` } }
          ];

          const joinLayout = {
            name: 'grid',
            rows: 1,
            padding: 50 // Añadimos un poco más de padding para que respire bien
          };

          const joinCy = cytoscape({
            container: joinEl,
            elements: joinElements,
            style: cyStyle,
            layout: joinLayout,
            userZoomingEnabled: false,
            panningEnabled: false
          });

          attachTooltip(joinCy);
          joinCy.fit(null, 50);

          instances.push({ cy: joinCy, type: 'join', layout: joinLayout });
        });
      }
    });
  }

  initAll();

  // ---------------------------------------------------------
  // REDIMENSIONAMIENTO RESPONSIVE
  // ---------------------------------------------------------
  window.addEventListener('resize', function() {
    instances.forEach((entry) => {
      const cy = entry.cy;
      const el = cy.container();
      const viz = el.closest('.viz-container');

      if (entry.type === 'spo') {
        const tmId = entry.tmId;
        const m = maps[tmId];
        const n = (m?.predicates || []).length;

        const neededH = computeDiagramHeight(n);
        if (viz) viz.style.height = neededH + "px";

        cy.resize();
        cy.layout(makeLayout(n, neededH)).run();
        cy.fit(null, 50);

      } else if (entry.type === 'join') {
        // APLICAMOS LA MISMA ADAPTACIÓN DE ESPACIO PARA LOS JOINS AL REDIMENSIONAR
        const joinH = computeDiagramHeight(1);
        if (viz) viz.style.height = joinH + "px";

        cy.resize();
        cy.layout(entry.layout).run();
        cy.fit(null, 50);
      }
    });
  });
})();