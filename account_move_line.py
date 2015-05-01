# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################
from openerp import models, fields, api, _

class account_move_line(models.Model):
    _inherit = 'account.move.line'

    balance_fapiao=fields.Float(compute='balance_fapiao', store=True)


    @api.depends
    def balance_fapiao(self):
        print '533'
        self.balance_fapiao = 5
        print '544'