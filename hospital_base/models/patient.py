from datetime import date
from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(
        string='Patient Name',
        required=True,
        help='Enter the full name of the patient.'
    )

    ref = fields.Char(
        string='Patient Reference',
        index=True,
        copy=False,
        help='Unique reference used to identify the patient.'
    )

    dob = fields.Date(
        string='Date of Birth',
        help='Enter the patient date of birth.'
    )

    age = fields.Integer(
        string='Age',
        help='Enter the patient age in years.'
    )

    age_group = fields.Char(
        string='Age Group',
        compute='_compute_age_group',
        store=True,
    )

    doctor_specialization = fields.Char(
        string='Doctor Specialization',
        related='doctor_id.specialization',
    )

    registration_date = fields.Date(
        string='Registration Date',
        default=lambda self: fields.Date.today(),
    )

    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        string='Gender'
    )

    phone = fields.Char(
        string='Phone',
        help='Enter the patient phone number.'
    )

    email = fields.Char(
        string='Email',
        help='Enter the patient email address.'
    )

    address = fields.Char(
        string='Address',
        help='Enter the patient address.'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('archived', 'Archived'),
        ],
        string='Status',
        default='draft',
        required=True
    )

    doctor_count = fields.Integer(
        string='Doctors',
        compute='_compute_doctor_count'
    )

    notes = fields.Text(
        string='Notes',
        help='Additional notes about the patient.'
    )

    def action_create_demo_patients(self):
        Patient = self.env['hospital.patient']
        Patient.create({'name': 'Ali Raza', 'ref': 'PAT-001', 'age': 30, 'gender': 'male'})
        Patient.create({'name': 'Sana Khan', 'ref': 'PAT-002', 'age': 25, 'gender': 'female'})
        Patient.create([
            {'name': 'Bilal Ahmed', 'ref': 'PAT-003', 'age': 40, 'gender': 'male'},
            {'name': 'Ayesha Noor', 'ref': 'PAT-004', 'age': 22, 'gender': 'female'},
        ])

    def action_read_demo_patients(self):
        patients = self.env['hospital.patient'].search([])
        for patient in patients:
            print(patient.id, patient.name, patient.age, patient.gender)

    def action_search_demo_patients(self):
        Patient = self.env['hospital.patient']
        active_patients = Patient.search([('active', '=', True)])
        male_patients = Patient.search([('gender', '=', 'male')])
        by_name = Patient.search([('name', 'like', 'Ali')])
        recent = Patient.search([], limit=5, order='id desc')
        return active_patients, male_patients, by_name, recent

    def action_update_demo_patients(self):
        Patient = self.env['hospital.patient']
        patient = Patient.search([('ref', '=', 'PAT-001')], limit=1)
        if patient:
            patient.write({'age': 31})

        male_patients = Patient.search([('gender', '=', 'male')])
        male_patients.write({'active': True})

    def action_delete_demo_patients(self):
        Patient = self.env['hospital.patient']
        test_patients = Patient.search([('ref', 'like', 'PAT-00')])
        test_patients.unlink()

    def action_count_and_browse_demo(self):
        Patient = self.env['hospital.patient']
        count = Patient.search_count([('gender', '=', 'female')])
        patient = Patient.browse(1)  # use a real existing ID
        exists = patient.exists()
        return count, patient, exists

    def action_orm_demo(self):
        Patient = self.env['hospital.patient']

        new_patient = Patient.create({'name': 'Demo Patient', 'ref': 'PAT-DEMO', 'age': 28, 'gender': 'male'})

        found = Patient.search([('ref', '=', 'PAT-DEMO')])

        for p in found:
            print(p.name, p.age)

        found.write({'age': 29})

        total = Patient.search_count([])

        found.unlink()

        return total

    def action_domain_search_examples(self):
        Patient = self.env['hospital.patient']

        male_patients = Patient.search([('gender', '=', 'male')])
        non_male = Patient.search([('gender', '!=', 'male')])
        adults = Patient.search([('age', '>', 18)])
        young_patients = Patient.search([('age', '<=', 12)])
        name_like = Patient.search([('name', 'like', 'Ali')])
        name_ilike = Patient.search([('name', 'ilike', 'ali')])
        specific_refs = Patient.search([('ref', 'in', ['PAT-001', 'PAT-002'])])
        excluded_refs = Patient.search([('ref', 'not in', ['PAT-DEMO'])])

        adult_males = Patient.search([
            ('gender', '=', 'male'),
            ('age', '>=', 18),
        ])

        male_or_female = Patient.search([
            '|',
            ('gender', '=', 'male'),
            ('gender', '=', 'female'),
        ])

        not_female = Patient.search([
            '!', ('gender', '=', 'female'),
        ])

        active_known_gender = Patient.search([
            ('active', '=', True),
            '|',
            ('gender', '=', 'male'),
            ('gender', '=', 'female'),
        ])

        return {
            'male_patients': male_patients,
            'non_male': non_male,
            'adults': adults,
            'young_patients': young_patients,
            'name_like': name_like,
            'name_ilike': name_ilike,
            'specific_refs': specific_refs,
            'excluded_refs': excluded_refs,
            'adult_males': adult_males,
            'male_or_female': male_or_female,
            'not_female': not_female,
            'active_known_gender': active_known_gender,
        }

    def action_filtered_examples(self):
        patients = self.env['hospital.patient'].search([])

        active_patients = patients.filtered(lambda p: p.active)
        adult_patients = patients.filtered(lambda p: p.age >= 18)
        adult_male_patients = patients.filtered(
            lambda p: p.age >= 18 and p.gender == 'male'
        )

        return active_patients, adult_patients, adult_male_patients

    def action_mapped_examples(self):
        patients = self.env['hospital.patient'].search([])

        names = patients.mapped('name')
        ages = patients.mapped('age')
        genders = patients.mapped('gender')

        return names, ages, genders

    def action_sorted_examples(self):
        patients = self.env['hospital.patient'].search([])

        by_age_asc = patients.sorted(key=lambda p: p.age)
        by_name_desc = patients.sorted(key=lambda p: p.name, reverse=True)

        return by_age_asc, by_name_desc

    def action_ensure_one_demo(self):
        self.ensure_one()
        return "Single patient confirmed: %s" % self.name

    def action_test_ensure_one(self):
        Patient = self.env['hospital.patient']
        all_patients = Patient.search([])

        result_one = None
        if all_patients:
            single = all_patients[0]
            result_one = single.action_ensure_one_demo()

        result_many = None
        try:
            all_patients.action_ensure_one_demo()
            result_many = 'Unexpectedly succeeded'
        except ValueError as e:
            result_many = 'Raised as expected: %s' % e

        return result_one, result_many

    def action_inspect_environment(self):
        user = self.env.user
        company = self.env.company
        context = self.env.context
        Patient = self.env['hospital.patient']

        return {
            'user_name': user.name,
            'user_login': user.login,
            'company_name': company.name,
            'context_keys': list(context.keys()),
            'patient_model_name': Patient._name,
        }

    def action_analyze_patients(self):
        Patient = self.env['hospital.patient']

        patients = Patient.search([('active', '=', True)])
        adult_patients = patients.filtered(lambda p: p.age >= 18)
        patient_names = adult_patients.mapped('name')
        sorted_patients = adult_patients.sorted(key=lambda p: p.age, reverse=True)

        oldest_name = None
        if sorted_patients:
            oldest = sorted_patients[0]
            oldest.ensure_one()
            oldest_name = oldest.name

        return {
            'patients_type': type(patients),
            'adult_patients_type': type(adult_patients),
            'patient_names_type': type(patient_names),
            'sorted_patients_type': type(sorted_patients),
            'patient_names': patient_names,
            'oldest_patient': oldest_name,
        }

    doctor_id = fields.Many2one(
        'hospital.doctor',
        string='Primary Doctor',
        ondelete='set null'
    )

    doctor_ids = fields.Many2many(
        'hospital.doctor',
        string='Treating Doctors'
    )

    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                today = date.today()
                record.age = today.year - record.dob.year - (
                        (today.month, today.day) <
                        (record.dob.month, record.dob.day)
                )
            else:
                record.age = 0

    @api.depends('age')
    def _compute_age_group(self):
        for record in self:
            if record.age < 18:
                record.age_group = 'Minor'
            else:
                record.age_group = 'Adult'

    @api.constrains('dob')
    def _check_date_of_birth(self):
        for record in self:
            if record.dob and record.dob > fields.Date.today():
                raise ValidationError('Date of birth cannot be in the future.')

    def action_validate_patient(self):
        self.ensure_one()

        if not self.dob:
            raise UserError('Please set the patient date of birth before validation.')

        return True

    _sql_constraints = [
        (
            'unique_patient_ref',
            'UNIQUE(ref)',
            'Patient reference must be unique.'
        ),
    ]

    @api.depends('doctor_ids')
    def _compute_doctor_count(self):
        for record in self:
            record.doctor_count = len(record.doctor_ids)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_archive(self):
        self.write({'state': 'archived'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    def action_open_doctors(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Treating Doctors',
            'res_model': 'hospital.doctor',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.doctor_ids.ids)],
        }

    def _cron_update_patients(self, limit=300):
        today = fields.Date.today()

        patients = self.search(
            [('dob', '!=', False)],
            limit=limit,
            order='id',
        )

        for patient in patients:
            new_age = today.year - patient.dob.year - (
                    (today.month, today.day) < (patient.dob.month, patient.dob.day)
            )

            if patient.age != new_age:
                patient.write({'age': new_age})

        remaining = self.search_count([
            ('dob', '!=', False),
            ('id', '>', patients[-1].id),
        ]) if patients else 0

        self.env['ir.cron']._commit_progress(
            len(patients),
            remaining=remaining,
        )

    def action_send_registration_email(self):
        self.ensure_one()

        if not self.email:
            raise UserError("Please set an email address before sending the registration email.")

        template = self.env.ref(
            "hospital_base.mail_template_patient_registration"
        )

        template.send_mail(self.id, force_send=True)

        return True

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        template = self.env.ref(
            'hospital_base.mail_template_patient_registration',
            raise_if_not_found=False,
        )

        if template:
            for record in records:
                if record.email:
                    template.send_mail(record.id, force_send=True)

        return records
