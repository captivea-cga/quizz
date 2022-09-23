#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class People(models.Model):
    
    _name = 'swapi.people'
    _description = 'People Info'
    
    name = fields.Char(string="Name")
    birth_year = fields.Char(string="Year of birth")
    eye_color = fields.Char(string="Color of eye")
    gender = fields.Char(string="Gender")
    hair_color = fields.Char(string="Color of hair")
    height = fields.Char(string="Height")
    mass = fields.Char(string="Mass")
    skin_color = fields.Char(string="Color of skin")
    url = fields.Char(string="ID (URL)")
    created = fields.Char(string="Creation")
    edited = fields.Char(string="Edition")
    planet_ids = fields.Many2many(comodel_name='swapi.planet',string='Planets',readonly=True)
    specie_ids = fields.Many2many(comodel_name='swapi.specie',string='Species',readonly=True)
    film_ids = fields.Many2many(comodel_name='swapi.film',string='Films',readonly=True)
    starship_ids = fields.Many2many(comodel_name='swapi.starship',string='Starships',readonly=True)
    vehicle_ids = fields.Many2many(comodel_name='swapi.vehicle',string='Vehicles',readonly=True)
    homeworld = fields.Char()
    
    
