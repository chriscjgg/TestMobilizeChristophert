# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Company(models.Model):
    _inherit = 'res.company'
    
    qty_lines_on_purchase_line = fields.Integer(string="lineas de consulta de productos por pedido", default=5)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    qty_lines_on_purchase_line = fields.Integer(string="lineas de consulta de productos por pedido", related="company_id.qty_lines_on_purchase_line",readonly=False)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    purchase_query_ids = fields.One2many('purchase.order', 'order_line_query_id', string="Compras del producto",compute="_compute_result_purchase")


    @api.depends("order_id.order_line")
    def _compute_result_purchase(self):
        for rec in self:
            rec.purchase_query_ids = self.env['purchase.order']
            id_purchaces = []
            purchases = self.env['purchase.order'].search([])
            for pur in purchases:
                for order_line in pur.order_line:
                    if rec.product_id.id == order_line.product_id.id:
                        id_purchaces.append(pur.id)
            for line in self.env['purchase.order'].search([('id','in',list(set(id_purchaces)))],order="create_date desc",limit=rec.company_id.qty_lines_on_purchase_line):
                rec.write({'purchase_query_ids': [(4, line.id)]})
                rec.purchase_query_ids.write({'product_query': rec.product_id.id})
            


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
            'target':'new',
            'context': {'create': False, 'delete': False, 'edit':False},
            
        }



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    order_line_query_id = fields.Many2one('purchase.order.line')
    invoice_name = fields.Many2one('account.move', string="Factura",compute="_invoice_factura_order") 
    date_invoice = fields.Date(string="Fecha Factura",compute="_invoice_factura_order_date") 
    product_query = fields.Many2one('product.product', string="Producto") 
    product_qty = fields.Float(string="Cantidad Pedida",compute="_compute_product_qty") 
    qty_received = fields.Float(string="Cantidad Recibida",compute="_compute_qty_received") 
    price_unit = fields.Float(string="Costo Neto",compute="_compute_price_unit") 
    bodeg = fields.Char(string="Sucursal",compute="_compute_bodeg") 
    

    def _compute_product_qty(self):
        for rec in self:
            mount = 0
            for line in rec.order_line:
                if line.product_id.id == rec.product_query.id:
                    mount += line.product_qty
            rec.product_qty = mount


    def _compute_qty_received(self):
        for rec in self:
            mount = 0
            for line in rec.order_line:
                if line.product_id.id == rec.product_query.id:
                    mount += line.qty_received
            rec.qty_received = mount

    def _compute_price_unit(self):
        for rec in self:
            mount = 0
            for line in rec.order_line:
                if line.product_id.id == rec.product_query.id:
                    mount += line.price_unit
            rec.price_unit = mount


    def _invoice_factura_order(self):
        for rec in self:
            rec.invoice_name = False
            if rec.invoice_ids:
                rec.invoice_name = rec.invoice_ids[0]

    def _invoice_factura_order_date(self):
        for rec in self:
            rec.date_invoice = False
            if rec.invoice_ids:
                rec.date_invoice = rec.invoice_ids[0].date

    def _compute_bodeg(self):
        for rec in self:
            rec.bodeg = False
            if rec.picking_ids:
                rec.bodeg = str(rec.picking_ids[0].location_dest_id.name)