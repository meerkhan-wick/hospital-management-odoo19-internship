from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(
        string='Doctor Name',
        required=True
    )

    license_ref = fields.Char(
        string='License/Reference',
        copy=False
    )

    specialization = fields.Char(
        string='Specialization'
    )

    phone = fields.Char(
        string='Phone'
    )

    email = fields.Char(
        string='Email'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    patient_ids = fields.One2many(
        'hospital.patient',
        'doctor_id',
        string='Primary Patients'
    )

    @api.constrains('name')
    def _check_doctor_name(self):
        for record in self:
            if record.name and len(record.name.strip()) < 3:
                raise ValidationError('Doctor name must contain at least 3 characters.')

    patient_count = fields.Integer(
        string='Patients',
        compute='_compute_patient_count'
    )

    def _compute_patient_count(self):
        for record in self:
            record.patient_count = len(record.patient_ids)

    def action_open_patients(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Patients',
            'res_model': 'hospital.patient',
            'view_mode': 'list,form',
            'domain': [('doctor_id', '=', self.id)],
        }
