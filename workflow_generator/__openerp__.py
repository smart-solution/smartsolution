# -*- coding: utf-8 -*-
{
    'name': "Workflow Generator",

    'summary': """
    Business Flow Generator
     """,

    'description': """
    Business Flow Generator
    """,

    'author': "fabian.semal@smartsolution.be",
    'website': "http://www.smartsolution.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'workflow_generator_view.xml',
    ],
}
