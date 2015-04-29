# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################
from openerp import models, fields, api, _

class account_fapiao(models.Model):
    _name = "account.fapiao"
    _inherit = ['mail.thread']
    _order = "fapiao_date desc,id desc"


    name=fields.Integer(string="Fapiao Number", required=True)
    fapiao_date=fields.Date(string="Fapiao Date", required=True,default=fields.Date.today)
    category_id=fields.Many2one('res.partner.category',string=u'发票抬头')
    amount_with_taxes=fields.Float('Fapiao total amount', required=True)
    notes=fields.Text(string="Notes")
    partner_id=fields.Many2one('res.partner',string='Partner')
    fapiao_line_id=fields.One2many('account.fapiao.line','fapiao_id')




    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):

        if self.partner_id:
            res=[]
            move_lines= self.env['account.move.line'].search([('state','=','valid'),('partner_id','=',self.partner_id.id),('account_id.type','not in',['receivable'])])
            for line in move_lines:
                if line.journal_id.type== 'sale':
                    if line.credit != 0 and line.debit == 0:
                        print '4',line.credit
                        res.append({ 'move_line_id': line.id, 'amount_original':line.credit,'product_id':line.product_id })
                        # res.append({ 'move_line_id': line.id, 'amount_original':line.credit,'product_id':line.product_id })
                        print '5',res
                        # pass
                if line.journal_id.type == 'sale_refund':
                    if line.credit ==0 and line.debit !=0:
                        res.append({'move_line_id':line.id,'amount_original':-line.debit, 'product_id':line.product_id})
                        # res.append({'move_line_id':line.id,'amount_original':-line.debit, 'product_id':line.product_id})
                        # pass
            # self.fapiao_line_id = [{'move_line_id': 2},{'partner_id':6}]
            self.fapiao_line_id = res
            # self.category_id = 1
            # self.fapiao_line_id = [{'move_line_id': 2},{'partner_id':6}]
        print self.fapiao_line_id




class account_fapiao_line(models.Model):
    _name = "account.fapiao.line"


    fapiao_id = fields.Many2one('account.fapiao')
    move_line_id=fields.Many2one('account.move.line',string=u'销售明细')
    partner_id =fields.Many2one('res.partner')
    move_id= fields.Many2one('account.move',readonly='True',string=u'账单编号')
    product_id= fields.Many2one('product.product',string=u'产品')
    quantity=fields.Float()
    amount_original=fields.Float()
    amount_unreconciled= fields.Float()
    reconcile = fields.Boolean()
    amount=fields.Float(string=u'本次开票')

    @api.onchange('reconcile')
    def onchange_reconcile(self):
        self.amount = 0.00
        if self.reconcile:
            self.amount = self.amount_original

    @api.multi
    @api.onchange('amount')
    def onchange_amount(self):
        amount_with_taxes = 0.00
        print '55'
        amount_with_taxes=self.amount+ amount_with_taxes
        print '77',self.amount,amount_with_taxes
        self.fapiao_id=[{'amount_with_taxes':10}]
        print '88',self.fapiao_id

    def _compute_balance(self):

        if not self.move_line:
            self.amount_unreconciled = 0.0






