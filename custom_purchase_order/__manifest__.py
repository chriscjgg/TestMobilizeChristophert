# -*- coding: utf-8 -*-
{
    'name': "Customización en pedidos de compra (Prueba)",


    'description': """
        BOTON DE CONSULTA AGREGADO AL FORMULARIO DE PEDIDO DE COMPRA
    """,

    'author': "Christopher García gutierrez.cg33@gmail.com",

    'category': 'purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        'views/purchase_order.xml',
    ],
    # only loaded in demonstration mode
#     'demo': [
#         'demo/demo.xml',
#     ],
}
