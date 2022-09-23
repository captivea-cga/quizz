from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import base64
import json
import requests
import logging

class PlanetWizard(models.TransientModel):
    _name= 'swapi.planet.wizard'
    _description= 'Wizard: Update planets from SWAPI'
    
    def update_planets(self):
        
        next_request = 'https://swapi.dev/api/planets/'
        while next_request and len(next_request) > 0:
            response = requests.get(next_request)
            json_data = json.loads(response.content)
            
            # read each line of JSON
            for line in json_data:
                if line == 'results':
                    for result in json_data[line]:
                        # find out if this specie already exists in the database
                        planet = self.env['swapi.planet'].search([('url', '=', result['url'])], limit=1)
                        residents = result['residents']
                        films = result['films']
                        if len(planet) > 0:
                            # this specie is already in the database, so update it
                            planet['name'] = result['name']
                            planet['diameter'] = result['diameter']
                            planet['rotation_period'] = result['rotation_period']
                            planet['orbital_period'] = result['orbital_period']
                            planet['gravity'] = result['gravity']
                            planet['population'] = result['population']
                            planet['climate'] = result['climate']
                            planet['terrain'] = result['terrain']
                            planet['surface_water'] = result['surface_water']
                            planet['url'] = result['url']
                            planet['created'] = result['created']
                            planet['edited'] = result['edited']
                            
                            for resident in residents:
                                resident_url = self.env['swapi.people'].search([('url','=',resident)])
                                planet['people_ids'] = [(4,resident_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                planet['film_ids'] = [(4,film_url.id)]
                        else:
                            # this specie is not in the database, so insert it

                            new_planet = self.env['swapi.planet'].create({
                                'name': result['name'],
                                'diameter':result['diameter'],
                                'rotation_period':result['rotation_period'],
                                'orbital_period':result['orbital_period'],
                                'gravity':result['gravity'],
                                'population':result['population'],
                                'climate':result['climate'],
                                'terrain':result['terrain'],
                                'surface_water':result['surface_water'],
                                'url':result['url'],
                                'created':result['created'],
                                'edited':result['edited']
                            })
                            for resident in residents:
                                resident_url = self.env['swapi.people'].search([('url','=',resident)])
                                new_planet['people_ids'] = [(4,resident_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                new_planet['film_ids'] = [(4,film_url.id)]
                        # endif
                    # endfor
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor

        self.env['swapi.planet'].search([('name','=','DEMO')]).unlink()
        return True
        
