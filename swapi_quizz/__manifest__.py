#  -*- coding: utf-8

{
    'name': 'Swapi Quizz',
    
    'summary': """Contains all Star Wars data""" ,
    
    'description': """
        All the Star Wars data you have ever wanted:
        - Species
        - Films
        - People
        - Vehicles
        - Spaceships
        - Planets
    """,
    'author': 'PBN + AGI + CGA',
    'website': 'https://www.captivea.com',
    'category':'Star Wars',
    'version':'1.1.0',
    'depends': ['base'],
    'data':[
        'security/swapi_security.xml',
        'security/ir.model.access.csv',
        'views/specie_views.xml',
        'views/planet_views.xml',
        'views/film_views.xml',
        'views/people_views.xml',
        'views/starship_views.xml',
        'views/vehicle_views.xml',
        'views/home_views.xml',
        'views/player_views.xml',
        'views/theme_views.xml',
        'views/level_views.xml',
        'views/quizz_views.xml',
        'views/question_template_views.xml',
        'views/swapi_menuitems.xml',
        'wizard/specie_wizard_view.xml',
        'wizard/planet_wizard_view.xml',
        'wizard/film_wizard_view.xml',
        'wizard/people_wizard_view.xml',
        'wizard/starship_wizard_view.xml',
        'wizard/vehicle_wizard_view.xml',
        'wizard/quizz_wizard_view.xml',
        'demo/swapi_demo.xml'
            ],
    'demo':[
        
    ],
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3'
}