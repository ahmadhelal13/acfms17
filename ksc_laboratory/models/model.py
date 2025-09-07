from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment'

    clinic = fields.Selection(selection_add=[('laboratory', 'Laboratory')])

    def get_journal_domain(self):
        domain = super(AccountPayment, self).get_journal_domain()
        if self._context.get('laboratory'):
            ids = self.env.company.laboratory_journal_ids.ids
            domain.append(('id', 'in', ids))
        return domain


class DentalPatientWizard(models.TransientModel):
    _inherit = "patient.wizard"

    def print_lab_result_for_this_patient(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        lab_ids = self.env['patient.laboratory.test'].search(
            domain, order="start_date asc").ids
        if lab_ids:
            return self.env.ref(
                'ksc_laboratory.lab_result_report_action').report_action([lab_ids])
        else:
            raise UserError("There's Nothing To Print")
