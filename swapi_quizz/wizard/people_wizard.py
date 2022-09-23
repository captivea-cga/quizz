from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import base64
import json
import requests
import logging

class PeopleWizard(models.TransientModel):
    _name= 'swapi.people.wizard'
    _description= 'Wizard: Update people from SWAPI'
    
    def update_people(self):
        
        next_request = 'https://swapi.dev/api/people/'
        while next_request and len(next_request) > 0:
            response = requests.get(next_request)
            json_data = json.loads(response.content)
            
            # read each line of JSON
            for line in json_data:
                if line == 'results':
                    for result in json_data[line]:
                        # find out if this specie already exists in the database
                        people = self.env['swapi.people'].search([('url', '=', result['url'])], limit=1)
                        films = result['films']
                        species = result['species']
                        starships = result['starships']
                        vehicles = result['vehicles']
                        if len(people) > 0:
                            # this specie is already in the database, so update it
                            people['name'] = result['name']
                            people['birth_year'] = result['birth_year']
                            people['eye_color'] = result['eye_color']
                            people['gender'] = result['gender']
                            people['hair_color'] = result['hair_color']
                            people['height'] = result['height']
                            people['mass'] = result['mass']
                            people['skin_color'] = result['skin_color']
                            people['url'] = result['url']
                            people['created'] = result['created']
                            people['edited'] = result['edited']
                            people['homeworld'] = result['homeworld']
                            
                            for specie in species:
                                specie_url = self.env['swapi.specie'].search([('url','=',specie)])
                                people['specie_ids'] = [(4,specie_url.id)]
                            for starship in starships:
                                starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                people['starship_ids'] = [(4,starship_url.id)]
                            for vehicle in vehicles:
                                vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                people['vehicle_ids'] = [(4,vehicle_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                people['film_ids'] = [(4,film_url.id)]
                            planet = self.env['swapi.planet'].search([('url','=',people['homeworld'])])
                            people['planet_ids'] = planet
                        else:
                            # this specie is not in the database, so insert it

                            new_people = self.env['swapi.people'].create({
                                'name': result['name'],
                                'birth_year': result['birth_year'],
                                'eye_color': result['eye_color'],
                                'gender': result['gender'],
                                'hair_color': result['hair_color'],
                                'height': result['height'],
                                'mass': result['mass'],
                                'skin_color': result['skin_color'],
                                'url': result['url'],
                                'created': result['created'],
                                'edited': result['edited'],
                                
                            })
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                new_people['film_ids'] = [(4,film_url.id)]
                            for specie in species:
                                specie_url = self.env['swapi.specie'].search([('url','=',specie)])
                                new_people['specie_ids'] = [(4,specie_url.id)]
                            for starship in starships:
                                starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                new_people['starship_ids'] = [(4,starship_url.id)]
                            for vehicle in vehicles:
                                vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                new_people['vehicle_ids'] = [(4,vehicle_url.id)]
                            
                            planet = self.env['swapi.planet'].search([('url','=',specie['homeworld'])])
                            new_people['planet_ids'] = planet
                        # endif
                    # endfor
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor

        self.env['swapi.people'].search([('name','=','DEMO')]).unlink()
        return True
        
