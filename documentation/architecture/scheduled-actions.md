# Patient Scheduled Automation

## Automation Name

Patient Age Automation

## Purpose

The scheduled action automatically recalculates the age of patients who have a date of birth.

## Model

`hospital.patient`

## Python Method

`_cron_update_patients()`

## Business Operation

The Cron searches for patients with a date of birth, calculates their current age, and updates the `age` field only when the calculated value differs from the existing value.

## Execution Frequency

The production interval is once per day.

A one-minute interval was used temporarily during development testing.

## Workflow

Scheduled Action
↓
Odoo Scheduler
↓
`model._cron_update_patients()`
↓
`hospital.patient` records
↓
Calculate current age from DOB
↓
Update age when required

## Safety

The automation processes patients in batches instead of attempting to process an unlimited number of records at once.

Patients without a date of birth are ignored.

The method checks whether the calculated age differs before writing, preventing unnecessary repeated updates.

## Expected Result

Patient ages remain synchronized with their dates of birth without requiring manual updates.

## Testing Result

Manual execution of the Scheduled Action was tested successfully.

Automatic execution was tested using a temporary one-minute interval.

The production configuration is set to execute once per day.

No duplicate records are created by the automation.
