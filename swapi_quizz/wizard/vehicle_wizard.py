from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import base64
import json
import requests
import logging

class VehicleWizard(models.TransientModel):
    _name= 'swapi.vehicle.wizard'
    _description= 'Wizard: Update vehicles from SWAPI'
    
    def update_vehicles(self):
        
        next_request = 'https://swapi.dev/api/vehicles/'
        while next_request and len(next_request) > 0:
            response = requests.get(next_request)
            json_data = json.loads(response.content)
            
            # read each line of JSON
            for line in json_data:
                if line == 'results':
                    for result in json_data[line]:
                        # find out if this specie already exists in the database
                        vehicle = self.env['swapi.vehicle'].search([('url', '=', result['url'])], limit=1)
                        pilots = result['pilots']
                        films = result['films']
                        if len(vehicle) > 0:
                            # this specie is already in the database, so update it
                            vehicle['name'] = result['name']
                            vehicle['model'] = result['model']
                            vehicle['vehicle_class'] = result['vehicle_class']
                            vehicle['manufacturer'] = result['manufacturer']
                            vehicle['cost_in_credits'] = result['cost_in_credits']
                            vehicle['length'] = result['length']
                            vehicle['crew'] = result['crew']
                            vehicle['passengers'] = result['passengers']
                            vehicle['max_atmosphering_speed'] = result['max_atmosphering_speed']
                            vehicle['cargo_capacity'] = result['cargo_capacity']
                            vehicle['consumables'] = result['consumables']
                            vehicle['url'] = result['url']
                            vehicle['created'] = result['created']
                            vehicle['edited'] = result['edited']
                            
                            for pilot in pilots:
                                pilot_url = self.env['swapi.people'].search([('url','=',pilot)])
                                vehicle['people_ids'] = [(4,pilot_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                vehicle['film_ids'] = [(4,film_url.id)]
                                
                        else:
                            # this specie is not in the database, so insert it

                            new_vehicle = self.env['swapi.vehicle'].create({
                                'name': result['name'],
                                'model': result['model'],
                                'vehicle_class': result['vehicle_class'],
                                'manufacturer': result['manufacturer'],
                                'cost_in_credits': result['cost_in_credits'],
                                'length': result['length'],
                                'crew': result['crew'],
                                'passengers': result['passengers'],
                                'max_atmosphering_speed': result['max_atmosphering_speed'],
                                'cargo_capacity': result['cargo_capacity'],
                                'consumables': result['consumables'],
                                'url': result['url'],
                                'created': result['created'],
                                'edited': result['edited'],
                               
                            })
                            
                            for pilot in pilots:
                                pilot_url = self.env['swapi.people'].search([('url','=',pilot)])
                                new_vehicle['people_ids'] = [(4,pilot_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                new_vehicle['film_ids'] = [(4,film_url.id)]
                        # endif
                    # endfor
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor
        self.env['swapi.vehicle'].search([('name','=','DEMO')]).unlink()
        return True
        
            