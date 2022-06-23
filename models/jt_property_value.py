# -*- coding: utf-8 -*-
import logging
import re
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class PropertyValue(models.Model):
    _name = 'jt.property.value'
    _description = 'Property value'
    _order = 'sequence'
    
    name = fields.Char(string='Name', required=True, translate=True)
    code = fields.Char(string='Code')

    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)
    key_id = fields.Many2one('jt.property.key', string='key')
    css_class = fields.Char(string='CSS class')

    page_id = fields.Many2one('website.page', string='Webpage')

    @api.onchange('name')
    def _check_name(self):
        for rec in self:
            _logger.info("before: %s", rec.code)
            if rec.name:
                if not rec.code:
                    rec.code = re.sub('\s+','-', rec.name)

    @api.onchange('code')
    def _check_code(self):
        for rec in self:
            if rec.code:
                rec.code = re.sub('[^a-z0-9\.\-]*', '', rec.code.lower())