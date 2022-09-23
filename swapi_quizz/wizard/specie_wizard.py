from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import base64
import json
import requests
import logging

class SpecieWizard(models.TransientModel):
    _name= 'swapi.specie.wizard'
    _description= 'Wizard: Update species from SWAPI'
    
    def update_species(self):
        
        next_request = 'https://swapi.dev/api/species/'
        while next_request and len(next_request) > 0:
            response = requests.get(next_request)
            json_data = json.loads(response.content)
            
            # read each line of JSON
            for line in json_data:
                if line == 'results':
                    for result in json_data[line]:
                        # find out if this specie already exists in the database
                        specie = self.env['swapi.specie'].search([('url', '=', result['url'])], limit=1)
                        films = result['films']
#                         planet = result['homeworld']
                        people = result['people']
                        
                        if len(specie) > 0:
                            # this specie is already in the database, so update it
                            specie['name'] = result['name']
                            specie['classification'] = result['classification']
                            specie['designation'] = result['designation']
                            specie['average_height'] = result['average_height']
                            specie['average_lifespan'] = result['average_lifespan']
                            specie['eye_colors'] = result['eye_colors']
                            specie['skin_colors'] = result['skin_colors']
                            specie['hair_colors'] = result['hair_colors']
                            specie['language'] = result['language']
                            specie['url'] = result['url']
                            specie['created'] = result['created']
                            specie['edited'] = result['edited']
                            specie['homeworld'] = result['homeworld']
                            
                            
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                specie['film_ids'] = [(4,film_url.id)]
                            
                            
                            
                            for character in people:
                                character_url = self.env['swapi.people'].search([('url','=',character)])
                                specie['people_ids'] = [(4,character_url.id)]
                                
                            planet = self.env['swapi.planet'].search([('url','=',specie['homeworld'])])
                            specie['planet_ids'] = planet
                            
                        else:
                            # this specie is not in the database, so insert it

                            new_specie = self.env['swapi.specie'].create({
                                'name': result['name'],
                                'classification':result['classification'],
                                'designation':result['designation'],
                                'average_height':result['average_height'],
                                'average_lifespan':result['average_lifespan'],
                                'eye_colors':result['eye_colors'],
                                'skin_colors':result['skin_colors'],
                                'hair_colors':result['hair_colors'],
                                'language':result['language'],
                                'url':result['url'],
                                'created':result['created'],
                                'edited':result['edited'],
                                'homeworld':result['homeworld']
                            })
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                new_specie['film_ids'] = [(4,film_url.id)]
                            for character in people:
                                people_url = self.env['swapi.people'].search([('url','=',character)])
                                new_specie['people_ids'] = [(4,people_url.id)]
                            planet = self.env['swapi.planet'].search([('url','=',specie['homeworld'])])
                            new_specie['planet_ids'] = planet
                        # endif
                    # endfor
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor
        self.env['swapi.specie'].search([('name','=','DEMO')]).unlink()
        return True
        
            