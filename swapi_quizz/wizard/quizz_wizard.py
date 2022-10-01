#  -*- coding: utf-8 -*-

from odoo import models, fields, api
import random

class QuizzWizard(models.TransientModel):
    _name= 'swapi.quizz.wizard'
    _description = 'Wizard: Start a new quizz'
    
    def _default_theme(self):
        return self.env['swapi.theme'].browse(self._context.get('active_id'))
    
    def _default_level(self):
        return self.env['swapi.level'].browse(self._context.get('active_id'))
    
    theme_id = fields.Many2one(comodel_name='swapi.theme',
                               string="Theme",
                               default=_default_theme,
                               readonly=True,
                               required=True)
     
    level_id = fields.Many2one(comodel_name='swapi.level',
                               string="Level",
                               default=_default_level,
                               readonly=True,
                               required=True)    
    
    player_id = fields.Many2one(comodel_name='swapi.player',
                                string='Player',
                                required=True)
    question = fields.Char(string="Question")
    response_specie_ids = fields.Many2many(comodel_name='swapi.specie',
                                   string='Response(s)')
    
    def start_quizz(self):
        if self.level_id == "Padawan" :
             if self.theme_id =="Species":
                random_number = random.randint()
                specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
                if specie_random:
                    self.question = specie_random.name     
        
        
        
        