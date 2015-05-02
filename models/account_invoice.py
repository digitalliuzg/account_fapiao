# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################
from openerp import models, fields, api, _


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'


    fapiao_number = fields.Char(string=u'发票号码',size=8)
    fapiao_amount = fields.Float(string=u'已开金额')
    fapiao_date = fields.Date(string=u'开票日期' )
    journal_id = fields.Many2one('account.journal',related='invoice_id.journal_id',string=u'凭证薄', store=True, readonly=True)
    # order_id = fields.Many2one('sale.order.line', related='id.sale_order_line_invoice_rel.order_line_id.order_id')




