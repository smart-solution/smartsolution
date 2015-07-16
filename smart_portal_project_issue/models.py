# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import Warning
from openerp import SUPERUSER_ID
from mock import self

class res_users(models.Model):
    _inherit = 'res.users'

    portal_project_id = fields.Many2one('project.project','Default Project for Portal Issues')
    portal_customer_id = fields.Many2one('res.partner','Customer for Portal Issues',domain=[('is_company','=',True),('customer','=',True)])


class res_partner(models.Model):
    _inherit = 'res.partner'

    project_ids = fields.One2many('project.project', 'partner_id', 'Projects')


class project_issue(models.Model):
    _inherit = 'project.issue'
    _order = 'id'

    in_warranty = fields.Boolean('Under Warranty')
    estimated_time = fields.Float('Estimated Duration')
    project_ids = fields.One2many('project.project', 'partner_id', string='Projects')
    stage_name = fields.Char(related='stage_id.name')

    def create(self, cr, uid, vals, context=None):
        """Fills the issue project with the user default project for portal issues"""
        if ('project_id' not in vals or 'project_id' in vals and not vals['project_id']) and 'partner_id' in vals and vals['partner_id']:
            user_id = self.pool.get('res.users').search(cr, uid, [('partner_id','=',vals['partner_id'])])
            if user_id:
                user = self.pool.get('res.users').browse(cr, uid, user_id[0])
                vals['project_id'] = user.portal_project_id and user.portal_project_id.id or False
        return super(project_issue, self).create(cr, uid, vals, context=context)


    def search(self, cr, uid, args, offset=0, limit=None, order=None,
                context=None, count=False):
#         if 'portal' in context:
#             user = self.pool.get('res.users').browse(cr, uid, uid)
        user = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context)
        if user.share:
            project_ids = self.pool.get('project.project').search(cr, uid, [('partner_id','=',user.portal_customer_id.id)])
            args.append(['project_id','in',project_ids])
        return super(project_issue, self).search(cr, uid, args=args, offset=offset, limit=limit, order=order,
            context=context, count=count)

    def write(self, cr, uid, ids, vals, context=None):
        print "WRITE PROJECT_ISSUE",vals
        user = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context)
        if user.share:
            print "share"
            if ('stage_id' in vals or 'priority' in vals or 'name' in vals) and len(vals) == 1:
                return super(project_issue, self).write(cr, uid, ids, vals=vals, context=context)
            else:
                raise Warning('You cannot modify an issue.')
        else:
            print "not share"
            return super(project_issue, self).write(cr, uid, ids, vals=vals, context=context)
#             raise osv.except_osv(_('Error!'), _('You cannot modify an issue.'))

    @api.one
    def action_to_plan(self, vals):
        stage_id = self.env['project.task.type'].search([('name', '=', 'To plan (Smart)')])
        self.stage_id = stage_id[0].id
#         issue = self.env['project.issue'].sudo().search([('id', '=', self.id)])
#         return self.write({'stage_id': stage_id[0].id})

    @api.one
    def action_to_qualify(self, vals):
        stage_id = self.env['project.task.type'].search([('name', '=', 'To qualify (Smart)')])
        self.stage_id = stage_id[0].id
#         issue = self.env['project.issue'].sudo().search([('id', '=', self.id)])
#         return issue.write({'stage_id': stage_id[0].id})
        
    @api.one
    def action_to_release(self, vals):
        stage_id = self.env['project.task.type'].search([('name', '=', 'To release (Smart)')])
        self.stage_id = stage_id[0].id
#         issue = self.env['project.issue'].sudo().search([('id', '=', self.id)])
#         return issue.write({'stage_id': stage_id[0].id})

    @api.one
    def action_in_progress(self, vals):
        stage_id = self.env['project.task.type'].search([('name', '=', 'In progress (Smart)')])
        self.stage_id = stage_id[0].id
#         issue = self.env['project.issue'].sudo().search([('id', '=', self.id)])
#         return issue.write({'stage_id': stage_id[0].id})
        
    @api.one
    def action_to_close(self, vals):
        stage_id = self.env['project.task.type'].search([('name', '=', 'Done')])
        self.stage_id = stage_id[0].id
#         issue = self.env['project.issue'].sudo().search([('id', '=', self.id)])
#         return issue.write({'stage_id': stage_id[0].id})

    @api.one
    def action_cancel(self, vals):
        stage_id = self.env['project.task.type'].search([('name', '=', 'Cancelled')])
        self.stage_id = stage_id[0].id
#         issue = self.env['project.issue'].sudo().search([('id', '=', self.id)])
#         return issue.write({'stage_id': stage_id[0].id})

    @api.one
    def action_hold(self, vals):
        stage_id = self.env['project.task.type'].search([('name', '=', 'On hold')])
        self.stage_id = stage_id[0].id
#         issue = self.env['project.issue'].sudo().search([('id', '=', self.id)])
#         return self.write({'stage_id': stage_id[0].id})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: