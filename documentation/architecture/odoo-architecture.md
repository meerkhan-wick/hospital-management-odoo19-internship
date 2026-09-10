# Odoo 19 — Architecture Overview

Day 3 · Section A (Conceptual) + Practical Task 1 (Source Code Exploration)

---

## 1. Overall Architecture of Odoo

Odoo follows a **3-tier architecture**:

```
┌─────────────────────┐
│   Web Client (UI)   │  Browser — OWL/JS framework renders views
└─────────┬────────────┘
          │ HTTP / JSON-RPC
┌─────────▼────────────┐
│    Odoo Server        │  Python — business logic, ORM, controllers,
│  (odoo-bin process)   │  Registry, security
└─────────┬────────────┘
          │ SQL (psycopg2)
┌─────────▼────────────┐
│     PostgreSQL         │  Persistent data storage
└─────────────────────┘
```

The server is the only layer that talks to the database — the browser never queries PostgreSQL directly.

## 2. Role of the Odoo Server

The Odoo server (`odoo-bin`) is the Python process that:
- Loads installed modules into the **Registry**
- Exposes business logic through the **ORM**
- Routes HTTP requests to **controllers**
- Enforces **security** (access rights, record rules)
- Serves the web client and REST/JSON-RPC endpoints

## 3. Purpose of PostgreSQL

PostgreSQL is Odoo's data layer. Each Odoo **database** is a PostgreSQL database. Every model (`models.Model`) maps to one PostgreSQL table, and every field maps to a column. Odoo never supports another RDBMS — the ORM is written specifically against PostgreSQL's features (e.g. sequences, constraints, `unaccent`).

## 4. What Is an Odoo Addon

An **addon** is a directory that Odoo scans (via `addons_path`) for installable modules. "Addon" often refers to the folder/repository level — e.g. the `addons/` directory itself, or a custom addons repo like `custom_addons/`.

## 5. What Is an Odoo Module

A **module** is a single self-contained package inside an addons path — a folder containing a `__manifest__.py` plus its models, views, security, and data. It's the installable unit shown in *Apps*.

## 6. Addon vs. Module — the Difference

| | Addon | Module |
|---|---|---|
| Scope | The directory/location Odoo scans | One installable package inside that directory |
| Contains | Many modules | Models, views, security, data for one feature |
| Example | `addons/`, `custom_addons/` | `sale`, `crm`, `hospital_patient` |

In practice the two words are often used interchangeably, but technically *addon* = the container, *module* = the thing inside it.

## 7. The Odoo Registry

The **Registry** is an in-memory Python object, built **per database**, holding every installed model class and its fields/methods for that database. It's created:
- When the server starts and a request first hits a database
- Rebuilt when a module is installed/upgraded

The ORM always goes through the Registry to know which models exist and how they're structured — without it, no model would be reachable.

## 8. The Odoo ORM

The **ORM** (Object-Relational Mapper) is the Python API that lets developers define models as Python classes and interact with PostgreSQL rows as Python objects (**recordsets**) — without writing raw SQL for standard CRUD, while still allowing raw SQL when needed (`self.env.cr.execute(...)`).

## 9. What Happens When a Module Loads

1. `__manifest__.py` is read (name, `depends`, data files, `installable`)
2. Its `depends` modules are loaded first (recursively)
3. Python models are imported → registered into the Registry
4. Database tables/columns are created or altered (`ir.model`, `ir.model.fields`)
5. XML/CSV data (views, security, demo data) is loaded in the order listed in `data`/`demo`
6. Access rights (`ir.model.access.csv`) and record rules are applied
7. The module is marked `installed` in `ir.module.module`

## 10. Flow: Browser Request → Data Stored in PostgreSQL

```
Browser
   │  HTTP/JSON-RPC request (e.g. save a record)
   ▼
Odoo Server → routes to a Controller
   ▼
Controller calls ORM (env['model'].create()/write())
   ▼
ORM builds and executes SQL via the Registry's model definition
   ▼
PostgreSQL stores the row
   ▼
ORM returns the updated recordset to the Controller
   ▼
Controller serializes a JSON response
   ▼
Browser updates the UI
```

---

## Practical Task 1 — Odoo 19 Source Code Structure

| Path | Purpose |
|---|---|
| `odoo/` | Core framework package — everything the server runs on |
| `addons/` | Official Odoo Community modules shipped with the source |
| `odoo-bin` | Entry point script that starts the server (`./odoo-bin -d dbname`) |
| `odoo/addons/` | Framework-level base addons (e.g. `base`, `web`) bundled with core |
| `odoo/http.py` | HTTP layer — request routing, `Controller`/`route` decorators, sessions |
| `odoo/models.py` | The `Model`/`TransientModel`/`AbstractModel` base classes — the heart of the ORM |
| `odoo/fields.py` | All field type definitions (`Char`, `Many2one`, `Selection`, computed fields, etc.) |
| `odoo/api.py` | Decorators (`@api.model`, `@api.depends`, `@api.constrains`) and the `Environment` object |
| `odoo/service/` | Low-level services — database management, WSGI server, cron/scheduler |
| `odoo/tools/` | Shared utility functions used throughout the framework |

**Development note:** Odoo core files (`odoo/`, `addons/`) are never modified directly. Custom work stays isolated in a separate addons path (e.g. `custom_addons/`) so upgrades to Odoo core don't break custom modules.

**Screenshots:** see `screenshots/day3/` for the source tree exploration.

# Hospital Base Module Architecture

## 1. Module Purpose

Explain what `hospital_base` is and why it was created.

## 2. Module Location

Explain that the module is located inside:

`custom_addons/hospital_base`

## 3. Module Structure

Show:

custom_addons/
└── hospital_base/
    ├── __init__.py
    └── __manifest__.py

## 4. Module Dependencies

Explain that the module depends on:

`base`

Explain why `base` is required.

## 5. __manifest__.py

Explain:
- Module name
- Version
- Summary
- Category
- Author
- License
- Dependencies
- Data

## 6. __init__.py

Explain its purpose and that it is currently minimal because the module has no Python components yet.

## 7. Addons Path

Document the custom addons path:

`/home/ameer/hospital-management-odoo19-internship/custom_addons`

## 8. Installation Process

Explain:
1. Odoo scans the addons path.
2. `hospital_base` is discovered.
3. Apps List is updated.
4. Module is installed.
5. Odoo loads the module.

## 9. Upgrade Process

Explain:
1. Make a change to the module.
2. Upgrade the module.
3. Odoo reloads the module.
4. The changes are applied.

## 10. Command-Line Options

### -i
Used to install a module.

Example:

`-i hospital_base`

### -u
Used to upgrade an already installed module.

Example:

`-u hospital_base`

## 11. Module Loading

Odoo
↓
Addons Path
↓
hospital_base
↓
__manifest__.py
↓
__init__.py
↓
Module Loaded

## 12. Verification

Document that:
- The module appeared in Apps.
- The module was installed.
- The module was upgraded successfully.
- The server logs showed `hospital_base` loading successfully.

## 13. Errors Encountered

Document the addons-path problem you encountered and how it was resolved.
