#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Film(models.Model):
    
    _name = 'swapi.film'
    _description = 'Film Info'
    
    
    name = fields.Char(string="Title")
    episode_id = fields.Integer(string="Episode")
    opening_crawl = fields.Text(string="Opening crawl text")
    director = fields.Char(string="Director")
    producer = fields.Char(string="Producer")
    release_date = fields.Date(string="Date of release")
    url = fields.Char(string="ID (URL)")
    created = fields.Char(string="Creation")
    edited = fields.Char(string="Edition")
    specie_ids = fields.Many2many(comodel_name='swapi.specie',string='Species',readonly=True)
    starship_ids = fields.Many2many(comodel_name='swapi.starship',string='Starships',readonly=True)
    vehicle_ids = fields.Many2many(comodel_name='swapi.vehicle',string='Vehicles',readonly=True)
    people_ids = fields.Many2many(comodel_name='swapi.people',string='People',readonly=True)
    planet_ids = fields.Many2many(comodel_name='swapi.planet',string='Planet',readonly=True)
    
    
