# -*- coding: utf-8 -*-
import json
import logging
import werkzeug.utils

from odoo import http
from odoo.http import request
from odoo.osv.expression import AND
from odoo.tools import convert

_logger = logging.getLogger(__name__)


class DentalController(http.Controller):

    @http.route(['/dental/web'], type='http', auth='user')
    def pdental_web(self, patient_id=False, **k):
        session_info = request.env['ir.http'].session_info()
        context = {
            'session_info': session_info,
            'patient_id': int(patient_id),
            'user_id': request.env.user.id,
        }
        response = request.render('ksc_dental.index', context)
        response.headers['Cache-Control'] = 'no-store'
        return response
