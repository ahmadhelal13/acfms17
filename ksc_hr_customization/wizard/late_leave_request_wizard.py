from odoo import models, fields, api

class LateLeaveRequestWizard(models.TransientModel):
    _name = 'late.leave.request.wizard'
    _description = 'Late Leave Request Wizard'
    # this wizard for AR- Late or Leave Latter Report

    date = fields.Date(string="Date", required=True)
    employee_name = fields.Char(string="Employee Name", required=True)
    work_number = fields.Char(string="Work Number", required=True)
    exit_time_from = fields.Float(string="Exit Time From", required=True)
    exit_time_to = fields.Float(string="Exit Time To", required=True)
    exit_hours = fields.Float(string="Exit Hours", required=True)
    reason_for_exit = fields.Text(string="Reason for Exit", required=True)
    manager_opinion = fields.Selection([('accepted', 'Accepted'), ('rejected', 'Rejected')], string="Manager's Opinion", required=True)

    def action_generate_report(self):
        self.ensure_one()
        data = {
            'date': self.date,
            'employee_name': self.employee_name,
            'work_number': self.work_number,
            'exit_time_from': self.exit_time_from,
            'exit_time_to': self.exit_time_to,
            'exit_hours': self.exit_hours,
            'reason_for_exit': self.reason_for_exit,
            'manager_opinion': self.manager_opinion,
        }
        return self.env.ref('ksc_hr_customization.ar_late_leave_request_latter_report_action').report_action(self, data=data)
