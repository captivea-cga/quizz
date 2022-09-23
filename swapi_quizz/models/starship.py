#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Starship(models.Model):
    
    _name = 'swapi.starship'
    _description = 'Starship Info'
    
    name = fields.Char(string="Name")
    model = fields.Char(string="Model")
    starship_class = fields.Char(string="Starship Class")
    manufacturer = fields.Char(string="Manufacturer")
    cost_in_credits = fields.Char(string="Cost (credits)")
    length = fields.Char(string="Length")
    crew = fields.Char(string="Crew")
    passengers = fields.Char(string="Passengers")
    max_atmosphering_speed = fields.Char(string="Max Atmosphering Speed")
    hyperdrive_rating = fields.Char(string="Hyperdrive Rating")
    mglt = fields.Char(string="Max Megalight travelled in one hour")
    cargo_capacity = fields.Char(string="Cargo Capacity")
    consumables = fields.Char(string="Consumables")
    url = fields.Char(string="ID (URL)")
    created = fields.Char(string="Creation")
    edited = fields.Char(string="Edition")
    people_ids = fields.Many2many(comodel_name='swapi.people',string='Pilots',readonly=True)
    film_ids = fields.Many2many(comodel_name='swapi.film',string='Films',readonly=True)
    
    
    
