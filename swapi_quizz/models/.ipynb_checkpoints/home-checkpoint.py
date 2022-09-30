#  -*- coding: utf-8 -*-



from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import base64
import json
import requests
import logging

class Home(models.Model):
    
    _name = 'swapi.home'
    _description = 'Home'
    
    name = fields.Char(string="Name")
    last_update = fields.Datetime(string="Last update")
    
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
                        planet = result['homeworld']
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
                                if film_url:
                                    specie['film_ids'] = [(4,film_url.id)]
                            
                            
                            
                            for character in people:
                                character_url = self.env['swapi.people'].search([('url','=',character)])
                                if character_url:
                                    specie['people_ids'] = [(4,character_url.id)]
                                
                            planet = self.env['swapi.planet'].search([('url','=',specie['homeworld'])])
                            if planet:
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
                                if film_url:
                                    new_specie['film_ids'] = [(4,film_url.id)]
                            for character in people:
                                people_url = self.env['swapi.people'].search([('url','=',character)])
                                if people_url:
                                    new_specie['people_ids'] = [(4,people_url.id)]
                            planet = self.env['swapi.planet'].search([('url','=',specie['homeworld'])])
                            if planet:
                                new_specie['planet_ids'] = planet
                    
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor
        self.env['swapi.specie'].search([('name','=','DEMO')]).unlink()
        to_update = self.env['swapi.home'].search([('name','=','SPECIES')])
        to_update['last_update'] = datetime.now()
#         return{
#             'res_model': 'swapi.specie',
#             'type': 'ir.actions.act_window',
#             'field_parent':'Species',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.specie_view_list'
#         }
        return True
    
#     UPDATE PLANETS
    
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
                                if resident_url:
                                    planet['people_ids'] = [(4,resident_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                if film_url:
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
                                if resident_url:
                                    new_planet['people_ids'] = [(4,resident_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                if film_url:
                                    new_planet['film_ids'] = [(4,film_url.id)]
                        # endif
                    # endfor
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor

        self.env['swapi.planet'].search([('name','=','DEMO')]).unlink()
        to_update = self.env['swapi.home'].search([('name','=','PLANETS')])
        to_update['last_update'] = datetime.now()
#         return{
#             'res_model': 'swapi.planet',
#             'type': 'ir.actions.act_window',
#             'field_parent':'Planets',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.planet_view_list'
#         }
        return True
    
#     UPDATE FILMS    
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
                                if specie_url:
                                    film['specie_ids'] = [(4,specie_url.id)]
                            for starship in starships:
                                starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                if starship_url:
                                    film['starship_ids'] = [(4,starship_url.id)]
                            for vehicle in vehicles:
                                vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                if vehicle_url:
                                    film['vehicle_ids'] = [(4,vehicle_url.id)]
                            for character in characters:
                                people_url = self.env['swapi.people'].search([('url','=',character)])
                                if people_url:
                                    film['people_ids'] = [(4,people_url.id)]
                            for planet in planets:
                                planet_url = self.env['swapi.planet'].search([('url','=',planet)])
                                if planet_url:
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
                                if specie_url:
                                    new_film['specie_ids'] = [(4,specie_url.id)]
                            for starship in starships:
                                starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                if starship_url:
                                    new_film['starship_ids'] = [(4,starship_url.id)]
                            for vehicle in vehicles:
                                vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                if vehicle_url:
                                    new_film['vehicle_ids'] = [(4,vehicle_url.id)]
                            for character in characters:
                                people_url = self.env['swapi.people'].search([('url','=',character)])
                                if people_url:
                                    new_film['people_ids'] = [(4,people_url.id)]
                            for planet in planets:
                                planet_url = self.env['swapi.planet'].search([('url','=',planet)])
                                if planet_url:
                                    new_film['planet_ids'] = [(4,planet_url.id)]
                        # endif
                    # endfor
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor

        self.env['swapi.film'].search([('title','=','DEMO')]).unlink()
        to_update = self.env['swapi.home'].search([('name','=','FILMS')])
        to_update['last_update'] = datetime.now()
#         return{
#             'res_model': 'swapi.film',
#             'type': 'ir.actions.act_window',
#             'field_parent':'Films',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.film_view_list'
#         }
        return True
    
#     UPDATE PEOPLE

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
                                    if specie_url:
                                        people['specie_ids'] = [(4,specie_url.id)]
                                for starship in starships:
                                    starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                    if starship_url:
                                        people['starship_ids'] = [(4,starship_url.id)]
                                for vehicle in vehicles:
                                    vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                    if vehicle_url:
                                        people['vehicle_ids'] = [(4,vehicle_url.id)]
                                for film in films:
                                    film_url = self.env['swapi.film'].search([('url','=',film)])
                                    if film_url:
                                        people['film_ids'] = [(4,film_url.id)]
                                if people.homeworld:
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
                                    if film_url:
                                        new_people['film_ids'] = [(4,film_url.id)]
                                for specie in species:
                                    specie_url = self.env['swapi.specie'].search([('url','=',specie)])
                                    if specie_url:
                                        new_people['specie_ids'] = [(4,specie_url.id)]
                                for starship in starships:
                                    starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                    if starship_url:
                                        new_people['starship_ids'] = [(4,starship_url.id)]
                                for vehicle in vehicles:
                                    vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                    if vehicle_url:
                                        new_people['vehicle_ids'] = [(4,vehicle_url.id)]

                                if people.homeworld:
                                    planet = self.env['swapi.planet'].search([('url','=',people['homeworld'])])
                                    new_people['planet_ids'] = planet
                            # endif
                        # endfor

                    elif line == 'next':
                        next_request = json_data[line]
                    # endif
                # endfor

            self.env['swapi.people'].search([('name','=','DEMO')]).unlink()
            to_update = self.env['swapi.home'].search([('name','=','PEOPLE')])
            to_update['last_update'] = datetime.now()
#             return{
#                 'res_model': 'swapi.people',
#                 'type': 'ir.actions.act_window',
#                 'field_parent':'People',
#                 'view_mode':'tree',
#                 'xml_id':'swapi_quizz.people_view_list'
#             }
            return True


#     UPDATE STARSHIP

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
                                if pilot_url:
                                    starship['people_ids'] = [(4,pilot_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                if film_url:
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
                                if pilot_url:
                                    new_starship['people_ids'] = [(4,pilot_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                if film_url:
                                    new_starship['film_ids'] = [(4,film_url.id)]
                        # endif
                    # endfor
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor
        self.env['swapi.starship'].search([('name','=','DEMO')]).unlink()
        to_update = self.env['swapi.home'].search([('name','=','STARSHIPS')])
        to_update['last_update'] = datetime.now()
#         return{
#             'res_model': 'swapi.starship',
#             'type': 'ir.actions.act_window',
#             'field_parent':'Starships',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.starship_view_list'
#         }  
        return True

# UPDATE VEHICLES

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
                                if pilot_url:
                                    vehicle['people_ids'] = [(4,pilot_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                if film_url:
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
                                if pilot_url:
                                    new_vehicle['people_ids'] = [(4,pilot_url.id)]
                            for film in films:
                                film_url = self.env['swapi.film'].search([('url','=',film)])
                                if film_url:
                                    new_vehicle['film_ids'] = [(4,film_url.id)]
                        # endif
                    # endfor
                    
                elif line == 'next':
                    next_request = json_data[line]
                # endif
            # endfor
        self.env['swapi.vehicle'].search([('name','=','DEMO')]).unlink()
        to_update = self.env['swapi.home'].search([('name','=','VEHICLES')])
        to_update['last_update'] = datetime.now()
#         return{
#             'res_model': 'swapi.vehicle',
#             'type': 'ir.actions.act_window',
#             'field_parent':'Vehicles',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.vehicle_view_list'
#         } 
        return True
    
#  START UPDATE ALL   
#   1 - SPECIES
    def update_all(self):

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
                            planet = result['homeworld']
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
                                    if film_url:
                                        specie['film_ids'] = [(4,film_url.id)]



                                for character in people:
                                    character_url = self.env['swapi.people'].search([('url','=',character)])
                                    if character_url:
                                        specie['people_ids'] = [(4,character_url.id)]

                                planet = self.env['swapi.planet'].search([('url','=',specie['homeworld'])])
                                if planet:
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
                                    if film_url:
                                        new_specie['film_ids'] = [(4,film_url.id)]
                                for character in people:
                                    people_url = self.env['swapi.people'].search([('url','=',character)])
                                    if people_url:
                                        new_specie['people_ids'] = [(4,people_url.id)]
                                planet = self.env['swapi.planet'].search([('url','=',specie['homeworld'])])
                                if planet:
                                    new_specie['planet_ids'] = planet


                    elif line == 'next':
                        next_request = json_data[line]
                    # endif
                # endfor
            

# 2 - PLANETS
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
                                    if resident_url:
                                        planet['people_ids'] = [(4,resident_url.id)]
                                for film in films:
                                    film_url = self.env['swapi.film'].search([('url','=',film)])
                                    if film_url:
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
                                    if resident_url:
                                        new_planet['people_ids'] = [(4,resident_url.id)]
                                for film in films:
                                    film_url = self.env['swapi.film'].search([('url','=',film)])
                                    if film_url:
                                        new_planet['film_ids'] = [(4,film_url.id)]
                            # endif
                        # endfor

                    elif line == 'next':
                        next_request = json_data[line]
                    # endif
                # endfor

# 3 -    
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
                                    if specie_url:
                                        film['specie_ids'] = [(4,specie_url.id)]
                                for starship in starships:
                                    starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                    if starship_url:
                                        film['starship_ids'] = [(4,starship_url.id)]
                                for vehicle in vehicles:
                                    vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                    if vehicle_url:
                                        film['vehicle_ids'] = [(4,vehicle_url.id)]
                                for character in characters:
                                    people_url = self.env['swapi.people'].search([('url','=',character)])
                                    if people_url:
                                        film['people_ids'] = [(4,people_url.id)]
                                for planet in planets:
                                    planet_url = self.env['swapi.planet'].search([('url','=',planet)])
                                    if planet_url:
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
                                    if specie_url:
                                        new_film['specie_ids'] = [(4,specie_url.id)]
                                for starship in starships:
                                    starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                    if starship_url:
                                        new_film['starship_ids'] = [(4,starship_url.id)]
                                for vehicle in vehicles:
                                    vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                    if vehicle_url:
                                        new_film['vehicle_ids'] = [(4,vehicle_url.id)]
                                for character in characters:
                                    people_url = self.env['swapi.people'].search([('url','=',character)])
                                    if people_url:
                                        new_film['people_ids'] = [(4,people_url.id)]
                                for planet in planets:
                                    planet_url = self.env['swapi.planet'].search([('url','=',planet)])
                                    if planet_url:
                                        new_film['planet_ids'] = [(4,planet_url.id)]
                            # endif
                        # endfor

                    elif line == 'next':
                        next_request = json_data[line]
                    # endif
                # endfor

#  4 - people
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
                                    if specie_url:
                                        people['specie_ids'] = [(4,specie_url.id)]
                                for starship in starships:
                                    starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                    if starship_url:
                                        people['starship_ids'] = [(4,starship_url.id)]
                                for vehicle in vehicles:
                                    vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                    if vehicle_url:
                                        people['vehicle_ids'] = [(4,vehicle_url.id)]
                                for film in films:
                                    film_url = self.env['swapi.film'].search([('url','=',film)])
                                    if film_url:
                                        people['film_ids'] = [(4,film_url.id)]
                                planet = self.env['swapi.planet'].search([('url','=',people['homeworld'])])
                                if planet:
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
                                    if film_url:
                                        new_people['film_ids'] = [(4,film_url.id)]
                                for specie in species:
                                    specie_url = self.env['swapi.specie'].search([('url','=',specie)])
                                    if specie_url:
                                        new_people['specie_ids'] = [(4,specie_url.id)]
                                for starship in starships:
                                    starship_url = self.env['swapi.starship'].search([('url','=',starship)])
                                    if starship_url:
                                        new_people['starship_ids'] = [(4,starship_url.id)]
                                for vehicle in vehicles:
                                    vehicle_url = self.env['swapi.vehicle'].search([('url','=',vehicle)])
                                    if vehicle_url:
                                        new_people['vehicle_ids'] = [(4,vehicle_url.id)]

                                planet = self.env['swapi.planet'].search([('url','=',specie['homeworld'])])
                                if planet:
                                    new_people['planet_ids'] = planet
                            # endif
                        # endfor

                    elif line == 'next':
                        next_request = json_data[line]
                    # endif
                # endfor

#  5 - starships

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
                                    if pilot_url:
                                        starship['people_ids'] = [(4,pilot_url.id)]
                                for film in films:
                                    film_url = self.env['swapi.film'].search([('url','=',film)])
                                    if film_url:
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
                                    if pilot_url:
                                        new_starship['people_ids'] = [(4,pilot_url.id)]
                                for film in films:
                                    film_url = self.env['swapi.film'].search([('url','=',film)])
                                    if film_url:
                                        new_starship['film_ids'] = [(4,film_url.id)]
                            # endif
                        # endfor

                    elif line == 'next':
                        next_request = json_data[line]


#  6 - vehicles
                
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
                                    if pilot_url:
                                        vehicle['people_ids'] = [(4,pilot_url.id)]
                                for film in films:
                                    film_url = self.env['swapi.film'].search([('url','=',film)])
                                    if film_url:
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
                                    if pilot_url:
                                        new_vehicle['people_ids'] = [(4,pilot_url.id)]
                                for film in films:
                                    film_url = self.env['swapi.film'].search([('url','=',film)])
                                    if film_url:
                                        new_vehicle['film_ids'] = [(4,film_url.id)]
                            # endif
                        # endfor

                    elif line == 'next':
                        next_request = json_data[line]

                
                
                
                
                
            self.env['swapi.planet'].search([('name','=','DEMO')]).unlink()
            to_update_species = self.env['swapi.home'].search([('name','=','SPECIES')])
            to_update_species['last_update'] = datetime.now()
            
            to_update_planets = self.env['swapi.home'].search([('name','=','PLANETS')])
            to_update_planets['last_update'] = datetime.now()
            
            to_update_films = self.env['swapi.home'].search([('name','=','FILMS')])
            to_update_films['last_update'] = datetime.now()
            
            to_update_people = self.env['swapi.home'].search([('name','=','PEOPLE')])
            to_update_people['last_update'] = datetime.now()
            
            to_update_starships = self.env['swapi.home'].search([('name','=','STARSHIPS')])
            to_update_starships['last_update'] = datetime.now()
            
            to_update_vehicles = self.env['swapi.home'].search([('name','=','VEHICLES')])
            to_update_vehicles['last_update'] = datetime.now()
            
            to_update_all = self.env['swapi.home'].search([('name','=','UPDATE ALL DATAS')])
            to_update_all['last_update'] = datetime.now()

        
# END UPDATE ALL    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# #     Redirection de Home vers menu Species    
#     def menu_species(self):
#         return{
#             'res_model': 'swapi.specie',
#             'type': 'ir.actions.act_window',
#             'field_parent':'Species',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.specie_view_list'
#         }
# #     Redirection de Home vers menu Planets    
#     def menu_planets(self):
#         return{
#             'res_model': 'swapi.planet',
#             'type': 'ir.actions.act_window',
#             'field_parent':'Planets',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.planet_view_list'
#         }

# #     Redirection de Home vers menu Films
#     def menu_films(self):
#         return{
#             'res_model': 'swapi.film',
#             'type': 'ir.actions.act_window',
#             'field_parent':'Films',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.film_view_list'
#         }
    
# #     Redirection de Home vers menu People
#     def menu_people(self):
#         return{
#             'res_model': 'swapi.people',
#             'type': 'ir.actions.act_window',
#             'field_parent':'People',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.people_view_list'
#         }
    
#  #     Redirection de Home vers menu Starships
#     def menu_starships(self):
#         return{
#             'res_model': 'swapi.starship',
#             'type': 'ir.actions.act_window',
#             'field_parent':'Starships',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.starship_view_list'
#         }       

#  #     Redirection de Home vers menu Vehicles
#     def menu_vehicles(self):
#         return{
#             'res_model': 'swapi.vehicle',
#             'type': 'ir.actions.act_window',
#             'field_parent':'Vehicles',
#             'view_mode':'tree',
#             'xml_id':'swapi_quizz.vehicle_view_list'
#         } 