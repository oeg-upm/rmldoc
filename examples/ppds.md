# RML Documentation (RMLdoc)

**Version:**

**Authors**:


**Mapping file:**
ppds.rml.ttl

**License**:

[![http://insertlicenseURIhere.org](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International%20(CC%20BY%204.0)-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

------


## **Namespaces used in the document**

| Prefix       |               IRI.                   |
| :----------- | :----------------------------------  |
| fnml     | http://semweb.mmlab.be/ns/fnml# |
| rml     | http://semweb.mmlab.be/ns/rml# |
| legal     | https://www.w3.org/ns/legal# |
| d2rq     | http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1# |
| locn     | http://www.w3.org/ns/locn# |
| schema1     | http://schema.org/ |
| dct     | http://purl.org/dc/terms/ |
| formats     | http://www.w3.org/ns/formats/ |
| grel     | http://users.ugent.be/~bjdmeest/function/grel.ttl# |
| epo     | http://data.europa.eu/a4g/ontology# |
| geo1     | http://www.w3.org/2003/01/geo/wgs84_pos# |
| rr     | http://www.w3.org/ns/r2rml# |
| ql     | http://semweb.mmlab.be/ns/ql# |
| comp     | http://semweb.mmlab.be/ns/rml-compression# |



## Mappings
>[!NOTE]
>1. **Source**: This is where you define the source of your data, which can be a relational database, a CSV file, or any other structured data source. The logical source specifies the location and format of your source data.
>2. **Subject**: This part of the mapping defines how the data from the logical source will be used to create RDF subjects, typically using templates and column mappings.
>3. **Predicate Object**: These describe how the data from the logical source will be used to generate RDF triples, indicating relationships between subjects and objects.
>4. **JoinCondition**: is used to specify the conditions under which two data sources or tables should be joined when creating RDF triples through mappings.


## procedure_technique_usage_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://data.europa.eu/a4g/ontology#usesTechnique | {http://data.europa.eu/a4g/resource/epo/techniqueUsage/codice_{replace(../../../id,"https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/","")}} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:usesTechnique"| object1("{http://data.europa.eu/a4g/resource/epo/techniqueUsage/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}}")
    
``` 
- **joinCondition**:
 ## organization_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/org/organization/{cac:PartyIdentification/cbc:ID[@schemeName="DIR3"]}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | org:Organization |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/org/organization/{cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}"] -->|"a"| object1("org:Organization")
    
``` 
- **joinCondition**:


  Source triple pattern: <organization_0>
  Target triple pattern: <organization_id_0>
  Function: **equal(cac:PartyIdentification/cbc:ID[@schemeName="DIR3"], cac:PartyIdentification/cbc:ID[@schemeName="DIR3"])**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S1["http://data.europa.eu/a4g/resource/org/organization/{cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}"] -->|"epo:hasID"| object1("http://data.europa.eu/a4g/resource/org/identifier/{cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}")

``` 



  Source triple pattern: <organization_0>
  Target triple pattern: <buyer_legal_type_0>
  Function: **equal(cbc:ContractingPartyTypeCode, codice)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S2["http://data.europa.eu/a4g/resource/org/organization/{cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}"] -->|"epo:hasBuyerType"| object2("eu_uri")

``` 



  Source triple pattern: <organization_0>
  Target triple pattern: <locn_address_0>
  Function: **equal(cac:PartyIdentification/cbc:ID[@schemeName="DIR3"], ../cac:PartyIdentification/cbc:ID[@schemeName="DIR3"])**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S3["http://data.europa.eu/a4g/resource/org/organization/{cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}"] -->|"legal:registeredAddress"| object3("http://data.europa.eu/a4g/resource/locn/address/{../cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}")

``` 

 ## lot_adhoc_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:Lot |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0"] -->|"a"| object1("epo:Lot")
    
``` 
- **joinCondition**:
 ## procedure_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:Procedure |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"a"| object1("epo:Procedure")
    
``` 
- **joinCondition**:


  Source triple pattern: <procedure_0>
  Target triple pattern: <lot_0>
  Function: **equal(../../id, ../../id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S1["http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:hasProcurementScopeDividedIntoLot"| object1("http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cbc:ID[@schemeName='ID_LOTE']}")

``` 



  Source triple pattern: <procedure_0>
  Target triple pattern: <procedure_type_0>
  Function: **equal(../cac:ProcurementProject/cbc:TypeCode, codice)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S2["http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:hasProcedureType"| object2("eu_uri")

``` 



  Source triple pattern: <procedure_0>
  Target triple pattern: <framework_agreement_technique_usage_0>
  Function: **equal(../../id, ../../id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S3["http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:usesTechnique"| object3("http://data.europa.eu/a4g/resource/epo/frameworkAgreementTechniqueUsage/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}")

``` 



  Source triple pattern: <procedure_0>
  Target triple pattern: <technique_usage_0>
  Function: **equal(../../id, ../../id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S4["http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:usesTechnique"| object4("http://data.europa.eu/a4g/resource/epo/techniqueUsage/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}")

``` 

 ## framework_agreement_technique_usage_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/frameworkAgreementTechniqueUsage/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:FrameworkAgreementTechniqueUsage |
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:TechniqueUsage |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/frameworkAgreementTechniqueUsage/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"a"| object1("epo:FrameworkAgreementTechniqueUsage")
S["http://data.europa.eu/a4g/resource/epo/frameworkAgreementTechniqueUsage/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"a"| object2("epo:TechniqueUsage")
    
``` 
- **joinCondition**:
 ## buyer_role_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/buyer/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:Buyer |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/buyer/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"a"| object1("epo:Buyer")
    
``` 
- **joinCondition**:


  Source triple pattern: <buyer_role_0>
  Target triple pattern: <organization_0>
  Function: **equal(../id, ../../../id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S1["http://data.europa.eu/a4g/resource/epo/buyer/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:playedBy"| object1("http://data.europa.eu/a4g/resource/org/organization/{cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}")

``` 

 ## country_code_0
- **Source**

```bash
country_code.csv
``` 
- **Subject**
```bash
eu_uri
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
    
``` 
- **joinCondition**:
 ## not_lot_award_outcome_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/lotAwardOutcome/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:LotAwardOutcome |
| http://data.europa.eu/a4g/ontology#hasAwardDecisionDate | {cac:TenderResult/cbc:AwardDate} |
| http://data.europa.eu/a4g/ontology#describesLot | {http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../id,"https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/","")}_0} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/lotAwardOutcome/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0"] -->|"a"| object1("epo:LotAwardOutcome")
S["http://data.europa.eu/a4g/resource/epo/lotAwardOutcome/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0"] -->|"epo:hasAwardDecisionDate"| object2("{cac:TenderResult/cbc:AwardDate}")
S["http://data.europa.eu/a4g/resource/epo/lotAwardOutcome/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0"] -->|"epo:describesLot"| object3("{http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0}")
    
``` 
- **joinCondition**:
 ## technique_usage_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/techniqueUsage/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:TechniqueUsage |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/techniqueUsage/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"a"| object1("epo:TechniqueUsage")
    
``` 
- **joinCondition**:
 ## result_notice_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/resultNotice/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:ResultNotice |
| http://data.europa.eu/a4g/ontology#hasDispatchDate | {cac:TenderingProcess/cac:TenderSubmissionDeadlinePeriod/cbc:EndDate} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/resultNotice/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"a"| object1("epo:ResultNotice")
S["http://data.europa.eu/a4g/resource/epo/resultNotice/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:hasDispatchDate"| object2("{cac:TenderingProcess/cac:TenderSubmissionDeadlinePeriod/cbc:EndDate}")
    
``` 
- **joinCondition**:


  Source triple pattern: <result_notice_0>
  Target triple pattern: <buyer_role_0>
  Function: **equal(../id, ../id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S1["http://data.europa.eu/a4g/resource/epo/resultNotice/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:refersToRole"| object1("http://data.europa.eu/a4g/resource/epo/buyer/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}")

``` 



  Source triple pattern: <result_notice_0>
  Target triple pattern: <procedure_0>
  Function: **equal(../id, ../../id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S2["http://data.europa.eu/a4g/resource/epo/resultNotice/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:refersToProcedure"| object2("http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}")

``` 



  Source triple pattern: <result_notice_0>
  Target triple pattern: <procedure_no_lot_0>
  Function: **equal(../id, ../id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S3["http://data.europa.eu/a4g/resource/epo/resultNotice/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:refersToProcedure"| object3("http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}")

``` 

 ## locn_address_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/locn/address/{../cac:PartyIdentification/cbc:ID[@schemeName="DIR3"]}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | locn:Address |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/locn/address/{../cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}"] -->|"a"| object1("locn:Address")
    
``` 
- **joinCondition**:


  Source triple pattern: <locn_address_0>
  Target triple pattern: <country_code_0>
  Function: **equal(cac:Country/cbc:IdentificationCode, codice)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S1["http://data.europa.eu/a4g/resource/locn/address/{../cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}"] -->|"epo:hasCountryCode"| object1("eu_uri")

``` 

 ## lot_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cbc:ID[@schemeName="ID_LOTE"]}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:Lot |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cbc:ID[@schemeName='ID_LOTE']}"] -->|"a"| object1("epo:Lot")
    
``` 
- **joinCondition**:
 ## not_lot_submission_statistical_information_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/submissionStatisticalInformation/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:SubmissionStatisticalInformation |
| http://data.europa.eu/a4g/ontology#hasReceivedTenders | {cac:TenderResult/cbc:ReceivedTenderQuantity} |
| http://data.europa.eu/a4g/ontology#concernsSubmissionsForLot | {http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../id,"https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/","")}_0} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/submissionStatisticalInformation/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0"] -->|"a"| object1("epo:SubmissionStatisticalInformation")
S["http://data.europa.eu/a4g/resource/epo/submissionStatisticalInformation/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0"] -->|"epo:hasReceivedTenders"| object2("{cac:TenderResult/cbc:ReceivedTenderQuantity}")
S["http://data.europa.eu/a4g/resource/epo/submissionStatisticalInformation/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0"] -->|"epo:concernsSubmissionsForLot"| object3("{http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0}")
    
``` 
- **joinCondition**:
 ## submission_statistical_information_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/submissionStatisticalInformation/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cac:AwardedTenderedProject/cbc:ProcurementProjectLotID}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:SubmissionStatisticalInformation |
| http://data.europa.eu/a4g/ontology#hasReceivedTenders | {cbc:ReceivedTenderQuantity} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/submissionStatisticalInformation/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cac:AwardedTenderedProject/cbc:ProcurementProjectLotID}"] -->|"a"| object1("epo:SubmissionStatisticalInformation")
S["http://data.europa.eu/a4g/resource/epo/submissionStatisticalInformation/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cac:AwardedTenderedProject/cbc:ProcurementProjectLotID}"] -->|"epo:hasReceivedTenders"| object2("{cbc:ReceivedTenderQuantity}")
    
``` 
- **joinCondition**:


  Source triple pattern: <submission_statistical_information_0>
  Target triple pattern: <lot_0>
  Function: **equal(../../id, ../../id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S1["http://data.europa.eu/a4g/resource/epo/submissionStatisticalInformation/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cac:AwardedTenderedProject/cbc:ProcurementProjectLotID}"] -->|"epo:concernsSubmissionsForLot"| object1("http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cbc:ID[@schemeName='ID_LOTE']}")

``` 



  Source triple pattern: <submission_statistical_information_0>
  Target triple pattern: <lot_0>
  Function: **equal(cac:AwardedTenderedProject/cbc:ProcurementProjectLotID, cbc:ID[@schemeName="ID_LOTE"])**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S2["http://data.europa.eu/a4g/resource/epo/submissionStatisticalInformation/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cac:AwardedTenderedProject/cbc:ProcurementProjectLotID}"] -->|"epo:concernsSubmissionsForLot"| object2("http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cbc:ID[@schemeName='ID_LOTE']}")

``` 

 ## procedure_no_lot_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:Procedure |
| http://data.europa.eu/a4g/ontology#hasProcurementScopeDividedIntoLot | {http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../id,"https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/","")}_0} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"a"| object1("epo:Procedure")
S["http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:hasProcurementScopeDividedIntoLot"| object2("{http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_0}")
    
``` 
- **joinCondition**:


  Source triple pattern: <procedure_no_lot_0>
  Target triple pattern: <procedure_type_0>
  Function: **equal(cac:ProcurementProject/cbc:TypeCode, codice)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S1["http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:hasProcedureType"| object1("eu_uri")

``` 

 ## lot_award_outcome_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/lotAwardOutcome/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cac:AwardedTenderedProject/cbc:ProcurementProjectLotID}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:LotAwardOutcome |
| http://data.europa.eu/a4g/ontology#hasAwardDecisionDate | {cbc:AwardDate} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/lotAwardOutcome/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cac:AwardedTenderedProject/cbc:ProcurementProjectLotID}"] -->|"a"| object1("epo:LotAwardOutcome")
S["http://data.europa.eu/a4g/resource/epo/lotAwardOutcome/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cac:AwardedTenderedProject/cbc:ProcurementProjectLotID}"] -->|"epo:hasAwardDecisionDate"| object2("{cbc:AwardDate}")
    
``` 
- **joinCondition**:


  Source triple pattern: <lot_award_outcome_0>
  Target triple pattern: <lot_0>
  Function: **equal(../../id, ../../id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S1["http://data.europa.eu/a4g/resource/epo/lotAwardOutcome/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cac:AwardedTenderedProject/cbc:ProcurementProjectLotID}"] -->|"epo:describesLot"| object1("http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cbc:ID[@schemeName='ID_LOTE']}")

``` 



  Source triple pattern: <lot_award_outcome_0>
  Target triple pattern: <lot_0>
  Function: **equal(cac:AwardedTenderedProject/cbc:ProcurementProjectLotID, cbc:ID[@schemeName="ID_LOTE"])**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S2["http://data.europa.eu/a4g/resource/epo/lotAwardOutcome/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cac:AwardedTenderedProject/cbc:ProcurementProjectLotID}"] -->|"epo:describesLot"| object2("http://data.europa.eu/a4g/resource/epo/lot/codice_{replace(../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}_{cbc:ID[@schemeName='ID_LOTE']}")

``` 

 ## buyer_legal_type_0
- **Source**

```bash
buyer_legal_type.csv
``` 
- **Subject**
```bash
eu_uri
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
    
``` 
- **joinCondition**:
 ## procedure_framework_agreement_technique_usage_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://data.europa.eu/a4g/ontology#usesTechnique | {http://data.europa.eu/a4g/resource/epo/frameworkAgreementTechniqueUsage/codice_{replace(../../../id,"https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/","")}} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/epo/procedure/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}"] -->|"epo:usesTechnique"| object1("{http://data.europa.eu/a4g/resource/epo/frameworkAgreementTechniqueUsage/codice_{replace(../../../id,'https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/','')}}")
    
``` 
- **joinCondition**:
 ## organization_id_0
- **Source**

```bash
spanish_data.xml
``` 
- **Subject**
```bash
http://data.europa.eu/a4g/resource/org/identifier/{cac:PartyIdentification/cbc:ID[@schemeName="DIR3"]}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | epo:Identifier |
| http://data.europa.eu/a4g/ontology#hasIdentifierValue | {cac:PartyIdentification/cbc:ID[@schemeName="DIR3"]} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://data.europa.eu/a4g/resource/org/identifier/{cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}"] -->|"a"| object1("epo:Identifier")
S["http://data.europa.eu/a4g/resource/org/identifier/{cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}"] -->|"epo:hasIdentifierValue"| object2("{cac:PartyIdentification/cbc:ID[@schemeName='DIR3']}")
    
``` 
- **joinCondition**:
 ## procedure_type_0
- **Source**

```bash
procedure_type.csv
``` 
- **Subject**
```bash
eu_uri
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
    
``` 
- **joinCondition**:
 



----

**Copyright © 2024** *[Ontology Engineering Group](https://oeg.fi.upm.es/)*, *[Universidad Politécnica de Madrid](https://www.upm.es/internacional)*.
