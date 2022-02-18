# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.tools import date_utils

import logging
import json
import requests

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    in_beta = fields.Boolean(default=False, string="In Beta")

    def button_function(self):
        _logger.warning("To Beta clicked")

        partner_json = self.partner_id.read()
        lead_json = self.read()

        data_set = {"partner": partner_json, "lead": lead_json}

        _logger.warning("Partner id"+ json.dumps(data_set, default=date_utils.json_default))

        response = requests.post('http://127.0.0.1:5000/create/', data_set)
        response_body = json.loads(response.json())

        if response.status_code == 201 and response_body['status'] == "success":
            self.in_beta = True
            self.partner_id.in_beta = True
            _logger.warning("CrmLead: " + response.json())
        else:
            _logger.error("CrmLead: " + response.json())
            return {
                'warning': {'title': 'Warning',
                            'message': 'Failed to send Lead data to Beta', },
            }


