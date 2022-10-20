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
    score = fields.Float("Score",readonly=True)
    question_nr = fields.Integer ("Number of question",readonly=True)
    question = fields.Char(string="Question")
    response_specie_ids = fields.Many2many(comodel_name='swapi.specie',
                                   string='Response(s)')
    
    
#     def start_quizz(self):
#         if self.level_id == "Padawan" :
#              if self.theme_id =="Species":
#                 random_number = random.randint()
#                 specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
#                 if specie_random:
#                     self.question = specie_random.name     
    def next_question(self):
         if self.level_id == "Padawan" :
             if self.theme_id =="Species":
                random_number = random.randint()
                specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
                if specie_random:
                    self.question = specie_random.name  
        
    @api.onchange('player_id','theme_id')
    def _onchange_score(self):
        score_player = self.env['swapi.player'].search([('id','=',self.player_id.id)]).score_total
        self.score = score_player
        
    @api.onchange('theme_id')
    def _onchange_theme(self):
        if self.theme_id.id == 1:
            self.question_nr = self.env['swapi.specie'].search_count([])
        if self.theme_id.id == 2:
            self.question_nr = self.env['swapi.planet'].search_count([])
        if self.theme_id.id == 3:
            self.question_nr = self.env['swapi.film'].search_count([])
        if self.theme_id.id == 4:
            self.question_nr = self.env['swapi.people'].search_count([])
        if self.theme_id.id == 5:
            self.question_nr = self.env['swapi.starship'].search_count([])
        if self.theme_id.id == 6:
            self.question_nr = self.env['swapi.vehicle'].search_count([])
