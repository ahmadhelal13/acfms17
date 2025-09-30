# -*- coding: utf-8 -*-
# ===========================================================#
# @Author:    Ahmed Mokhtar
# @Date:      2025-01-01
# @File:      attendance_call.py
# @Desc:
# desc :     EmployeeInherit class extends the hr.employee model to integrate with a face recognition API.
#    Methods:
#        get_image_in_base64(employee_id):
#       create_user():
#       update_user():
#       create_all_users():
#       delete_user():
#       unlink():
# ======================================================#

import json
import re
import requests
from odoo import _, models
from odoo.exceptions import UserError


class EmployeeInherit(models.Model):
    _inherit = "hr.employee"

    def get_image_in_base64(self, employee_id):
        """
        Retrieve the image of an employee in base64 format.

        Args:
            employee_id (int): The ID of the employee whose image is to be retrieved.

        Returns:
            str: The employee's image in base64 encoded string format.
        """
        employee = self.env["hr.employee"].browse(employee_id)
        image_emp_bytes = employee.image_1920.decode("utf-8")
        return image_emp_bytes

    def create_user(self):
        """
        Creates a user by sending a POST request to the face recognition API with the employee's image.

        This method retrieves the company information, constructs the API URL, and sends the employee's image
        in base64 format to the face recognition API. It handles the response and raises appropriate errors
        if the request fails.

        Raises:
            UserError: If the request to the face recognition API fails or an unexpected error occurs.

        Returns:
            None
        """
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
                    f"{url}?subject={subject_id}", data=payload, headers=headers
                )
                response.raise_for_status()  # Raise an exception for HTTP errors
                dict_data = response.json()
                print(f"Response: {dict_data}")
            except requests.exceptions.RequestException as e:
                raise UserError(
                    f"Request failed: {str(e)}\nResponse: {response.text if response else 'No response'}"
                )
            except Exception as e:
                raise UserError(f"An unexpected error occurred: {str(e)}")

    # def update_user(self):
    #     """
    #     Updates the user's face recognition data by sending a POST request to the face recognition API.

    #     This method retrieves the company information, constructs the API URL, and sends the user's image
    #     in base64 format to the face recognition service. It handles the response and raises appropriate
    #     errors if the request fails.

    #     Raises:
    #         UserError: If the request to the face recognition API fails or an unexpected error occurs.

    #     Exceptions:
    #         requests.exceptions.RequestException: Raised for HTTP errors during the API request.
    #         Exception: Raised for any other unexpected errors.

    #     """
    #     company_id = self.env["res.company"].search([], limit=1)
    #     if self.image_1920:
    #         url = f"http://{company_id.face_recog_url}/api/v1/recognition/faces"
    #         image = self.get_image_in_base64(employee_id=self.id)
    #         payload = json.dumps({"file": image})
    #         headers = {
    #             "Content-Type": "application/json",
    #             "x-api-key": f"{company_id.face_recog_token}",
    #         }
    #         subject_id = f"{self.name}(_{str(self.id)})"
    #         try:
    #             response = requests.post(
    #                 f"{url}?subject={subject_id}", data=payload, headers=headers
    #             )
    #             response.raise_for_status()  # Raise an exception for HTTP errors
    #             dict_data = response.json()
    #             print(f"Response: {dict_data}")
    #         except requests.exceptions.RequestException as e:
    #             raise UserError(
    #                 f"Request failed: {str(e)}\nResponse: {response.text if response else 'No response'}"
    #             )
    #         except Exception as e:
    #             raise UserError(f"An unexpected error occurred: {str(e)}")


    def update_user(self):
        """
        Updates the user's face recognition data by first checking if a record with the same ID exists.
        If found, updates the name and image; otherwise, creates a new record.

        Raises:
            UserError: If the request to the face recognition API fails or an unexpected error occurs.
        """
        self.delete_user()
        company_id = self.env["res.company"].search([], limit=1)
        if self.image_1920:
            # First, try to delete any existing record with the same ID (regardless of name)
            old_subject_id_pattern = f"(_\\{self.id})$"  # Pattern to match any name ending with (_id)
            url = f"http://{company_id.face_recog_url}/api/v1/recognition/faces"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": f"{company_id.face_recog_token}",
            }

            # Get list of all faces to find any existing records with this ID
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                existing_faces = response.json().get("faces", [])

                # Find any face with subject matching our ID pattern
                for face in existing_faces:
                    if re.search(old_subject_id_pattern, face.get("subject", "")):
                        # Delete the old record
                        delete_url = f"{url}?subject={face['subject']}"
                        requests.delete(delete_url, headers=headers)
                        break

            except requests.exceptions.RequestException as e:
                # If we can't check existing faces, proceed anyway (might be first creation)
                pass

            # Now create/update the record with current name and image
            image = self.get_image_in_base64(employee_id=self.id)
            payload = json.dumps({"file": image})

            # Handle name in English and Arabic languages
            if re.search(r"[\u0600-\u06FF]", self.name):
                updated_name = re.sub(r"[^A-Za-z\u0600-\u06FF]", "", self.name)
            else:
                updated_name = re.sub(r"[^A-Za-z]", "", self.name)
            subject_id = f"{updated_name}(_{str(self.id)})"

            try:
                response = requests.post(f"{url}?subject={subject_id}", data=payload, headers=headers)
                response.raise_for_status()
                dict_data = response.json()
                print(f"Response: {dict_data}")
            except requests.exceptions.RequestException as e:
                raise UserError(f"Request failed: {str(e)}\nResponse: {response.text if response else 'No response'}")
            except Exception as e:
                raise UserError(f"An unexpected error occurred: {str(e)}")
    def create_all_users(self):
        """
        Creates user records for all employees by sending their images to a face recognition API.

        This method performs the following steps:
        1. Retrieves the company information.
        2. Searches for all employee records.
        3. For each employee with a name and image:
            a. Constructs the URL for the face recognition API.
            b. Converts the employee's image to a base64 string.
            c. Prepares the payload and headers for the API request.
            d. Updates the employee's name to remove non-alphabetic characters.
            e. Constructs a subject ID using the updated name and employee ID.
            f. Sends a POST request to the face recognition API with the image and subject ID.
            g. Handles the API response and prints the response data.
            h. Catches and handles any request exceptions or unexpected errors.

        Raises:
            UserError: If an unexpected error occurs during the API request.

        Note:
            This method assumes that the company information contains the `face_recog_url` and `face_recog_token` fields.
        """
        company_id = self.env["res.company"].search([], limit=1)
        employees = self.search([])
        for rec in employees:
            if rec.name and rec.image_1920:
                url = f"http://{company_id.face_recog_url}/api/v1/recognition/faces"
                image = self.get_image_in_base64(employee_id=rec.id)
                payload = json.dumps({"file": image})
                headers = {
                    "Content-Type": "application/json",
                    "x-api-key": f"{company_id.face_recog_token}",
                }
                # Handle name in English and Arabic languages
                if re.search(r'[\u0600-\u06FF]', rec.name):
                    updated_name = re.sub(r"[^A-Za-z\u0600-\u06FF]", "", rec.name)
                else:
                    updated_name = re.sub(r"[^A-Za-z]", "", rec.name)
                subject_id = f"{updated_name}(_{str(rec.id)})"

                response = None
                try:
                    response = requests.post(
                        f"{url}?subject={subject_id}", data=payload, headers=headers
                    )
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    dict_data = response.json()
                    print(f"Response: {dict_data}")
                except requests.exceptions.RequestException as e:
                    pass
                except Exception as e:
                    raise UserError(f"An unexpected error occurred: {str(e)}")

    def delete_user(self):
        """
        Deletes a user from the face recognition system.

        This method sends a DELETE request to the face recognition API to remove a user based on their name and ID.

        Raises:
            UserError: If the request fails or an unexpected error occurs.

        Exceptions:
            requests.exceptions.RequestException: If there is an issue with the HTTP request.
            Exception: For any other unexpected errors.
        """
        company_id = self.env["res.company"].search([], limit=1)
        url = f"http://{company_id.face_recog_url}/api/v1/recognition/faces"
        subject_id = f"{self.name}(_{str(self.id)})"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": f"{company_id.face_recog_token}",
        }

        response = None
        try:
            # Sending DELETE request
            response = requests.delete(f"{url}?subject={subject_id}", headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Handling the response
            if response.status_code == 200:
                dict_data = response.json()
                print(f"User deleted successfully: {dict_data}")
            else:
                raise UserError(
                    f"Failed to delete user. Status code: {response.status_code}, Response: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            raise UserError(
                f"Request failed: {str(e)}\nResponse: {response.text if response else 'No response'}"
            )
        except Exception as e:
            raise UserError(f"An unexpected error occurred: {str(e)}")

        return response.status_code

    def unlink(self):
        """
        Overrides the unlink method to perform additional operations when an employee record is deleted.

        This method first calls the superclass's unlink method to delete the employee record.
        If the deletion is successful, it then calls the delete_user method to perform any
        additional cleanup related to the user associated with the employee.

        Returns:
            bool: True if the record was successfully deleted, False otherwise.
        """

        if self.delete_user() == 200:
            return super(EmployeeInherit, self).unlink()
        else:
            return False
