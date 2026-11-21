{
    "name": "Estate",
    "version": "1.0",
    "summary": "Realestate",
    "description": """the real estate module""",
    "author": "Hashim",
    "website": "https://www.hashim.com",
    "category": "Real Estate/Brokerage",
    "sequences": -10,
    "application": True,
    'depends': [
        'base'
    ],
    "data": [
        'security/ir.access.csv',
        'view/estate_propertice.xml',
        'view/estate_property_type.xml',
        'view/estate_property_tag.xml',
        'view/estate_menus.xml',
        'view/estate_property_offer.xml'
    ]
}

