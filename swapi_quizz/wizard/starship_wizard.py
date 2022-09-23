from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import base64
import json
import requests
import logging

class StarshipWizard(models.TransientModel):
    _name= 'swapi.starship.wizard'
    _description= 'Wizard: Update starships from SWAPI'
    
    def update_starships(self):
        
        next_request = 'https://swapi.dev/api/starships/'
        while next_request and len(next_request) > 0:
            response = requests.get(next_request)
            json_data = json.loads(response.content)
            
            # read each line of JSON
            for line in json_data:
                if line == 'results':
                    for result in json_data[line]:
                        # find out if this specie already exists in the database
                        starship = self.env['swapi.starship'].search([('url', '=', result['url'])], limit=1)
                        pilots = result['pilots']
                        films = result['films']
                        if len(starship) > 0:
                            # this specie is already in the database, so update it
                            starship['name'] = result['name']
                            starship['model'] = result['model']
                            starship['starship_class'] = result['starship_class']
                            starship['manufacturer'] = result['manufacturer']
                            starship['cost_in_credits'] = result['cost_in_credits']
                            starship['length'] = result['length']
                            starship['crew'] = result['crew']
                            starship['passengers'] = result['passengers']
                            starship['max_atmosphering_speed'] = result['max_atmosphering_speed']
                            starship['hyperdrive_rating'] = result['hyperdrive_rating']
                            starship['mglt'] = result['MGLT']
                            starship['cargo_capacity'] = result['cargo_capacity']
                            starship['consumables'] = result['consumables']
                            starship['url'] = result['url']
                            starship['created'] = result['created']
                            starship['edited'] = result['edited']
                            
                            for pilot in pilots:
                                pilot_url = self.env['swapi.people'].search([('url','=',pilot)])
                                starship['people_ids'] = [(4,pilot_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                starship['film_ids'] = [(4,film_url.id)]
                        else:
                            # this specie is not in the database, so insert it

                            new_starship = self.env['swapi.starship'].create({
                                'name': result['name'],
                                'model': result['model'],
                                'starship_class': result['starship_class'],
                                'manufacturer': result['manufacturer'],
                                'cost_in_credits': result['cost_in_credits'],
                                'length': result['length'],
                                'crew': result['crew'],
                                'passengers': result['passengers'],
                                'max_atmosphering_speed': result['max_atmosphering_speed'],
                                'hyperdrive_rating': result['hyperdrive_rating'],
                                'mglt': result['MGLT'],
                                'cargo_capacity': result['cargo_capacity'],
                                'consumables': result['consumables'],
                                'url': result['url'],
                                'created': result['created'],
                                'edited': result['edited'],
                               
                            })
                            
                            for pilot in pilots:
                                pilot_url = self.env['swapi.people'].search([('url','=',pilot)])
                                new_starship['people_ids'] = [(4,pilot_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                new_starship['film_ids'] = [(4,film_url.id)]
                        # endif
                    # endfor
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor
        self.env['swapi.starship'].search([('name','=','DEMO')]).unlink()
        return True
        
            