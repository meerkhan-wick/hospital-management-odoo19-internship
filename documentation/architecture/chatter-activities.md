# Chatter and Activities

## Chatter

Chatter provides communication and history directly on hospital patient records.

It allows hospital staff to:
- Post internal notes
- Send messages
- Manage followers
- View record history
- Track important field changes
- Schedule activities

## Followers

Followers are users or contacts subscribed to a patient record.

Followers can receive notifications when relevant updates occur.

Users can follow and unfollow patient records directly from the Chatter.

## Internal Messages

Internal messages are record-specific communications stored in the patient's Chatter.

Examples:
- Doctor review required
- Follow-up required
- Additional information needed

## Field Tracking

Important Patient fields use tracking=True.

Tracked fields:
- State
- Primary Doctor

Changes to these fields appear automatically in the patient's Chatter.

## Activities

Activities represent work that a user needs to perform.

Examples:
- Review Patient
- Call Patient
- Doctor Review
- Follow Up

Activities are assigned to users and can be scheduled and completed from the Patient record.

## Automatic Workflow

When a Patient is registered:

Patient Created
    ↓
Registration Email
    ↓
Review Patient Activity
    ↓
Staff Review
    ↓
Activity Completed
    ↓
Chatter Note

The automatic activity is created during patient creation only, preventing new review activities from being generated whenever the patient is edited.

## Testing

The following were tested:
- Chatter visibility
- Internal messages
- Log notes
- Followers
- Unfollow
- Notifications
- Field tracking
- Activity scheduling
- Activity completion
- Automatic review activity
- Different hospital users
- Security permissions