# Computed, Related and Default Fields

## Computed Field

A computed field automatically calculates its value from other fields.

Example: Patient age is calculated from birth_date.

Computed fields are normally not stored unless store=True is used.

## Stored Computed Field

A stored computed field is calculated automatically and saved in the database.

Example: age_group depends on patient age.

store=True is useful when the value needs to be searched, sorted or grouped efficiently.

## Related Field

A related field retrieves a value through a relationship.

Example: doctor_specialization retrieves specialization from the selected doctor.

It avoids duplicating the same business information.

## Default Field

A default field automatically initializes a value when a new record is created.

Example: registration_date is automatically set to today's date.

## Comparison

| Type | Purpose | Example |
|---|---|---|
| Computed | Calculate a value | Patient Age |
| Stored Computed | Calculate and store a value | Age Group |
| Related | Retrieve value through relationship | Doctor Specialization |
| Default | Initialize a value | Registration Date |

## Testing Observations

1. Age is automatically calculated from birth date.
2. Empty birth date results in age 0.
3. Changing birth date recalculates age.
4. Selecting a doctor automatically displays the doctor's specialization.
5. Changing the doctor updates the related specialization.
6. Registration date is automatically assigned to new patients.
7. Multiple patient records can be processed by the compute methods.