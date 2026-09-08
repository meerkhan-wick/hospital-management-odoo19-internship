# Day 8 — Advanced ORM Recordsets

## Conceptual Questions

**search() vs filtered()**
`search()` runs a domain against the database — filtering happens in SQL and
only matching rows are loaded. `filtered()` runs on a recordset already in
memory and filters it in Python using a lambda.

**mapped()**
Extracts a value (or list of values) from every record in a recordset in one
call, e.g. `patients.mapped('name')` returns a plain Python list of names.
Works on simple fields and can traverse relational fields
(`patients.mapped('doctor_id.name')`).

**sorted()**
Returns a new recordset ordered by a key function, evaluated in Python.
`patients.sorted(key=lambda p: p.age)` sorts ascending;
`reverse=True` sorts descending.

**filtered() vs a database domain**
A domain filters before records are fetched — cheaper for large tables since
only matching rows are loaded. `filtered()` requires the full recordset to
already be in memory, so it should only be used for conditions a domain can't
express.

**ensure_one()**
Raises an exception unless the recordset it's called on has exactly one
record. Used at the top of methods that only make sense for a single record.

**self.env**
The Environment object — carries the current user, cursor, context, and
access to every model via `self.env['model.name']`.

**self.env.user**
The `res.users` record for whoever is executing the code.

**self.env.company**
The `res.company` record currently active (relevant in multi-company setups).

**self.env.context**
A dict of contextual keys/values (language, timezone, defaults, flags) that
travels with ORM calls.

**Why prefer domains over Python-side filtering**
Database filtering avoids loading records you'll immediately discard —
faster and lighter, especially at scale, since the database engine (with
indexes) does the work instead of Python iterating in memory.

---

## Task 1 & 2 — Domain Search Examples (actual results)

| Method | Domain type | Count | Names returned |
|---|---|---|---|
| `male_patients` | equality | 2 | Ali Raza, Bilal Ahmed |
| `non_male` | not equal | 2 | Sana Khan, Ayesha Noor |
| `adults` | greater than (age > 18) | 4 | Ali Raza, Sana Khan, Bilal Ahmed, Ayesha Noor |
| `young_patients` | less/equal (age <= 12) | 0 | (none) |
| `name_like` | case-sensitive partial | 1 | Ali Raza |
| `name_ilike` | case-insensitive partial | 1 | Ali Raza |
| `specific_refs` | in | 2 | Ali Raza, Sana Khan |
| `excluded_refs` | not in | 4 | Ali Raza, Sana Khan, Bilal Ahmed, Ayesha Noor |
| `adult_males` | implicit AND | 2 | Ali Raza, Bilal Ahmed |
| `male_or_female` | OR | 4 | Ali Raza, Sana Khan, Bilal Ahmed, Ayesha Noor |
| `not_female` | NOT | 2 | Ali Raza, Bilal Ahmed |
| `active_known_gender` | AND + OR | 4 | Ali Raza, Sana Khan, Bilal Ahmed, Ayesha Noor |

Note: `excluded_refs` returns all 4 records because none of the current
patients have `ref = 'PAT-DEMO'` — that demo record is created and deleted
within `action_orm_demo()` itself, so excluding it from a "not in" search
naturally matches everyone else.

## Task 3 — filtered() (actual results)

- active: Ali Raza, Sana Khan, Bilal Ahmed, Ayesha Noor
- adults (age >= 18): Ali Raza, Sana Khan, Bilal Ahmed, Ayesha Noor
- adult males: Ali Raza, Bilal Ahmed

## Task 4 — mapped() (actual results)

- names: ['Ali Raza', 'Sana Khan', 'Bilal Ahmed', 'Ayesha Noor']
- ages: [30, 25, 40, 22]
- genders: ['male', 'female', 'male', 'female']

## Task 5 — sorted() (actual results)

- by age ascending: Ayesha Noor (22), Sana Khan (25), Ali Raza (30), Bilal Ahmed (40)
- by name descending: Sana Khan, Bilal Ahmed, Ayesha Noor, Ali Raza

## Task 6 — ensure_one() (actual results)

- One record: `"Single patient confirmed: Ali Raza"` — method executes normally.
- Multiple records: raises
  `ValueError: Expected singleton: hospital.patient(7, 8, 9, 10)`
  — confirms `ensure_one()` blocks execution on a multi-record recordset.

## Task 7 — Environment (actual results)

| Object | What it represents | Observed value |
|---|---|---|
| `self.env.user` | currently logged-in `res.users` record | name: OdooBot, login: `__system__` (shell runs as superuser) |
| `self.env.company` | active `res.company` record | My Company |
| `self.env.context` | dict of contextual keys | keys: `lang`, `tz`, `uid` |
| `self.env['hospital.patient']` | the model class itself | `hospital.patient` |

## Task 8 — action_analyze_patients() pipeline (actual results)

| Step | Variable | Type | Value |
|---|---|---|---|
| `Patient.search([...])` | `patients` | recordset | 4 active patients |
| `patients.filtered(...)` | `adult_patients` | recordset | same 4 (all are adults) |
| `adult_patients.mapped('name')` | `patient_names` | `list` | Ali Raza, Sana Khan, Bilal Ahmed, Ayesha Noor |
| `adult_patients.sorted(...)` | `sorted_patients` | recordset | ordered oldest→youngest |
| `sorted_patients[0]` after `ensure_one()` | `oldest` | single-record recordset | Bilal Ahmed |

---

## Testing Checklist

- [x] Basic domain search tested
- [x] Multiple domain conditions tested
- [x] OR domain tested
- [x] filtered() tested
- [x] mapped() tested
- [x] sorted() tested
- [x] ensure_one() tested with one record
- [x] ensure_one() tested with multiple records
- [x] self.env inspected
- [x] self.env.user inspected
- [x] self.env.company inspected
- [x] self.env.context inspected
No traceback in server logs 
Module upgrades successfully