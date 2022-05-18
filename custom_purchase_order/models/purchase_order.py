# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    invoice_id = fields.Many2one('account.move', string="Factura",compute="_invoice_factura_order") 
    date_invoice = fields.Date(string="Fecha Factura",compute="_invoice_factura_order_date") 
    

    def _invoice_factura_order(self):
        for rec in self:
            rec.invoice_id = False
            if rec.order_id.invoice_ids:
                rec.invoice_id = rec.order_id.invoice_ids[0]

    def _invoice_factura_order_date(self):
        for rec in self:
            rec.date_invoice = False
            if rec.order_id.invoice_ids:
                rec.date_invoice = rec.order_id.invoice_ids[0].date


    def show_item_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window',
            'name':'Operaciones detalladas',
            'res_model':'purchase.order.line',
            'res_id':self.id,
            'context':self._context,
            'view_mode':'form',
            'view_id':self.env.ref('custom_purchase_order.purchase_order_line_form777').id,
            'target':'new'
        }