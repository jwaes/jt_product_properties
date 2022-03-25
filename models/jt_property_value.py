# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class PropertyValue(models.Model):
    _name = 'jt.property.value'
    _description = 'Property value'
    _order = 'sequence'
    
    name = fields.Char(string='Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)
    key_id = fields.Many2one('jt.property.key', string='key')

    css_class = fields.Char(string='CSS class')

    page_id = fields.Many2one('website.page', string='Webpage')