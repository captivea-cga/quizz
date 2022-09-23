#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Theme(models.Model):
    
    _name = 'swapi.theme'
    _description = 'Theme Info'
    
    
    name = fields.Char(string="Name")

    
    
    
