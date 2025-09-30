from odoo import _, api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError


class HrAttendanceInherit(models.Model):
    _inherit = "hr.attendance"

    work_start = fields.Float(string="Work Start")
    work_end = fields.Float(string="Work End")
    late_duration = fields.Float(string="Late Duration")
    day_state = fields.Selection(
        [("absent", "Absent"), ("present", "Present")],
    )
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    @api.model
    def create(self, values):
        attendance = super(HrAttendanceInherit, self).create(values)
        employee = attendance.employee_id

        # Calculate day of the week (0 = Monday, 6 = Sunday)
        day_of_week = (int(attendance.check_in.strftime("%w")) - 1) % 7

        # Retrieve attendance schedule for the employee
        attendance_schedule = employee.resource_calendar_id.attendance_ids
        permission_request = self.env["hr.leave"].search(
            [
                ("employee_id", "=", employee.id),
                ("request_date_from", "=", attendance.check_in.date()),
                ('state','=','validate')
            ],
            limit=1,
        )

        # Determine work start and end times based on permission request and schedule
        work_start, work_end = None, None

        for schedule in attendance_schedule:
            if int(schedule.dayofweek) == day_of_week:

                work_start = schedule.hour_from
                work_end = schedule.hour_to

                if permission_request:
                    leave_hours = float(permission_request.request_hour_to) - float(
                        permission_request.request_hour_from
                    )

                    if float(permission_request.request_hour_from) == work_start:
                        work_start += leave_hours
                    elif (
                        float(permission_request.request_hour_from) != work_start
                        and float(permission_request.request_hour_to) == work_end
                    ):
                        work_end -= leave_hours
                break

        if work_start is None:
            raise UserError(_("Employee has no schedule for today."))

        # Set the calculated work start and end times
        attendance.work_start = work_start
        attendance.work_end = work_end

        # Calculate late duration
        check_in_time = fields.Datetime.from_string(attendance.check_in)
        work_start_time = check_in_time.replace(
            hour=int(work_start),
            minute=int((work_start % 1) * 60),
            second=0,
        )
        # 2024-09-02 13:05:53,,,2024-09-02 13:00:00
        if check_in_time > work_start_time:
            late_duration = check_in_time - work_start_time

            attendance.late_duration = (
                late_duration.total_seconds() / 3600
            )  # Convert to hour
        
            # Determine the day state based on late duration
            late_policy = self.env["late.policy"].search(
                [("job_position_id", "=", employee.job_id.id)], limit=1
            )
        
            if (
                late_policy
                and attendance.late_duration >= float(late_policy.late_duration) / 100
            ):
                attendance.day_state = "absent"
            else:
                attendance.day_state = "present"
        else:
            attendance.late_duration = 0.0
            attendance.day_state = "present"

        return attendance


# from odoo import _, api, fields, models
# from datetime import timedelta
# from odoo.exceptions import UserError


# class HrAttendanceInherit(models.Model):
#     _inherit = "hr.attendance"

#     work_start = fields.Float(string="Work Start")
#     work_end = fields.Float(string="Work End")
#     late_duration = fields.Float(string="Late Duration")
#     day_state = fields.Selection(
#         [("absent", "Absent"), ("present", "Present")],
#     )
#     from_date = fields.Date(string="From Date")
#     to_date = fields.Date(string="To Date")

#     @api.model
#     def create(self, values):
#         attendance = super(HrAttendanceInherit, self).create(values)

#         employee = attendance.employee_id
#         late_policy = self.env["late.policy"].search(
#             [("job_position_id", "=", employee.job_id.id)], limit=1
#         )

#         # Calculate day of the week (0 = Monday, 6 = Sunday)
#         day_of_week = (
#             int(fields.Date.from_string(attendance.check_in).strftime("%w")) - 1
#         ) % 7

#         # Retrieve attendance schedule for the employee
#         attendance_schedule = employee.resource_calendar_id.attendance_ids
#         permission_request = self.env["permissions.request"].search(
#             [("employee_id", "=", employee.id), ("day", "=", day_of_week)], limit=1
#         )

#         # Initialize work start and end times
#         work_start, work_end = None, None

#         # Determine work start and end times based on permission request and schedule
#         for schedule in attendance_schedule:
#             if int(schedule.dayofweek) == day_of_week:
#                 work_start = schedule.hour_from
#                 work_end = schedule.hour_to

#                 if permission_request:
#                     if permission_request.permission_type == "beginning":
#                         work_start += 2
#                     elif permission_request.permission_type == "end":
#                         work_end -= 2
#                     elif permission_request.permission_type == "general":
#                         if permission_request.start_time == schedule.hour_from:
#                             work_start += 2
#                         elif permission_request.end_time == schedule.hour_to:
#                             work_end -= 2
#                 break

#         if work_start is None:
#             raise UserError("Employee has no schedule for today")

#         # Set the calculated work start and end times
#         attendance.work_start = work_start
#         attendance.work_end = work_end

#         # Calculate late duration
#         check_in_time = fields.Datetime.from_string(attendance.check_in)
#         work_start_time = check_in_time.replace(
#             hour=int(work_start),
#             minute=int((work_start % 1) * 60),
#             second=0,
#         )

#         if check_in_time > work_start_time:
#             late_duration = check_in_time - work_start_time
#             attendance.late_duration = (
#                 late_duration.total_seconds() / 3600
#             )  # Convert to hours

#             # Determine the day state based on late duration
#             if (
#                 late_policy
#                 and attendance.late_duration >= float(late_policy.late_duration) / 100
#             ):
#                 attendance.day_state = "absent"
#             else:
#                 attendance.day_state = "present"
#         else:
#             attendance.late_duration = 0.0
#             attendance.day_state = "present"

#         return attendance

#     # @api.model
#     # def create(self, values):
#     #     attendance = super(HrAttendanceInherit, self).create(values)

#     #     employee = attendance.employee_id
#     #     late_policy_obj = self.env["late.policy"].search(
#     #         [("job_position_id", "=", employee.job_id.id)], limit=1
#     #     )

#     #     day_of_week = (
#     #         int(fields.Date.from_string(attendance.check_in).strftime("%w")) - 1
#     #     ) % 7

#     #     attendance_ids = employee.resource_calendar_id.attendance_ids
#     #     permission_request_obj = self.env["permissions.request"].search(
#     #         [("employee_id", "=", employee.id), ("day", "=", day_of_week)], limit=1
#     #     )

#     #     if permission_request_obj:
#     #         if attendance_ids:
#     #             matched_schedule = False
#     #             for line in attendance_ids:
#     #                 if int(line.dayofweek) == day_of_week:
#     #                     matched_schedule = True
#     #                     attendance.work_start = (
#     #                         line.hour_from + 2
#     #                         if permission_request_obj.permission_type == "beginning"
#     #                         else line.hour_from
#     #                     )
#     #                     attendance.work_end = (
#     #                         line.hour_to - 2
#     #                         if permission_request_obj.permission_type == "end"
#     #                         else line.hour_to
#     #                     )

#     #                     # Calculate late duration
#     #                     check_in_time = fields.Datetime.from_string(attendance.check_in)
#     #                     work_start_time = check_in_time.replace(
#     #                         hour=int(attendance.work_start),
#     #                         minute=int((attendance.work_start % 1) * 60),
#     #                         second=0,
#     #                     )

#     #                     if check_in_time > work_start_time:
#     #                         late_duration = check_in_time - work_start_time
#     #                         attendance.late_duration = (
#     #                             late_duration.total_seconds() / 3600
#     #                         )  # Convert seconds to hours
#     #                         if attendance.late_duration:
#     #                             if (
#     #                                 late_policy_obj.job_position_id.id
#     #                                 == employee.job_id.id
#     #                             ) and attendance.late_duration >= float(
#     #                                 late_policy_obj.late_duration
#     #                             ) / 100:
#     #                                 attendance.day_state = "absent"
#     #                             else:
#     #                                 attendance.day_state = "present"
#     #                     else:
#     #                         attendance.late_duration = 0.0
#     #                     break
#     #     else:

#     #         if attendance_ids:
#     #             matched_schedule = False
#     #             for line in attendance_ids:
#     #                 if int(line.dayofweek) == day_of_week:
#     #                     matched_schedule = True
#     #                     attendance.work_start = line.hour_from
#     #                     attendance.work_end = line.hour_to

#     #                     # Calculate late duration
#     #                     check_in_time = fields.Datetime.from_string(attendance.check_in)
#     #                     work_start_time = check_in_time.replace(
#     #                         hour=int(line.hour_from),
#     #                         minute=int((line.hour_from % 1) * 60),
#     #                         second=0,
#     #                     )

#     #                     if check_in_time > work_start_time:
#     #                         late_duration = check_in_time - work_start_time
#     #                         attendance.late_duration = (
#     #                             late_duration.total_seconds() / 3600
#     #                         )
#     #                         if attendance.late_duration:
#     #                             if (
#     #                                 late_policy_obj.job_position_id.id
#     #                                 == employee.job_id.id
#     #                             ) and attendance.late_duration >= float(
#     #                                 late_policy_obj.late_duration
#     #                             ) / 100:
#     #                                 attendance.day_state = "absent"
#     #                             else:
#     #                                 attendance.day_state = "present"
#     #                     else:
#     #                         attendance.late_duration = 0.0
#     #                     break

#     #     if not matched_schedule:
#     #         raise UserError("Employee has no schedule for today")
#     #     return attendance
