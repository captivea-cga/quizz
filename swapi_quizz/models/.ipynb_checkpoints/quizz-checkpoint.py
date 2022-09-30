#  -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import random

class Quizz(models.Model):
    
    _name = 'swapi.quizz'
    _description = 'Quizz Info'
    
    name = fields.Char(string="Name")
    # player_id = fields.Many2one(comodel_name='swapi.player',
    #                                    string='Player',
    #                             )
    theme_id = fields.Many2one(comodel_name='swapi.theme',
                                       string='Theme',
                                       required=True)
    level_id = fields.Many2one(comodel_name='swapi.level',
                                       string='Level',
                                       required=True)
    
#     states = fields.Text(string="Question")
#     proposition = fields.Char(string="Proposition")
#     start_quizz = fields.Boolean(string="Start_quizz", default=False)
    # @api.onchange('player_id','theme_id','level_id')
    # def _onchange_name(self):
    #     self.name = str(self.player_id.name).upper() + " / " + str(self.theme_id.name) + " * " + str(self.level_id.name)
    #     if self.level_id.name == "Padawan" :
    #         if self.theme_id.name =="Species":
    #             self.states = "Dans quel(s) film(s) peut-on voir cette espèce ?"
    #         else:
    #             self.states = "Il n'y a pas encore de question pour ce thème/niveau"
    def start_quizz_species_padawan(self):
#         self.start_quizz = True
        specie_count = self.env['swapi.specie'].search_count([])
        random_number = random.randint(1,specie_count)
        specie_random = self.env['swapi.specie'].search([('id',"=",random_number)])
#         self.states = self.env['swapi.question_template'].search(["&",('theme_id.id','=',self.theme_id.id),('level_id.id','=',self.level_id.id)]).question_template
#         self.proposition = str(specie_random.name)
        # raise UserError(str(specie_random.name))
                
    # Faire une fonction pour créer les quizz (tous) et faire un boutton dans la vue liste : Create All Quizz
    def create_all_quizz(self):
        raise UserError("All Quizz")           
                     