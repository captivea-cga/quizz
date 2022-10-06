#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import random

class Quizz(models.Model):
    
    _name = 'swapi.quizz'
    _description = 'Quizz Info'
    
    name = fields.Char(string="Name")
    
    theme_id = fields.Many2one(comodel_name='swapi.theme',
                                       string='Theme',
                                       required=True, readonly=True)
    level_id = fields.Many2one(comodel_name='swapi.level',
                                       string='Level',
                                       required=True, readonly=True)
    
    player_id = fields.Many2one(comodel_name='swapi.player',
                                string='Player')
    score = fields.Float("Score",readonly=True)
    question_nr = fields.Integer ("Number of question",readonly=True)
    question = fields.Char(string="Question")
    response_specie_ids = fields.Many2many(comodel_name='swapi.specie',
                                   string='Response(s)')
    is_quizz_started = fields.Boolean(string="Start_quizz",default=False)
    question_spinner = fields.Integer(string="Question nr")
    question_template = fields.Char()            
    proposal_nr = fields.Integer(string="Proposal nr")
    
    def start_quizz(self):
        self.is_quizz_started = True
        question_nr = self.env['swapi.specie'].search_count([])
        self.question_nr = question_nr
        random_number = random.randint(1,question_nr)
        specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
        
        self.question_spinner = 1
        question_template = self.env['swapi.question_template'].search(["&",('theme_id.id','=',self.theme_id.id),('level_id.id','=',self.level_id.id)])
        self.question_template = question_template.question_template
        self.question = specie_random.name
    
    def next_question(self):
        if self.question_spinner == self.question_nr :
            self.is_quizz_started = False
        random_number = random.randint(1,self.question_nr)
        specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
        self.question = specie_random.name
        self.question_spinner +=1
        if self.level_id.id == 1 :
           self.proposal_nr = specie_random.film_ids.count 
        
#         if self.level_id == "Padawan" :
#              if self.theme_id =="Species":
#                 random_number = random.randint()
#                 specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
#                 if specie_random:
#                     self.question = specie_random.name            
                     