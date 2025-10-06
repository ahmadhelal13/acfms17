from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime

WEEKDAYS = [
    ("0", "Sunday"),
    ("1", "Monday"),
    ("2", "Tuesday"),
    ("3", "Wednesday"),
    ("4", "Thursday"),
    ("5", "Friday"),
    ("6", "Saturday"),
]


class HrEmployeee(models.Model):
    _inherit = "hr.employee"

    work_start_date = fields.Date(string="Work Start Date")
    emp_address = fields.Text(string="Full Address")
    permission_number = fields.Integer(string="Permission Number")
    day_state = fields.Selection(
        [
            ("absent", "Absent"),
            ("absent_cuz_late", "Absent Cuz Late"),
            ("present", "Present"),
        ],
        compute="_compute_day_state",
        store=True,
    )
    permission_balance = fields.Integer(string="Permission Balance", default=6)
    shift_managment_line_ids = fields.One2many("shift.managment.line", "employee_id")
    late_duration = fields.Float(string="Late Duration", readonly=True)

    @api.depends("last_check_in", "job_id")
    def _compute_day_state(self):
        for rec in self:
            attendance_obj = self.env["hr.attendance"].search([("employee_id", "=", rec.id), ("check_in", "=", rec.last_check_in)])

            if attendance_obj:
                if attendance_obj.late_duration > 0 and attendance_obj.day_state == "absent":
                    rec.day_state = "absent_cuz_late"
                    rec.late_duration = attendance_obj.late_duration
            else:
                rec.day_state = False
                rec.late_duration = 0

    def update_permission_balance(self):
        emp_obj = self.search([])
        if emp_obj:
            for rec in emp_obj:
                rec.permission_balance = 6

    def get_absent_employees(self):
        # Get today's date
        today_date = datetime.now().date()
        today_weekday = str(today_date.weekday())  # Odoo stores weekdays as strings (0=Monday, 6=Sunday)

        # Get all employees
        employees = self.search([])

        for employee in employees:
            # Get the employee's working schedule (resource calendar)
            calendar = employee.resource_calendar_id

            # Check if the employee has work scheduled today
            work_scheduled_today = calendar.attendance_ids.filtered(lambda a: a.dayofweek == today_weekday)
            permission_request = self.env["hr.leave"].search(
                [
                    ("employee_id", "=", employee.id),
                    ("request_date_from", "=", today_date),
                    ("state", "=", "validate"),
                ],
                limit=1,
            )

            if work_scheduled_today:
                if not permission_request:
                    # Check if the employee has attendance for today
                    attendance_today = (
                        self.env["hr.attendance"]
                        .sudo()
                        .search(
                            [
                                ("employee_id", "=", employee.id),
                                (
                                    "check_in",
                                    ">=",
                                    datetime.combine(today_date, datetime.min.time()),
                                ),
                                (
                                    "check_in",
                                    "<=",
                                    datetime.combine(today_date, datetime.max.time()),
                                ),
                            ]
                        )
                    )

                    # If no attendance record found for today, add to the absent_employees list
                    if not attendance_today:
                        employee.write({"day_state": "absent"})
                    else:
                        if attendance_today.day_state == "absent":
                            employee.write({"day_state": "absent_cuz_late"})
                        elif attendance_today.day_state == "present":
                            employee.write({"day_state": "present"})
                        else:
                            employee.write({"day_state": ""})
                        # absent_employees.append(employee)
                else:
                    employee.write({"day_state": ""})

        # Return the list of employees who haven't made attendance today


# class KscAppointmentModel(models.Model):
#     _inherit = "ksc.appointment"

#     has_access_to_see_other_profiles = fields.Boolean(compute="_compute_has_access_to_see_other_profiles")

#     def _compute_has_access_to_see_other_profiles(self):
#         for rec in self:
#             if self.has_group("hr.employee_public"):
#                 rec.has_access_to_see_other_profiles = True
#                 raise UserError("access")
#             else:
#                 rec.has_access_to_see_other_profiles = False


class ShiftManagmentLine(models.Model):
    _name = "shift.managment.line"
    _description = "shift.managment.line"

    employee_id = fields.Many2one("hr.employee")
    day = fields.Selection(WEEKDAYS, string="Day")
    date = fields.Date(string="Date")
    work_start = fields.Float(string="Work Start")
    work_end = fields.Float(string="Work End")
    shift_type = fields.Selection([("night", "Night"), ("morning", "Morning")])
    lateness_duration = fields.Float(string="Lateness Duration")
    day_state = fields.Selection([("absent", "Absent"), ("present", "Presnet")])
    check_in = fields.Datetime(string="Check in")

    # @api.depends("shift_managment_line_ids", "last_check_in", "job_id")
    # def _compute_day_state(self):
    #     late_policy_obj = self.env["late.policy"]
    #     for employee in self:
    #         for line in employee.shift_managment_line_ids:
    #             if (
    #                 employee.last_check_in
    #                 and employee.last_check_in.date() == line.date
    #             ):
    #                 if line.work_start and line.work_end:
    #                     line.check_in = employee.last_check_in
    #                     hours = int(line.work_start)
    #                     minutes = int((line.work_start - hours) * 60)
    #                     diff_hour = employee.last_check_in.time().hour - hours
    #                     diff_min = employee.last_check_in.time().minute - minutes
    #                     lateness_duration_hours = max(diff_hour, 0)
    #                     lateness_duration_minutes = max(diff_min, 0)

    #                     # If minutes are greater than or equal to 60, adjust the hours and minutes accordingly
    #                     if lateness_duration_minutes >= 60:
    #                         lateness_duration_hours += lateness_duration_minutes // 60
    #                         lateness_duration_minutes = lateness_duration_minutes % 60

    #                     line.lateness_duration = float(
    #                         f"{lateness_duration_hours}.{lateness_duration_minutes:02d}"
    #                     )
    #                     if line.lateness_duration:
    #                         late_policy = late_policy_obj.search(
    #                             [("job_position_id", "=", employee.job_id.id)]
    #                         )
    #                         if late_policy:
    #                             if (
    #                                 line.lateness_duration
    #                                 > int(late_policy.late_duration) / 100
    #                             ):
    #                                 line.day_state = "absent"
    #                                 employee.day_state = "absent"
    #                             else:
    #                                 line.day_state = "present"
    #                                 employee.day_state = "present"

    #                 else:
    #                     line.lateness_duration = 0
    #             else:
    #                 pass

    # @api.depends("shift_managment_line_ids", "last_check_in", "job_id")
    # def _compute_day_state(self):
    #     late_policy_obj = self.env["late.policy"]

    #     for employee in self:
    #         last_check_in_date = (
    #             employee.last_check_in and employee.last_check_in.date()
    #         )

    #         for line in employee.shift_managment_line_ids:
    #             if (
    #                 last_check_in_date == line.date
    #                 and line.work_start
    #                 and line.work_end
    #             ):
    #                 work_start_hours = int(line.work_start)
    #                 work_start_minutes = int((line.work_start - work_start_hours) * 60)

    #                 check_in_time = employee.last_check_in.time()
    #                 diff_hour = check_in_time.hour - work_start_hours
    #                 diff_minute = check_in_time.minute - work_start_minutes

    #                 # Calculate lateness duration
    #                 lateness_duration_hours = max(diff_hour, 0)
    #                 lateness_duration_minutes = max(diff_minute, 0)
    #                 line.lateness_duration = float(
    #                     f"{lateness_duration_hours}.{lateness_duration_minutes}"
    #                 )

    #                 # Determine day state based on lateness duration and policy
    #                 late_policy = late_policy_obj.search(
    #                     [("job_position_id", "=", employee.job_id.id)], limit=1
    #                 )
    #                 if (
    #                     late_policy
    #                     and line.lateness_duration > late_policy.late_duration / 100
    #                 ):
    #                     line.day_state = "absent"
    #                     employee.day_state = "absent"
    #                 else:
    #                     line.day_state = "present"
    #                     employee.day_state = "present"
    #             else:
    #                 line.lateness_duration = 0
