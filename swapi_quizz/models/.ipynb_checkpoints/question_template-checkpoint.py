#  -*- coding: utf-8 -*-


from email.policy import default
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import random

class QuestionTemplate(models.Model):
    
    _name = 'swapi.question_template'
    _description = 'Template for questions of quizz'
    
    theme_id = fields.Many2one(comodel_name='swapi.theme',
                                       string='Theme',
                                       required=True)
    level_id = fields.Many2one(comodel_name='swapi.level',
                                       string='Level',
                                       required=True)
    question_template = fields.Text(string="Question template")
    
    
       
                     