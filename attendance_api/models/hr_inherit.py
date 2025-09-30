# # -*- coding: utf-8 -*-

# from odoo import fields, models, api, _
# from odoo.exceptions import UserError


# class HRInherit(models.Model):
#     _inherit = 'hr.employee'

#     matrix_array = fields.Text()


# class HelpdeskInherit(models.Model):
#     _inherit = 'helpdesk.ticket'

#     attachement = fields.Binary(string="Upload Attachement")
# # message_partner_ids


# class HelpdeskTeamInherit(models.Model):
#     _inherit = 'helpdesk.team'

#     def show_team(self):
#         # is_the_same_doctor = fields.Boolean(
#         #     default=lambda self:  self.env.user.partner_id.id == self.physician_id.id, readonly=True)
#         x = str(self.env.user.name).lower()
#         raise UserError(x)
#         # user_ids = self.env['helpdesk.team'].search(
#         #     [('id', '=', id)]).member_ids

#         # raise UserError(user_ids)

#         # [('id', '=', id)]


# class PartnerInherit(models.Model):
#     _inherit = "res.partner"

#     def get_partner(self):
#         partner_id = self.id
#         individual_contacts = self.env['res.partner'].search(
#             [('id', '=', self.id)]).child_ids

#         selected_student = self.env['discipline.student'].search(
#             [('partner_id.id', '=', partner_id.id)])

#         raise UserError(individual_contacts[0].name)


# class AccountInherit(models.Model):
#     _inherit = "account.move"

#     def get_partner(self):
#         # partner_id = self.id
#         individual_contacts = self.env['account.move'].search(
#             [('id', '=', self.id)]).partner_id
#         raise UserError(individual_contacts.id)

#         [('partner_id.id', '=', partner_id.id)]
#         selected_student = self.env['discipline.student'].search(
#             [('student_id', '=', partner_id.id)])

#         raise UserError(individual_contacts[0].name)
