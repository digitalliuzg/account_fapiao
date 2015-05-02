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
    amount_with_taxes = fields.Float('Fapiao total amount', compute='_compute_amount_with_taxes')
    notes=fields.Text(string="Notes")
    partner_id=fields.Many2one('res.partner',string='Partner')
    fapiao_line_id=fields.One2many('account.fapiao.line','fapiao_id')
    state= fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('refunded','Refunded'),
        ('cancel','Cancel')
    ], string=u'状态',default='draft')

    @api.depends('fapiao_line_id')
    def _compute_amount_with_taxes(self):
        if self.fapiao_line_id:
            self.amount_with_taxes = sum((l.amount for l in self.fapiao_line_id))

    def _compute_balance(self,line,amount_original):

        if line:
            subtotal_fapiao_line_amount=0
            #过滤掉取消,草稿的金额 
            fapiao_line= self.env['account.fapiao.line'].search([('move_line_id','=',line.id),('state','in',['confirmed','refunded'])])
            print '554,',fapiao_line
            if fapiao_line:
                for item in fapiao_line:
                    print '23',item.amount
                    subtotal_fapiao_line_amount = subtotal_fapiao_line_amount + item.amount
                amount_unreconciled = amount_original-subtotal_fapiao_line_amount
            else:
                amount_unreconciled = amount_original
            return amount_unreconciled

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
                        amount_original=line.credit
                        print '5',res
                        # pass
                if line.journal_id.type == 'sale_refund':
                    if line.credit ==0 and line.debit !=0:
                        amount_original=-line.debit
                #计算未开发票余额
                amount_unreconciled=self._compute_balance(line,amount_original)
                #不显示余额为0的明细
                if amount_unreconciled>0:
                    res.append({ 'move_line_id': line.id, 'amount_original':amount_original,'amount_unreconciled':amount_unreconciled,'product_id':line.product_id })

            self.fapiao_line_id = res
        print self.fapiao_line_id

    @api.multi
    def fapiao_confirmed(self):
        return self.write({'state': 'confirmed'})

    @api.multi
    def fapiao_cancel(self):
        return self.write({'state':'cancel'})

    @api.multi
    def fapiao_refunded(self):
        return self.write({'state':'refunded'})




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

    # @api.multi
    # @api.depends('move_line_id')
    # def _compute_balance(self):
    #     for self in self:
    #         print self.move_line_id
    #     if self.move_line_id:
    #         res = [item for item in self.move_line_id]
    #         print '333',self.move_line_id.id,res
    #         subtotal_fapiao_line_amount=0
    #         fapiao_line= self.env['account.fapiao.line'].search([('move_line_id','=','self.move_line_id.id')])
    #         print fapiao_line
    #         # for item in fapiao_line.amount:
    #         #     subtotal_fapiao_line_amount = subtotal_fapiao_line_amount + item
    #         # print '444',subtotal_fapiao_line_amount
    #         # self.amount_unreconciled = self.amount_original-subtotal_fapiao_line_amount
    #     # print '774',self.amount_unreconciled






