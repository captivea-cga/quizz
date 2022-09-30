#  -*- coding: utf-8 -*-

from odoo import models, fields, api
import random

class QuizzWizard(models.TransientModel):
    _name= 'swapi.quizz.wizard'
    _description = 'Wizard: Start a new quizz'
    
    theme_id = fields.Many2one(comodel_name='swapi.theme',
                               string="Theme",
                               required=True)
    
    level_id = fields.Many2one(comodel_name='swapi.level',
                               string="Level",
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
        
        
        
        