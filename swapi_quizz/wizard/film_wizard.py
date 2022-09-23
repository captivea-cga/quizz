from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import base64
import json
import requests
import logging

class FilmWizard(models.TransientModel):
    _name= 'swapi.film.wizard'
    _description= 'Wizard: Update films from SWAPI'
    
    def update_films(self):
        
        next_request = 'https://swapi.dev/api/films/'
        while next_request and len(next_request) > 0:
            response = requests.get(next_request)
            json_data = json.loads(response.content)
            
            # read each line of JSON
            for line in json_data:
                if line == 'results':
                    for result in json_data[line]:
                        # find out if this specie already exists in the database
                        film = self.env['swapi.film'].search([('url', '=', result['url'])], limit=1)
                        species = result['species']
                        starships = result['starships']
                        vehicles = result['vehicles']
                        characters = result['characters']
                        planets = result['planets']
                        if len(film) > 0:
                            # this specie is already in the database, so update it
                            film['title'] = result['title']
                            film['episode_id'] = result['episode_id']
                            film['opening_crawl'] = result['opening_crawl']
                            film['director'] = result['director']
                            film['producer'] = result['producer']
                            film['release_date'] = result['release_date']
                            film['url'] = result['url']
                            film['created'] = result['created']
                            film['edited'] = result['edited']
                            
                            for specie in species:
                                specie_url = self.env['swapi.specie'].search([('url','=',specie)])
                                film['specie_ids'] = [(4,specie_url.id)]
                            for starship in starships:
                                starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                film['starship_ids'] = [(4,starship_url.id)]
                            for vehicle in vehicles:
                                vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                film['vehicle_ids'] = [(4,vehicle_url.id)]
                            for character in characters:
                                people_url = self.env['swapi.people'].search([('url','=',character)])
                                film['people_ids'] = [(4,people_url.id)]
                            for planet in planets:
                                planet_url = self.env['swapi.planet'].search([('url','=',planet)])
                                film['planet_ids'] = [(4,planet_url.id)]
                            
                        else:
                            # this specie is not in the database, so insert it
                            
                            new_film = self.env['swapi.film'].create({
                                'title': result['title'],
                                'episode_id': result['episode_id'],
                                'opening_crawl': result['opening_crawl'],
                                'director': result['director'],
                                'producer': result['producer'],
                                'release_date': result['release_date'],
                                'url': result['url'],
                                'created': result['created'],
                                'edited': result['edited'],
                                })
                            for specie in species:
                                specie_url = self.env['swapi.specie'].search([('url','=',specie)])
                                new_film['specie_ids'] = [(4,specie_url.id)]
                            for starship in starships:
                                starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                new_film['starship_ids'] = [(4,starship_url.id)]
                            for vehicle in vehicles:
                                vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                new_film['vehicle_ids'] = [(4,vehicle_url.id)]
                            for character in characters:
                                people_url = self.env['swapi.people'].search([('url','=',character)])
                                new_film['people_ids'] = [(4,people_url.id)]
                            for planet in planets:
                                planet_url = self.env['swapi.planet'].search([('url','=',planet)])
                                new_film['planet_ids'] = [(4,planet_url.id)]
                        # endif
                    # endfor
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor

        self.env['swapi.film'].search([('title','=','DEMO')]).unlink()
        return True
        
       