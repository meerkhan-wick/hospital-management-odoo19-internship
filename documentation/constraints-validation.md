# Constraints and Validation

## 1. What is a Constraint?

A constraint is a rule that prevents invalid data from being stored in Odoo.

## 2. Python Constraint vs SQL Constraint

A Python constraint is implemented with `@api.constrains` and performs business validation in Python.

An SQL constraint is enforced by the database and is useful for rules such as unique values.

## 3. @api.constrains

`@api.constrains` defines a method that Odoo executes when the specified fields are created or updated.

## 4. When is a Python Constraint Triggered?

It is triggered when a record is created or updated and one of the fields specified in `@api.constrains` is involved.

## 5. Why Use Database-Level Integrity?

Important integrity rules should sometimes be enforced by the database because database constraints protect data regardless of whether it comes from the user interface, ORM, import, RPC, or another module.

## 6. ValidationError

`ValidationError` is used when entered data violates a validation or business rule.

Example:

```python
raise ValidationError('Date of birth cannot be in the future.')
