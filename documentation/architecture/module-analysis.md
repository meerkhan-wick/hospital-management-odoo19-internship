# Odoo 19 — Module Structure & Dependency Analysis

Day 3 · Practical Tasks 2, 3 & 7

---

## Practical Task 2 — Comparing Three Existing Modules

Modules compared: **`crm`**, **`sale`**, **`project`** (standard Odoo Community apps).

> ⚠️ Note: exact filenames vary slightly by version — check each module's own folder for the authoritative list. The table below reflects the typical structure.

| Component | `crm` | `sale` | `project` |
|---|---|---|---|
| Module directory | `addons/crm/` | `addons/sale/` | `addons/project/` |
| `__init__.py` | ✅ imports `models`, `wizard`, `report` | ✅ imports `models`, `wizard`, `report`, `controllers` | ✅ imports `models`, `wizard`, `controllers` |
| `__manifest__.py` | ✅ | ✅ | ✅ |
| Models | `crm.lead`, `crm.stage`, `crm.team` | `sale.order`, `sale.order.line`, `sale.order.template` | `project.project`, `project.task`, `project.task.type` |
| Views | Kanban/list/form for leads & pipeline | Order form, quotation templates, portal views | Kanban board, task form, Gantt |
| Security | `ir.model.access.csv` + `crm_security.xml` (record rules per sales team) | `ir.model.access.csv` + multi-company/portal rules | `ir.model.access.csv` + project-membership rules |
| Data | Default stages, mail templates | Sequences, default order settings | Default task stages |
| Reports | Pipeline analysis (QWeb/BI) | Quotation/Order PDF report (QWeb) | Task/burndown reports |
| Wizards | `crm.lead.merge` (merge duplicate leads) | `sale.order.cancel`, discount wizard | `project.task.type.delete` |
| Controllers | — (rarely needed) | ✅ portal controllers (customer views their quotation online) | — (Community; more in Enterprise) |

**Takeaway:** not every module needs every folder. `crm` and `project` are largely self-contained apps with no public-facing controllers, while `sale` needs controllers because customers view/approve quotations through the online portal. Structure follows function, not a fixed template.

---

## Practical Task 3 — Module Dependencies & Loading

**Example: `sale`**

A module's dependencies live in its manifest:

```python
{
    'name': 'Sales',
    'depends': ['sales_team', 'product', 'account', 'portal', 'digest', 'mail'],
    ...
}
```

*(Check your local `sale/__manifest__.py` for the exact, version-accurate list — it can change between releases.)*

**What each dependency typically provides `sale` with:**
- `product` → the `product.template`/`product.product` models sale order lines rely on
- `account` → invoicing models (`account.move`) used when confirming an order
- `portal` → customer-facing portal infrastructure for the online quotation view
- `mail` → chatter/activities/notifications on the sale order

**Loading order:** Odoo builds a dependency graph from every installed module's `depends` list and topologically sorts it — a module is never loaded before all of its dependencies are loaded. `base` is the root dependency almost everything ultimately depends on.

**If a required dependency is removed/uninstalled:**
- Any model, field, or view that `sale` inherits from that dependency becomes unavailable
- Odoo will refuse to uninstall a module that others still depend on (it lists the dependent modules and blocks the action) unless you explicitly cascade-uninstall
- If forced, the dependent module (`sale`) breaks — missing models cause `KeyError`s, missing views fail to render, and the module is effectively unusable until reinstalled

---

## Practical Task 7 — Deep-Dive: Structure of One Module (`crm`)

```
crm/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── crm_lead.py          # main opportunity/lead model
│   ├── crm_stage.py         # pipeline stages
│   └── crm_team.py          # sales teams
├── views/
│   ├── crm_lead_views.xml   # kanban, list, form, pivot, calendar
│   └── crm_team_views.xml
├── security/
│   ├── ir.model.access.csv  # CRUD access per group
│   └── crm_security.xml     # record rules (team-based visibility)
├── data/
│   └── crm_stage_data.xml   # default pipeline stages
├── report/
│   └── crm_lead_report_views.xml  # pipeline analysis
├── wizard/
│   └── crm_lead_merge.py    # merge-duplicate-leads wizard
├── static/                  # JS/SCSS for kanban widgets, icons
├── i18n/                    # translations
└── tests/                   # Python unit/integration tests
```

**Purpose:** manage the sales pipeline — leads, opportunities, and their progression through stages.

**Dependencies:** `base`, `mail`, `sales_team`, `calendar`, `utm` (approximate — verify against the local manifest).

**How the pieces relate:**
```
models/  →  defines crm.lead, crm.stage
views/   →  render those models (kanban board = the pipeline)
security/→  controls who can see/edit which leads (team-based rules)
data/    →  seeds default stages so the pipeline isn't empty on install
wizard/  →  extra UI actions (merge) that operate on existing records
report/  →  analytical views built on top of crm.lead
```

**Lesson for Hospital Management System design:** each planned module (`hospital_patient`, `hospital_appointment`, etc.) should follow this same separation — models define the data, views expose it, security scopes visibility (e.g. a doctor only sees their own patients), and wizards/reports are added only where actually needed.