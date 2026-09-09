# QWeb Reports

## Report Type

The Patient Report uses `qweb-pdf` to generate a PDF document from a QWeb template.

## QWeb Template

The QWeb template defines the structure and content of the Patient Report.

The template accesses Patient data using:

- `t-field` for Odoo model fields
- `t-esc` for escaped expressions
- `t-if` and `t-else` for conditional content
- `t-foreach` for iterating through multiple records

## t-field vs t-esc

`t-field` is used for displaying Odoo model fields and supports Odoo field formatting.

Example:

```xml
<span t-field="doc.doctor_id"/>