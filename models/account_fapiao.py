# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################
import time
from lxml import etree
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import float_compare
from openerp.report import report_sxw
import openerp

class account_fapiao(osv.osv):
    _name = "account.fapiao"
    _inherit = ['mail.thread']
    _order = "fapiao_date desc,id desc"


    _columns = {
        'name':fields.integer(string="Fapiao Number", required=True),
        'fapiao_date':fields.date(string="Fapiao Date", required=True),
        'category_id':fields.many2one('res.partner.category',string=u'发票抬头'),
        'amount_with_taxes': fields.float('Fapiao total amount',
                                              required=True),

        'notes':fields.text(string="Notes"),
        'partner_id':fields.many2one('res.partner',string='Partner'),

        'fapiao_line_id': fields.one2many('account.fapiao.line','fapiao_id'),
    }
    # state = fields.Selection([
    #         ('draft','Draft'),
    #         ('refund','Refund'),
    #         ('open','Open'),
    #         ('paid','Paid'),
    #         ('cancel','Cancelled'),
    #     ], string='Status', index=True, default='draft',)






    def onchange_partner_id(self, cr, uid, ids, partner_id,   date, context=None):

        # if context is None:
        #     context = {}
        # res = self.basic_onchange_partner(cr, uid, ids, partner_id, context=context)
        # print '1',res
        # ctx = context.copy()
        # ctx.update({'date': date})
        # print '2',ctx
        # vals = self.recompute_voucher_lines(cr, uid, ids, partner_id,  date, context=ctx)
        # vals2 = self.recompute_payment_rate(cr, uid, ids, vals,  date,  context=context)
        # print '3',vals
        # print '4',vals2
        #
        # for key in vals.keys():
        #     print '20',key
        #     res[key].update(vals[key])
        #     print '21',res
        # for key in vals2.keys():
        #     res[key].update(vals2[key])
        res = ''
        if partner_id:
            res = {'value': {'fapiao_line_id': [{ 'move_line_id': 1,  },{ 'move_line_id': 2,  }], }}

        return res


class account_fapiao_line(osv.osv):
    _name = "account.fapiao.line"

    _columns = {
        'fapiao_id' : fields.many2one('account.fapiao'),
        'move_line_id':fields.many2one('account.move.line',string=u'账单明细'),
        'partner_id' :fields.many2one('res.partner'),
        'move_id' : fields.many2one('account.move.line',string=u'账单编号'),
        'product_id' : fields.many2one('product.product',string=u'产品'),
        'quantity' : fields.float(),
        'amount_original' : fields.float(),
        'amount_unreconciled' : fields.float(),
        # reconcile = fields.Boolean()
        'amount' :fields.float(string=u'本次开票'),
    }







