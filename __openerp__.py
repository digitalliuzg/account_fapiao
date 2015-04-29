# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution

#
##############################################################################


{
    'name': '根据账单明细开发票',

    'category': 'account',
    'sequence': 10,

    'name': '根据账单明细开发票',
    'description': """
        根据账单明细开发票
    """,
    'author': 'ZWL',

    'images': [],
    'depends': ['base','account','stock','product','sale'],
    'data': [
        # 'account_invoice.xml',
        'fapiao_view.xml',

    ],

    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
