from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request


class HospitalWebsite(http.Controller):

    @http.route(
        '/hospital/patients',
        type='http',
        auth='public',
        website=True,
        sitemap=True,
    )
    def patients(self, **kwargs):
        patients = request.env['hospital.patient'].sudo().search(
            [('state', '=', 'active')],
            order='name',
        )
        return request.render(
            'hospital_base.patient_website_page',
            {'patients': patients},
        )

    @http.route(
        '/hospital/patient/<int:patient_id>',
        type='http',
        auth='user',
        website=True,
    )
    def patient_detail(self, patient_id, **kwargs):
        Patient = request.env['hospital.patient']

        try:
            patient = Patient.browse(patient_id)
            if not patient.exists():
                return request.not_found()
            patient.check_access('read')
        except AccessError:
            return request.not_found()

        return request.render(
            'hospital_base.patient_website_detail_page',
            {'patient': patient},
        )

    @http.route(
        '/hospital/appointment',
        type='http',
        auth='public',
        website=True,
    )
    def appointment_form(self, **kwargs):
        patients = request.env['hospital.patient'].sudo().search(
            [('state', '=', 'active')],
            order='name',
        )
        doctors = request.env['hospital.doctor'].sudo().search(
            [],
            order='name',
        )

        return request.render(
            'hospital_base.website_appointment_form',
            {
                'patients': patients,
                'doctors': doctors,
            },
        )

    @http.route(
        '/hospital/appointment/submit',
        type='http',
        auth='public',
        methods=['POST'],
        website=True,
    )
    def appointment_submit(self, **post):
        if not post.get('patient_id'):
            return request.render(
                'hospital_base.website_appointment_form',
                {'error': 'Patient is required.'},
            )

        if not post.get('doctor_id'):
            return request.render(
                'hospital_base.website_appointment_form',
                {'error': 'Doctor is required.'},
            )

        if not post.get('appointment_date'):
            return request.render(
                'hospital_base.website_appointment_form',
                {'error': 'Appointment date and time are required.'},
            )

        try:
            patient_id = int(post['patient_id'])
            doctor_id = int(post['doctor_id'])
        except (TypeError, ValueError):
            return request.render(
                'hospital_base.website_appointment_form',
                {'error': 'Invalid patient or doctor.'},
            )

        patient = request.env['hospital.patient'].sudo().browse(patient_id)
        doctor = request.env['hospital.doctor'].sudo().browse(doctor_id)

        if not patient.exists() or not doctor.exists():
            return request.render(
                'hospital_base.website_appointment_form',
                {'error': 'Invalid patient or doctor.'},
            )

        appointment = request.env['hospital.appointment'].sudo().create({
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'appointment_date': post['appointment_date'].replace('T', ' '),
            'notes': post.get('notes'),
        })

        appointment.action_confirm()

        return request.render(
            'hospital_base.appointment_confirmation',
            {'appointment': appointment},
        )
