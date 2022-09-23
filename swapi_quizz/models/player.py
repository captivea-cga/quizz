#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Player(models.Model):
    
    _name = 'swapi.player'
    _description = 'Player Info'
    
    
    pseudo = fields.Char(string="Pseudo")
    score_total = fields.Float(string="Score STAR WARS")
    score_species = fields.Float(string="Score Species")
    score_planets = fields.Float(string="Score Planets")
    score_films = fields.Float(string="Score Films")
    score_people = fields.Float(string="Score People")
    score_starships = fields.Float(string="Score Starships")
    score_vehicles = fields.Float(string="Score Vehicles")
    # level_id
    # quizz_ids
    
    
    
