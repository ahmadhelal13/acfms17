import json

import requests
from odoo import _, models
from odoo.exceptions import UserError


class EmployeeInherit(models.Model):
    _inherit = "hr.employee"

    def get_image_in_base64(self, employee_id):
        employee = self.env['hr.employee'].browse(employee_id)
        image_emp_bytes = employee.image_1920.decode("utf-8")
        return image_emp_bytes

    def create_user(self):
        company_id = self.env["res.company"].search([], limit=1)
        if self.name and self.image_1920:
            url = f"http://{company_id.face_recog_url}/api/v1/recognition/faces"
            image = self.get_image_in_base64(employee_id=self.id)
            payload = json.dumps({"file": image})
            headers = {
                "Content-Type": "application/json",
                "x-api-key": f"{company_id.face_recog_token}",
            }
            subject_id = f"{self.name}(_{str(self.id)})"
            response = None
            try:
                response = requests.post(
                    f"{url}?subject={subject_id}", data=payload, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors
                dict_data = response.json()
                print(f'Response: {dict_data}')
            except requests.exceptions.RequestException as e:
                raise UserError(
                    f"Request failed: {str(e)}\nResponse: {response.text if response else 'No response'}")
            except Exception as e:
                raise UserError(f"An unexpected error occurred: {str(e)}")

    def update_user(self):
        company_id = self.env["res.company"].search([], limit=1)
        if self.image_1920:
            url = f"http://{company_id.face_recog_url}/api/v1/recognition/faces"
            image = self.get_image_in_base64(employee_id=self.id)
            payload = json.dumps({"file": image})
            headers = {
                "Content-Type": "application/json",
                "x-api-key": f"{company_id.face_recog_token}",
            }
            subject_id = f"{self.name}(_{str(self.id)})"
            try:
                response = requests.post(
                    f"{url}?subject={subject_id}", data=payload, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors
                dict_data = response.json()
                print(f'Response: {dict_data}')
            except requests.exceptions.RequestException as e:
                raise UserError(
                    f"Request failed: {str(e)}\nResponse: {response.text if response else 'No response'}")
            except Exception as e:
                raise UserError(f"An unexpected error occurred: {str(e)}")
