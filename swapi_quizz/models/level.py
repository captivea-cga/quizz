#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Level(models.Model):
    
    _name = 'swapi.level'
    _description = 'Level Info'
    
    
    name = fields.Char(string="Name")
    limit_down = fields.Float(string="Limit DOWN")
    limit_up = fields.Float(string="Limit UP")
    
    

    
    
    
