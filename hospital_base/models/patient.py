from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Patient Name',
        required=True,
        index=True,
        tracking=True,
    )
    ref = fields.Char(
        string='Patient Reference',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: self.env['ir.sequence'].next_by_code(
            'hospital.patient'
        ),
    )
    dob = fields.Date(
        string='Date of Birth',
    )
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
    )
    age_group = fields.Selection(
        selection=[
            ('minor', 'Minor'),
            ('adult', 'Adult'),
        ],
        string='Age Group',
        compute='_compute_age_group',
    )
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        string='Gender',
    )
    phone = fields.Char(
        string='Phone',
    )
    email = fields.Char(
        string='Email',
    )
    address = fields.Char(
        string='Address',
    )
    registration_date = fields.Date(
        string='Registration Date',
        default=fields.Date.context_today,
        required=True,
        readonly=True,
    )
    active = fields.Boolean(
        default=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('archived', 'Archived'),
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True,
    )
    notes = fields.Text(
        string='Notes',
    )
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Primary Doctor',
        ondelete='restrict',
        tracking=True,
    )
    doctor_ids = fields.Many2many(
        comodel_name='hospital.doctor',
        string='Treating Doctors',
    )
    doctor_specialization = fields.Char(
        string='Doctor Specialization',
        related='doctor_id.specialization',
        store=True,
    )
    doctor_count = fields.Integer(
        string='Doctors',
        compute='_compute_doctor_count',
    )

    _ref_unique = models.Constraint(
        'UNIQUE(ref)',
        'Patient reference must be unique.',
    )

    @api.depends('dob')
    def _compute_age(self):
        today = fields.Date.context_today(self)

        for patient in self:
            if not patient.dob:
                patient.age = 0
                continue

            patient.age = (
                    today.year
                    - patient.dob.year
                    - (
                            (today.month, today.day)
                            < (patient.dob.month, patient.dob.day)
                    )
            )

    @api.depends('dob')
    def _compute_age_group(self):
        for patient in self:
            if not patient.dob:
                patient.age_group = False
            else:
                patient.age_group = (
                    'minor' if patient.age < 18 else 'adult'
                )

    @api.depends('doctor_ids')
    def _compute_doctor_count(self):
        for patient in self:
            patient.doctor_count = len(patient.doctor_ids)

    @api.constrains('dob')
    def _check_date_of_birth(self):
        today = fields.Date.context_today(self)

        for patient in self:
            if patient.dob and patient.dob > today:
                raise ValidationError(
                    'Date of birth cannot be in the future.'
                )

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)

    def action_activate(self):
        self.write({
            'state': 'active',
            'active': True,
        })
        return True

    def action_archive_patient(self):
        self.write({
            'state': 'archived',
            'active': False,
        })
        return True

    def action_reset_to_draft(self):
        self.write({
            'state': 'draft',
            'active': True,
        })
        return True

    def action_validate_patient(self):
        self.ensure_one()

        if not self.dob:
            raise UserError(
                'Please set the patient date of birth before validation.'
            )

        self.action_activate()
        return True

    def action_open_doctors(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Treating Doctors',
            'res_model': 'hospital.doctor',
            'view_mode': 'list,form',
            'domain': [
                ('id', 'in', self.doctor_ids.ids),
            ],
        }

    def action_send_registration_email(self):
        self.ensure_one()

        if not self.email:
            raise UserError(
                'Please set an email address before sending '
                'the registration email.'
            )

        template = self.env.ref(
            'hospital_base.mail_template_patient_registration',
            raise_if_not_found=False,
        )

        if not template:
            raise UserError(
                'The patient registration email template was not found.'
            )

        template.send_mail(
            self.id,
            force_send=False,
        )

        return True
