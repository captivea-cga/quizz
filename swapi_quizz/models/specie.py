#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Specie(models.Model):
    
    _name = 'swapi.specie'
    _description = 'Specie Info'
    
    name = fields.Char(string="Name")
    classification = fields.Char(string="Classification")
    designation = fields.Char(string="Designation")
    average_height = fields.Char(string="Height (average)")
    average_lifespan = fields.Char(string="Lifespan (average)")
    eye_colors = fields.Char(string="Color of eye")
    hair_colors = fields.Char(string="Color of hair")
    skin_colors = fields.Char(string="Color of skin")
    language = fields.Char(string="Language")
    url = fields.Char(string="ID (URL)")
    created = fields.Char(string="Creation")
    edited = fields.Char(string="Edition")
    # planet_ids = fields.Many2many(comodel_name='swapi.planet',string='Planets',readonly=True)
    # people_ids = fields.Many2many(comodel_name='swapi.people',string='People',readonly=True)
    # film_ids = fields.Many2many(comodel_name='swapi.film',string='Films',readonly=True)
    homeworld = fields.Char()
    
    