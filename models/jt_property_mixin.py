# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class PropertyMixin(models.AbstractModel):
    # _name = 'jt.property.mixin'
    _description = 'Adds property fields'

    # property_kv_ids = fields.One2many('jt.property.kv', string='Property fields')

    proppy = fields.Char('proppy')
    