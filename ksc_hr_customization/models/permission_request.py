from odoo import _, api, fields, models
from odoo.exceptions import UserError

WEEKDAYS = [
    ("0", "Monday"),
    ("1", "Tuesday"),
    ("2", "Wednesday"),
    ("3", "Thursday"),
    ("4", "Friday"),
    ("5", "Saturday"),
    ("6", "Sunday"),
]


class PermissionRequest(models.Model):
    _name = "permissions.request"
    _description = "Permission Request"

    employee_id = fields.Many2one("hr.employee", string="Employee")
    permission_type = fields.Selection(
        [
            ("beginning", "Beginning of Work"),
            ("middle", "Middle of Work"),
            ("end", "End of Work"),
            ("general", "General"),
        ],
        string="Permission Type",
    )
    day = fields.Date(string="Day")
    start_time = fields.Datetime(string="From")
    end_time = fields.Datetime(string="To")

    @api.model
    def create(self, values):
        result = super(PermissionRequest, self).create(values)
        day = (int(result.day.strftime("%w")) - 1) % 7

        if result:
            attendance_ids = result.employee_id.resource_calendar_id.attendance_ids
            if attendance_ids and result.permission_type != "general":
                matched_schedule = False
                for line in attendance_ids:
                    if int(line.dayofweek) == day:
                        matched_schedule = True
                        if (
                            result.start_time
                            >= fields.Datetime.to_datetime(line.hour_from)
                            and result.start_time
                            <= fields.Datetime.to_datetime(line.hour_to)
                            and result.end_time
                            <= fields.Datetime.to_datetime(line.hour_to)
                        ):
                            if result.employee_id.permission_balance > 0:
                                result.employee_id.permission_balance -= 2
                            else:
                                raise UserError(
                                    _(
                                        "There is no permission balance for this employee."
                                    )
                                )
                            break
                        else:
                            raise UserError(
                                _("Cannot make request outside the schedule of today.")
                            )
                if not matched_schedule:
                    raise UserError(_("Employee has no schedule for today."))
            elif not attendance_ids:
                raise UserError(_("The schedule is empty!"))
        return result


# from odoo import _, api, fields, models
# from odoo.exceptions import UserError

# WEEKDAYS = [
#     ("0", "Monday"),
#     ("1", "Tuesday"),
#     ("2", "Wednesday"),
#     ("3", "Thursday"),
#     ("4", "Friday"),
#     ("5", "Saturday"),
#     ("6", "Sunday"),
# ]


# class PermissionRequest(models.Model):
#     _name = "permissions.request"
#     _description = "permission request"

#     employee_id = fields.Many2one("hr.employee")
#     permission_type = fields.Selection(
#         [
#             ("beginning", "Beginning of Work"),
#             ("middle", "Middle of Work"),
#             ("end", "End of Work"),
#             ("general", "General"),
#         ],
#         string="Permission Type",
#     )
#     # day = fields.Selection(WEEKDAYS, string="Day")
#     #  start_time = fields.Float(string="From")
#     # end_time = fields.Float(string="To")

#     day = fields.Date(string="Day")
#     start_time = fields.Datetime(string="From")
#     end_time = fields.Datetime(string="To")

#     @api.model
#     def create(self, values):
#         result = super(PermissionRequest, self).create(values)
#         day = (int(fields.Date.from_string(result.day).strftime("%w")) - 1) % 7

#         if result:
#             attendance_ids = result.employee_id.resource_calendar_id.attendance_ids
#             if attendance_ids:
#                 if not result.permission_type == "general":
#                     matched_schedule = False
#                     for line in attendance_ids:
#                         if line.dayofweek == day:
#                             matched_schedule = True
#                             if (
#                                 result.start_time >= line.hour_from
#                                 and result.start_time <= line.hour_to
#                             ) and (result.end_time <= line.hour_to):
#                                 if result.employee_id.permission_balance > 0:
#                                     result.employee_id.permission_balance -= 2
#                                 else:
#                                     raise UserError(
#                                         "There is no permission balance for this employee"
#                                     )
#                                 break
#                             else:
#                                 raise UserError(
#                                     "Cannot make request outside the schedule of today"
#                                 )

#                     if not matched_schedule:
#                         raise UserError("Employee has no schedule for today")
#                 else:
#                     pass
#             else:
#                 raise UserError("The schedule is empty!!!")
#         return result
