# Odoo 19 — Registry, ORM & Request Flow

Day 3 · Practical Tasks 4, 5 & 6

---

## Practical Task 4 — The Odoo Registry

**What is it?** A per-database, in-memory Python object holding every installed model class (with its fields and methods merged from all modules that extend it).

**When is it created?** On first access to a database after server start, and rebuilt automatically whenever a module is installed, upgraded, or uninstalled.

**What does it contain?** One entry per model (`res.partner`, `crm.lead`, future `hospital.patient`, …), each carrying its combined field definitions, methods, and constraints — including everything added by inheritance (`_inherit`) from other modules.

**How are models registered?** When a module loads, its Python model classes are imported and merged into the Registry under their `_name`. If another module later inherits the same model (`_inherit = 'res.partner'`) and adds fields, the Registry entry for that model is updated to include them.

**What happens on upgrade?** The Registry is rebuilt: new/changed fields are reflected in PostgreSQL (`ALTER TABLE`), new views/data are (re)loaded, and the in-memory model definitions are refreshed to match the new code.

**Why it matters to the ORM:** the ORM never talks to the database using anything except what the Registry says a model looks like. No Registry entry → the ORM has no idea the model exists.

```
Odoo Server
     ↓
Database (per-DB connection)
     ↓
Registry   (in-memory model definitions for this DB)
     ↓
Models     (res.partner, crm.lead, hospital.patient, ...)
     ↓
ORM        (translates Python calls to SQL)
     ↓
PostgreSQL
```

---

## Practical Task 5 — ORM Architecture

| Concept | Meaning |
|---|---|
| **Model** | A Python class (`models.Model`) mapping to one PostgreSQL table |
| **Field** | A typed attribute of a model (`Char`, `Many2one`, `Date`, …) mapping to a column |
| **Record** | One row of data for a model |
| **Recordset** | An ordered collection of records of the same model (even a single record is a recordset of length 1) — the core object you work with in Odoo code |
| **Environment (`env`)** | Carries the current user, database cursor, and context; every ORM call goes through it (`self.env['model.name']`) |
| **ORM** | Translates Python method calls on recordsets (`create`, `write`, `search`, `browse`) into SQL against the Registry's model definitions |
| **PostgreSQL Table** | The physical storage — one table per model, one row per record |

### Mapping for the Future Hospital Management System

```
Patient Model (hospital.patient)
      ↓
Patient Fields (name, dob, gender, doctor_id, ...)
      ↓
Patient Records (one row per real patient)
      ↓
ORM (env['hospital.patient'].create({...}) / .search([...]))
      ↓
PostgreSQL (table: hospital_patient)
```

**Example:** `self.env['hospital.patient'].create({'name': 'John Doe', 'dob': '1990-01-01'})` — the ORM takes this Python call, resolves `hospital.patient` via the Registry, builds an `INSERT` into the `hospital_patient` table, and returns a recordset representing the new row.

---

## Practical Task 6 — Request Flow

```
Browser
   ↓  HTTP request
Odoo Server
   ↓
Controller / Framework
   ↓
ORM
   ↓
PostgreSQL
   ↓
ORM
   ↓
Odoo Response
   ↓
Browser
```

**Walkthrough — opening the Apps menu:**

1. Browser sends an HTTP request for the Apps action (menu click → JSON-RPC call to `/web/dataset/call_kw`)
2. The Odoo server's HTTP layer routes it to the relevant controller (web client's action-loading endpoint)
3. The controller calls the ORM: `env['ir.module.module'].search_read([...])`
4. The ORM, using the Registry's definition of `ir.module.module`, builds and executes the corresponding SQL `SELECT` against PostgreSQL
5. PostgreSQL returns matching rows
6. The ORM wraps them back into a recordset / list of dicts
7. The controller serializes this into a JSON response
8. The browser receives it and the OWL web client renders the Apps grid

This same round-trip (Browser → Controller → ORM → PostgreSQL → back) is what will happen for every action in the Hospital Management System — e.g. loading the patient list, saving a new appointment, or confirming a prescription.