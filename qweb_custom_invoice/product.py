# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Guewen Baconnier, Bessi Nicolas, Vincent Renaville
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm, fields


class ProductTemplate(orm.Model):
    """TMP fix of bug 1111430"""
    _inherit = 'product.template'
    
    def _empl_product(self, cr, uid, ids, name, args, context=None):
        """Return  true if product is a hr_employee.product_id else return false"""
        res = {}
        empl_obj = self.pool.get('hr.employee')
        for product in self.browse(cr, uid, ids, context=context):
            empl_id = empl_obj.search(cr, uid, [('product_id', '=', product.id)], limit=1)
            res[product.id] = False
            if empl_id:
                res[product.id] = True
        return res

    _columns = {'purchase_ok': fields.boolean('Can be Purchased',
                                              help=("Specify if the product can be selected"
                                                    " in a purchase order line.")),
                'empl_product': fields.function(
                    _empl_product, type='boolean', string='empl', method=True,),
                }
