#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import random

class Quizz(models.Model):
    
    _name = 'swapi.quizz'
    _description = 'Quizz Info'
    
    name = fields.Char(string="Name")
    player_id = fields.Many2one(comodel_name='swapi.player',
                                       string='Player',
                                       required=True)
    theme_id = fields.Many2one(comodel_name='swapi.theme',
                                       string='Theme',
                                       required=True)
    level_id = fields.Many2one(comodel_name='swapi.level',
                                       string='Level',
                                       required=True)
    
    
    @api.onchange('player_id','theme_id','level_id')
    def _onchange_name(self):
        self.name = str(self.player_id.name).upper() + " / " + str(self.theme_id.name) + " * " + str(self.level_id.name)
    
    def start_quizz(self):
        if self.level_id == "Padawan" :
             if self.theme_id =="Species":
                random_number = random.randint()
                specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
                if specie_random:
                    self.question = specie_random.name     