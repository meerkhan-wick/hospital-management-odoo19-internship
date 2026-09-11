# ORM & Recordsets — Day 7 Notes

## Methods Practiced
- `create()` — single dict and list-of-dicts (batch create)
- `search()` — empty domain, field domains, `limit`, `order`
- `write()` — single record and multi-record recordset
- `unlink()` — bulk delete on a filtered recordset
- `search_count()` — count without loading records
- `browse()` — fetch by known ID, checked with `.exists()`

## Observations
1. `browse(1)` returned `hospital.patient(1,)` even though no record with ID 1 exists in the database — `browse()` never queries the DB or validates the ID up front. Only calling `.exists()` (which returned an empty recordset) confirmed the record wasn't real.
2. An empty recordset (`Patient.search([('ref', '=', 'NOPE')])`) is falsy (`bool(empty) == False`, `len(empty) == 0`) but is still a valid recordset object, not `None` — so `if not patients:` is the correct emptiness check.
3. `write()` applied to a multi-record recordset (`male_patients.write({'active': True})`) updated both matching patients in a single call — no loop was needed, confirming batched updates.

## Deliverables
- Updated `patient.py` with create/search/read/update/count/browse/unlink demo methods and `action_orm_demo()` lifecycle method
- Screenshots of shell output for each method (see `/screenshots`)
- This file