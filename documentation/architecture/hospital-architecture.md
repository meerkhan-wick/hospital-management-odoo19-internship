# Hospital Management System — Planned Module Architecture

Day 3 · Practical Task 8

No modules have been created yet — this is the design/planning stage only.

---

## High-Level Module Plan

```
Hospital Management System
│
├── hospital_base
├── hospital_patient
├── hospital_doctor
├── hospital_appointment
├── hospital_consultation
├── hospital_prescription
└── hospital_billing
```

---

## `hospital_base`

**Purpose:** foundational module every other `hospital_*` module depends on.
**Main responsibility:** shared configuration, sequences, common security groups, and base data (departments, specializations) used across the whole system.
**Expected dependencies:** `base`, `mail`
**Possible models:** `hospital.department`, `hospital.config.settings`
**Possible views:** Settings screen, department list/form

## `hospital_patient`

**Purpose:** manage patient records.
**Main responsibility:** store patient demographics, contact info, and medical history references.
**Expected dependencies:** `hospital_base`, `contacts` (or extend `res.partner`)
**Possible models:** `hospital.patient`
**Possible views:** Patient kanban/list/form, search filters (by name, doctor, department)

## `hospital_doctor`

**Purpose:** manage doctor records and availability.
**Main responsibility:** doctor profiles, specialization, department assignment, working schedule.
**Expected dependencies:** `hospital_base`, `hr` (if linking to employee records) or `contacts`
**Possible models:** `hospital.doctor`, `hospital.doctor.schedule`
**Possible views:** Doctor list/form, schedule calendar

## `hospital_appointment`

**Purpose:** book and manage patient appointments with doctors.
**Main responsibility:** appointment scheduling, status tracking (draft/confirmed/done/cancelled), conflict checks against doctor availability.
**Expected dependencies:** `hospital_patient`, `hospital_doctor`, `calendar`
**Possible models:** `hospital.appointment`
**Possible views:** Calendar view, list/form, kanban by status

## `hospital_consultation`

**Purpose:** record what happens during a patient visit.
**Main responsibility:** capture consultation notes, diagnosis, vitals, linked to the originating appointment.
**Expected dependencies:** `hospital_appointment`, `hospital_patient`, `hospital_doctor`
**Possible models:** `hospital.consultation`
**Possible views:** Consultation form (linked from appointment), patient consultation history list

## `hospital_prescription`

**Purpose:** manage prescriptions issued during a consultation.
**Main responsibility:** record prescribed medicines, dosage, and duration; link back to the consultation and patient.
**Expected dependencies:** `hospital_consultation`, `hospital_patient`, `hospital_doctor`, (optionally `product` for a medicine catalog)
**Possible models:** `hospital.prescription`, `hospital.prescription.line`
**Possible views:** Prescription form (from consultation), printable prescription report

## `hospital_billing`

**Purpose:** generate and manage invoices for consultations/services.
**Main responsibility:** bill patients for appointments, consultations, and prescribed items; integrate with accounting.
**Expected dependencies:** `hospital_consultation`, `hospital_patient`, `account`
**Possible models:** `hospital.invoice` (or direct `account.move` integration)
**Possible views:** Billing form, patient invoice history, payment status list

---

## Dependency Relationship

```
hospital_base
     ↓
hospital_patient ──┐
                    ├──► hospital_appointment ──► hospital_consultation ──► hospital_prescription
hospital_doctor ────┘                                    │
                                                           ▼
                                                    hospital_billing
```

`hospital_base` sits at the root; `hospital_patient` and `hospital_doctor` build on it independently; `hospital_appointment` ties the two together; `hospital_consultation`, `hospital_prescription`, and `hospital_billing` build progressively on the appointment/consultation chain — mirroring a real patient visit from booking → consultation → prescription → invoice.

**Design principle followed:** each module has a single, clear business responsibility (per the Day 3 development advice) — no module tries to own the entire application.