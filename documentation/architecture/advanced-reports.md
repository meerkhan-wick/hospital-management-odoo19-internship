# Advanced Hospital PDF Reports

## Patient Report

The Patient Report is implemented using an Odoo QWeb PDF template.

It displays patient identification, date of birth, age, gender, contact details, address, doctor, specialization, registration date, status, and notes.

## External Layout

The report uses `web.external_layout` to provide the standard Odoo company header, footer, and page structure.

## Conditional Content

QWeb `t-if` and `t-else` are used to display patient notes only when notes exist.

## Multiple Records

The template loops through `docs` so multiple selected patient records can be included in the same report.

## Paper Format

A custom A4 Portrait paper format was created with controlled margins and header spacing.

## Consultation Report

A second QWeb PDF report was created for consultation records. It displays the confirmed consultation information available in the project.

## Dynamic Report Data

Standard reports automatically provide objects such as:

- docs
- doc_ids
- doc_model
- user
- res_company

A custom `_get_report_values()` method is only required when additional data preparation is necessary.

## Testing

Both reports were tested with different records, empty optional fields, multiple records, and long text.

## Result

The reports generate printable PDFs using the custom hospital paper format and standard Odoo external layout.