#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class Planet(models.Model):
    
    _name = 'swapi.planet'
    _description = 'Planet Info'
    
    name = fields.Char(string="Name")
    diameter = fields.Char(string="Diameter")
    rotation_period = fields.Char(string="Period of rotation")
    orbital_period = fields.Char(string="Period of orbital")
    gravity = fields.Char(string="Gravity")
    population = fields.Char(string="Population")
    climate = fields.Char(string="Climate")
    terrain = fields.Char(string="Terrain")
    surface_water = fields.Char(string="Surface of water")
    url = fields.Char(string="ID (URL)")
    created = fields.Char(string="Creation")
    edited = fields.Char(string="Edition")
    people_ids = fields.Many2many(comodel_name='swapi.people',string='Residents',readonly=True)
    film_ids = fields.Many2many(comodel_name='swapi.film',string='Films',readonly=True)
    