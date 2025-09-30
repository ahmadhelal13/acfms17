# -*- coding: utf-8 -*-
# ===========================================================#
# @Author:    Ahmed Mokhtar
# @Date:      2025-01-01
# @File:      attendance_call.py
# @Desc:
# CustomCallsOpenapi is a model that provides methods for handling attendance check-in and check-out requests,
# as well as interacting with a face recognition API to process these requests.

# Methods:
#     post_response(status, code, return_list):

#     check_in_request(*args):

#     check_out_request(*args):

#     get_id_from_subject(raw_subject):

#     post_check_in_request(*args):

#     post_check_out_request(*args):
# ===========================================================#
import json
from datetime import datetime
import requests
from dateutil.relativedelta import relativedelta
from odoo import _, api, models


class CustomCallsOpenapi(models.Model):

    _name = "attendance.openapi"
    _description = "Attendance Openapi"

    @api.model
    def post_response(self, status, code, return_list):
        """
        Posts a response with the given status, code, and return list.

        Args:
            status (str): The status of the response.
            code (int): The code associated with the response.
            return_list (list): The list of items to be included in the response.

        Returns:
            list: A list containing a dictionary with the status, code, and return list.
        """
        vals = [
            {
                "status": status,
                "code": code,
                "list": return_list,
            }
        ]

        return vals

    @api.model
    def check_in_request(self, *args):
        """
        Handles the check-in request for an employee.

        This method checks if the employee has already checked in and not checked out.
        If the employee is already checked in, it returns a response indicating that the check-in has already been recorded.
        If the employee is not checked in, it creates a new attendance record with the current check-in time.

        Args:
            *args: Variable length argument list. The first argument should be the employee ID.

        Returns:
            dict: A dictionary containing the status, code, and response message.

        Response:
            - If the employee is already checked in:
                    "status": "Success",
                    "code": 200,
                    "response": [
                    ]
            - If the employee is not checked in:
                    "status": "Success",
                    "code": 200,
                    "response": [
                            "response": "{employee_name} You are checked in at {check_in_time} \n {employee_name} لقد تم تسجيل حضورك في {check_in_time}",
                    ]
        """
        status = ""
        code = 0
        response_msg = []
        employee_id = args[0]
        check_in = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        format_string = "%m/%d/%Y %H:%M:%S"
        check_in_formated = datetime.strptime(check_in, format_string)
        attendance_id = self.env["hr.attendance"].search(
            [
                ("employee_id", "=", employee_id),
                ("check_in", "!=", False),
                ("check_out", "=", False),
            ],
            order="id desc",
            limit=1,
        )
        if attendance_id:
            status = "Success"
            code = 200
            response_msg.append(
                {
                    "response": "Sorry You Are Already Checked In \n عفوا لقد تم تسجيل الحضور مسبقا",
                }
            )
        else:
            attend_id = self.env["hr.attendance"].create(
                {
                    "employee_id": employee_id,
                    "check_in": check_in_formated,
                }
            )
            status = "Success"
            code = 200
            response_msg.append(
                {
                    "response": f"{attend_id.employee_id.name} You are checked in at {check_in_formated + relativedelta(hours=+3)} \ n {attend_id.employee_id.name} لقد تم تسجيل حضورك في {check_in_formated + relativedelta(hours=+3)}",
                }
            )
        return self.post_response(status=status, code=code, return_list=response_msg)

    @api.model
    def check_out_request(self, *args):
        """
        Handles the check-out request for an employee.

        Args:
            *args: Variable length argument list. The first argument should be the employee ID.

        Returns:
            dict: A dictionary containing the status, code, and response message.

        The function performs the following steps:
        1. Retrieves the employee ID from the arguments.
        2. Gets the current date and time as the check-out time.
        3. Searches for the latest attendance record for the given employee ID.
        4. If no attendance record is found, returns a 404 status with an appropriate message.
        5. If the employee has not checked in, returns a 404 status with an appropriate message.
        6. If the employee has checked in but not checked out, updates the check-out time and returns a 200 status with a success message.
        7. If the employee has already checked out, returns a 201 status with an appropriate message.
        """
        status = ""
        code = 0
        response_msg = []
        employee_id = args[0]
        check_out = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        format_string = "%m/%d/%Y %H:%M:%S"
        check_in_formated = datetime.strptime(check_out, format_string)
        attendance_id = self.env["hr.attendance"].search(
            [("employee_id.id", "=", employee_id)], order="id desc", limit=1
        )
        if attendance_id:
            if attendance_id[0].check_in == False:
                status = "Not Found"
                code = 404
                response_msg.append(
                    {
                        "response": "Sorry You Are Not Checked In Today \n عفوا لم تقم بتسجيل الحضور اليوم",
                    }
                )
            elif attendance_id[0].check_in and not attendance_id[0].check_out:
                # attendance_id.check_out = check_in_formated + relativedelta(hours=-3)
                attendance_id.check_out = check_in_formated
                status = "Success"
                code = 200
                response_msg.append(
                    {
                        "response": f"{attendance_id.employee_id.name} Checked Out At { check_in_formated + relativedelta(hours=+3)} \n {attendance_id.employee_id.name} تم تسجيل الانصراف في {check_in_formated + relativedelta(hours=+3)}",
                    }
                )
            elif attendance_id[0].check_out:
                status = "Success"
                code = 201
                response_msg.append(
                    {
                        "response": "Sorry You Are Checked out already  \n عفوا لقد تم تسجيل الانصراف مسبقا",
                    }
                )

        else:
            status = "Not Founded"
            code = 404
            response_msg.append(
                {
                    "response": f"There no employee with this id {employee_id} \n لا يوجد موظف بهذا الرقم {employee_id}",
                }
            )
        return self.post_response(status=status, code=code, return_list=response_msg)

    def get_id_from_subject(self, raw_subject):
        """
        Extracts and returns the subject ID from a given raw subject string.

        The function looks for the last underscore before a parenthesis and extracts
        the number between that underscore and the closing parenthesis.

        Args:
            raw_subject (str): The raw subject string containing the subject ID.

        Returns:
            str: The extracted subject ID.
        """
        # Find the last underscore before a parenthesis
        underscore_pos = raw_subject.rfind("_(")
        if underscore_pos == -1:
            underscore_pos = raw_subject.rfind("_")
            if underscore_pos == -1:
                return ""  # No underscore found

        # Find the closing parenthesis after the underscore
        paren_pos = raw_subject.find(")", underscore_pos)
        if paren_pos == -1:
            return ""  # No closing parenthesis found

        # Extract the ID between the underscore and parenthesis
        subject_id = raw_subject[underscore_pos + 1 : paren_pos].strip()

        # Remove any non-digit characters (like spaces or other characters)
        subject_id = "".join(filter(str.isdigit, subject_id))

        return subject_id

    @api.model
    def post_check_in_request(self, *args):
        """
        Sends a check-in request to the face recognition API and processes the response.

        Args:
            *args: Variable length argument list. The first argument should be the employee image in binary format.

        Returns:
            dict: A dictionary containing the status, code, and response message of the check-in request.

        Raises:
            requests.exceptions.RequestException: If the request to the face recognition API fails.

        The function performs the following steps:
        1. Retrieves the company information.
        2. Constructs the URL and payload for the face recognition API request.
        3. Sends the request to the face recognition API.
        4. Processes the response from the API to determine the employee's identity and similarity score.
        5. If the similarity score is above the threshold, it sends a check-in request for the identified employee.
        6. Returns the status, code, and response message based on the outcome of the check-in request.
        """
        company_id = self.env["res.company"].search([], limit=1)
        status = ""
        code = 0
        response_msg = []
        emp_img = args[0]
        if emp_img:
            url = f"http://{company_id.face_recog_url}/api/v1/recognition/recognize"
            payload = json.dumps({"file": emp_img})
            headers = {
                "Content-Type": "application/json",
                "x-api-key": f"{company_id.face_recog_token}",
            }
            try:
                response = requests.post(url, data=payload, headers=headers)
                response.raise_for_status()
                dict_data = response.json()

            except requests.exceptions.RequestException as e:
                return self.post_response(
                    status="Error",
                    code=500,
                    return_list=[{"response": f"Request failed: {str(e)}"}],
                )

            result = dict_data.get("result")
            if result:
                subject = result[0]["subjects"][0]["subject"]
                similarity = result[0]["subjects"][0]["similarity"]
                if subject:
                    if similarity >= 0.9:
                        emp_id = self.get_id_from_subject(raw_subject=str(subject))
                        res = self.check_in_request(int(emp_id))
                        status = res[0]["status"]
                        code = res[0]["code"]
                        response_msg.append(
                            {
                                "response": f"{res[0]['list'][0]['response']}",
                            }
                        )

                    else:
                        status = "Not Founded"
                        code = 404
                        response_msg.append(
                            {
                                "response": "similarity in not satisfied \n نسبة التشابه غير كافية"
                            }
                        )
                else:
                    status = "Not Founded"
                    code = 404
                    response_msg.append(
                        {"response": "There's no employee \n لا يوجد موظف"}
                    )
            else:
                status = "Not Founded"
                code = 404
                response_msg.append(
                    {"response": "result not statsifed \n النتيجة غير مرضية"}
                )
        else:
            status = "Not Founded"
            code = 404
            response_msg.append({"response": "There's no image \n لا يوجد صورة"})

        return self.post_response(status=status, code=code, return_list=response_msg)

    @api.model
    def post_check_out_request(self, *args):
        """
        Sends a check-out request to the face recognition API and processes the response.
        Args:
            *args: Variable length argument list. The first argument should be the employee image in binary format.
        Returns:
            dict: A dictionary containing the status, code, and response message of the check-out request.
        Raises:
            requests.exceptions.RequestException: If the HTTP request to the face recognition API fails.
        Workflow:
            1. Retrieves the company information.
            2. Constructs the API request payload and headers.
            3. Sends a POST request to the face recognition API.
            4. Processes the API response to determine the employee's identity and similarity score.
            5. If the similarity score is above the threshold, sends a check-out request for the identified employee.
            6. Returns the status, code, and response message based on the outcome of the check-out request.
        Response Codes:
            200: Success - The check-out request was processed successfully.
            404: Not Found - The employee was not found or the similarity score was insufficient.
            500: Error - The request to the face recognition API failed.
        """
        company_id = self.env["res.company"].search([], limit=1)
        status = ""
        code = 0
        response_msg = []
        emp_img = args[0]
        if emp_img:
            url = f"http://{company_id.face_recog_url}/api/v1/recognition/recognize"
            payload = json.dumps({"file": emp_img})
            headers = {
                "Content-Type": "application/json",
                "x-api-key": company_id.face_recog_token,
            }

            try:
                response = requests.post(url, data=payload, headers=headers)
                response.raise_for_status()
                dict_data = response.json()
            except requests.exceptions.RequestException as e:
                return self.post_response(
                    status="Error",
                    code=500,
                    return_list=[{"response": f"Request failed: {str(e)}"}],
                )

            subject = dict_data["result"][0]["subjects"][0]["subject"]
            similarity = dict_data["result"][0]["subjects"][0]["similarity"]
            if subject:
                if similarity >= 0.9:
                    emp_id = self.get_id_from_subject(raw_subject=str(subject))
                    res = self.check_out_request(int(emp_id))

                    status = res[0]["status"]
                    code = res[0]["code"]
                    response_msg.append(
                        {
                            "response": f"{res[0]['list'][0]['response']}",
                        }
                    )
                else:
                    status = "Not Founded"
                    code = 404
                    response_msg.append(
                        {
                            "response": "similarity in not stasfied \n نسبة التشابه غير كافية",
                        }
                    )
            else:
                status = "Not Founded"
                code = 404
                response_msg.append(
                    {
                        "response": "There's no employee \n لا يوجد موظف",
                    }
                )

        else:
            status = "Not Founded"
            code = 404
            response_msg.append(
                {
                    "response": "There's no image \n لا يوجد صورة",
                }
            )

        return self.post_response(status=status, code=code, return_list=response_msg)
