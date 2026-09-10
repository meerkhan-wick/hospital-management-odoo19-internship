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
