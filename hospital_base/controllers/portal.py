from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal


class HospitalPortal(portal.CustomerPortal):

    @http.route(
        '/my/appointments',
        type='http',
        auth='user',
        website=True,
    )
    def portal_my_appointments(self, **kwargs):
        patient = request.env['hospital.patient'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1,
        )

        appointments = request.env['hospital.appointment'].search(
            [('patient_id', '=', patient.id)]
        ) if patient else request.env['hospital.appointment']

        return request.render(
            'hospital_base.portal_my_appointments',
            {'appointments': appointments},
        )

    @http.route(
        '/my/appointments/<int:appointment_id>',
        type='http',
        auth='user',
        website=True,
    )
    def portal_appointment_detail(self, appointment_id, **kwargs):
        patient = request.env['hospital.patient'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1,
        )

        appointment = request.env['hospital.appointment'].search([
            ('id', '=', appointment_id),
            ('patient_id', '=', patient.id),
        ]) if patient else request.env['hospital.appointment']

        if not appointment:
            return request.not_found()

        return request.render(
            'hospital_base.portal_appointment_detail',
            {'appointment': appointment},
        )