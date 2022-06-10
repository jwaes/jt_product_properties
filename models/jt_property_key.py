# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class PropertyKey(models.Model):
    _name = 'jt.property.key'
    _description = 'Property key'
    _order = 'code, sequence'

    name = fields.Char(string='Key name', required=True, translate=True)
    sequence = fields.Integer(
        'Sequence', help="Determine the display order", index=True)
    code = fields.Char(string="Key code", required=True)
    property_type = fields.Selection([
        ('selection', 'Selection'),
        ('free_text', 'Free text'),
        ('html', 'HTML')],
        string='Type',
        default='selection',
        required=True)

    value_ids = fields.One2many(
        'jt.property.value', 'key_id', string='Property values')

    behavior = fields.Selection([
        ('replace', 'Replace'),
        ('add', 'Add')], 
        string='Behavior',
        default='replace',
        required=True)
