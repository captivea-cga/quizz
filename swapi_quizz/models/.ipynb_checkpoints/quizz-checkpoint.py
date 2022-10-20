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
    score = fields.Integer("Score",readonly=True)
    score_question = fields.Integer("Score question",readonly=True)
    question_nr = fields.Integer ("Number of question",readonly=True)
    question = fields.Char(string="Question")
    response_film_ids = fields.Many2many('swapi.film',
                                   string='Response(s)')
    is_quizz_started = fields.Boolean(string="Start_quizz",default=False)
    question_spinner = fields.Integer(string="Question nr")
    question_template = fields.Char()            
    proposal_nr = fields.Integer(string="Proposal nr")
    test = fields.Char()
    random_number = fields.Integer(string="Random Number")
    def start_quizz(self):
        self.score_question = 0
        self.is_quizz_started = True
        question_nr = self.env['swapi.specie'].search_count([])
        self.question_nr = question_nr
        random_number = random.randint(1,question_nr)
        self.random_number = random_number 
        specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
        
        self.question_spinner = 1
        question_template = self.env['swapi.question_template'].search(["&",('theme_id.id','=',self.theme_id.id),('level_id.id','=',self.level_id.id)])
        self.question_template = question_template.question_template
        self.question = specie_random.name
        self.score = 0
        self.score_question = 0
        proposals = specie_random.film_ids
        self.proposal_nr = len(proposals)
        self.response_film_ids = False
   
    def next_question(self):
        random_number = random.randint(1,self.question_nr)
        self.random_number = random_number
        specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
#         random_number = 1
#         specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
        #         SCORE
        
#         proposals_max = self.env['swapi.film'].search_count([])
#         responses = self.response_film_ids
        solutions = specie_random.film_ids
#         solution_nr = len(solutions)
#         raise UserError("solution_nr = " + str(solution_nr) + " * nb réponses = " + str(len(responses)))
        # 1 - Pas de réponse => score = 0
#         if len(responses) == 0:
#             self.score_question = 0
#             self.test = "1 - Pas de réponse => score = 0"
        # 2 - si il y a 6 réponses (tous les films) et que le nombre de réponses n'est pas 6 , score - 5
#         proposals_max = self.env['swapi.film'].search_count([])
#         responses = self.response_film_ids   
#             raise UserError("solution_nr = " + str(solution_nr) + " * nb réponses = " + str(len(responses)))
#         elif len(responses) == proposals_max :
            
#             solutions = specie_random.film_ids
#             solution_nr = len(solutions)
           
#             self.test = "solution_nr = " + str(solution_nr) + " * nb réponses = " + str(len(responses))
#             if solution_nr != len(responses):
#                 raise UserError("nombre de réponses = " + str(solution_nr) + " * nb réponses = " + str(len(responses)))
#                 self.score_question = -5
#                 self.test = "2 - si il y a 6 réponses (tous les films) et que le nombre de réponses n'est pas 6 , score - 5"  
#         # 3 - si tout est bon : score + 5
#         # 4 - si une des réponses est bonne : score +1 
#         # 5 - si une des réponses est fausse : score -1
#         elif len(responses) == solution_nr:
#             good_responses_nr = 0
#             for response in responses:
#                 if response in solutions:
#                     good_responses_nr +=1
#                     raise UserError(response)
#             if good_responses_nr == len(responses):
#                 self.score_question = 5
#                 self.test = "3 - si tout est bon : score + 5"
#             if good_responses_nr != len(responses):
#                 self.score_question = 2*good_responses_nr - solution_nr
#                 self.test = "4 et 5"
                
                
#         self.score += self.score_question
        
#         self.response_film_ids = False
        
        #         affichage du bouton start quizz
        
        if self.question_spinner == self.question_nr :
            self.is_quizz_started = False
#             question au hasard
        
        
        self.question = specie_random.name
        self.question_spinner +=1
#         affichage du nombre de réponses si level = Padawan
        if self.level_id.id == 1 :
#             proposals = specie_random.film_ids
            self.proposal_nr = len(solutions)
            
    
        
    def submit(self):
        proposals_max = self.env['swapi.film'].search_count([])
        responses = self.response_film_ids
        responses_nr = len(responses)
        solutions = self.env['swapi.specie'].search([('name','=',self.question)]).film_ids
        solutions_nr = len(solutions)
#         raise UserError("solution_nr = " + str(solution_nr) + " * nb réponses = " + str(len(responses)))
        # 1 - Pas de réponse => score = 0
        if responses_nr == 0:
            self.score_question = 0
            self.test = "1 - Pas de réponse => score = 0"
        self.score += self.score_question    
    def reset_quizz(self):
        self.question_spinner = 0
        self.is_quizz_started = False
        self.score = 0             
        self.score_question = 0