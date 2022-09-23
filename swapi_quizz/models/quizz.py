#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


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
    
    
    @api.model
    def create(self, vals):
        quizz=super().create(vals)
        quizz.name = ""
        
        return quizz
    
        
    
    @api.onchange('player_id','theme_id','level_id')
    def _onchange_name(self):
        self.name = str(self.player_id.name).upper() + " / " + str(self.theme_id.name) + " * " + str(self.level_id.name)
    
