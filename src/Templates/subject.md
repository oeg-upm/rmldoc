### Subject
| URI                                                          | label | comment |
| ------------------------------------------------------------ | ----- | ------- |
{% for s in subject -%}
| {{ s['template'] }} |       |        |
{%+ endfor %}