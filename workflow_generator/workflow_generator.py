# -*- coding: utf-8 -*-

from openerp import models
from openerp.osv import fields
from openerp.exceptions import Warning
from openerp import SUPERUSER_ID


class workflow_generator_wizard(models.TransientModel):

    _name = "workflow.generator.wizard"

    _columns = {
        'name': fields.char('Nom du menu', size=64),
        'parent_menu_id': fields.many2one('ir.ui.menu', 'Menu parent'),
    }

    def workflow_generate(self, cr, uid, ids, context=None):
        # Genereate business flow

        stage_obj = self.pool.get('crm.case.stage')
        menu_obj = self.pool.get('ir.ui.menu')

        wizard = self.browse(cr, uid, ids)[0]

        for wkf in self.pool.get('workflow').browse(cr, uid, context['active_ids']):
            seq = 10
            for act in wkf.activities:
                stage_vals = {
                    'name': act.name,
                    'sequence': seq,
                    'type': 'opportunity',
                    'fold': False,
                    'probability': 0,
                }
                stage_obj.create(cr, uid, stage_vals, context=context)
                seq = seq + 10

            menu_vals = {
                'name': wizard.name,
                'parent_id': wizard.parent_menu_id.id,
            }
            menu_obj.copy(cr, uid, 138, default=menu_vals, context=context)

        return True


    def default_get(self, cr, uid, fields, context=None):
        res = super(workflow_generator_wizard, self).default_get(cr, uid, fields, context=context)
        wkf = self.pool.get('workflow').browse(cr, uid, context['active_id'])
        res.update({
            'name': wkf.name,
        })
        return res

