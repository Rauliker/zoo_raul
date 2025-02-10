{
    'name': 'Zoologia Raul',
    'application': True,
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/zoo_views.xml',
        'views/species_views.xml',  
        'views/animal_views.xml',
        'views/city_views.xml',
        'views/continent_views.xml', 
        'views/estate_menus.xml',
    ],
    'icon': '/zoo_raul/static/description/icon.png',
}
