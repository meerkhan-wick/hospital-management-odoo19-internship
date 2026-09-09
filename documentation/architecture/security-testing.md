# Hospital Security Implementation

## Groups

The Hospital Management System contains three security groups:

- Hospital User
- Hospital Doctor
- Hospital Manager

## ACL Policy

Hospital User:
- Read: Yes
- Create: No
- Write: No
- Delete: No

Hospital Doctor:
- Read: Yes
- Create: Yes
- Write: Yes
- Delete: No

Hospital Manager:
- Read: Yes
- Create: Yes
- Write: Yes
- Delete: Yes

## Record Rule

Hospital Doctors can access only patients assigned to their own Doctor record.

The rule uses:

[('doctor_id.user_id', '=', user.id)]

Hospital Managers can access all patient records.

## ACL vs Record Rule

ACL controls whether a user can perform an operation on a model.

Record Rule controls which records the user can access.

Example:

A Doctor may have Write access to the patient model through an ACL, but the Record Rule prevents that Doctor from modifying another Doctor's patient.

## Security Testing

Hospital User:
- Read: Passed
- Create: Blocked
- Write: Blocked
- Delete: Blocked

Hospital Doctor:
- Own patients: Allowed
- Other doctors' patients: Blocked
- Create: Allowed
- Write: Allowed
- Delete: Blocked

Hospital Manager:
- Read: Allowed
- Create: Allowed
- Write: Allowed
- Delete: Allowed

## Security Review

Security was tested using multiple users rather than Administrator.

ACLs and Record Rules were tested together.

No sudo() was used to bypass security.