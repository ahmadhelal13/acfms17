from odoo import models, api
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(name_)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def print_custom_report(self):
        """Prints the report with the report_name 's' for the current Sale Order."""
        self.ensure_one()  # Ensure that the method is called on a single record

        # Define the report name; adjust this as per your actual report's technical name
        report_name = "s"

        # Find the report action based on the report_name
        report_action = self.env["ir.actions.report"].search(
            [("report_name", "=", report_name)], limit=1
        )
        raise UserError(
            f"Report '{report_action}.,,,,, {report_action.id}.,,, {report_action.name} \n {report_action.data}"
        )
        if not report_action:
            raise UserError(
                f"Report '{report_name}' not found. Please check the report configuration."
            )

        try:
            # Fetch the report action reference
            report_ref = self.env.ref(report_action.xml_id)
            if not report_ref:
                raise UserError(
                    f"Report action '{report_action.xml_id}' could not be found or referenced."
                )

            # Attempt to generate the report
            report_data = report_ref.report_action(self)

            # Debugging the structure of report_data
            _logger.info(f"Report Data Type: {type(report_data)}")
            _logger.info(f"Report Data Content: {report_data}")

            # Check if report_data is a dictionary as expected
            if isinstance(report_data, dict):
                # Directly return if report_data matches expected structure
                if "data" in report_data and "file_type" in report_data:
                    _logger.info(
                        "Report generated successfully with correct structure."
                    )
                    return report_data
                else:
                    # Report structure does not match expected keys
                    _logger.error(
                        "Unexpected format: Report data does not contain expected keys."
                    )
                    raise UserError(
                        "Unexpected report format: missing 'data' or 'file_type'."
                    )

            # If report_data is not a dictionary, handle unexpected structure
            _logger.error(
                "Unexpected report structure encountered. Review report generation process."
            )

            # Attempt to unpack if report_data is an iterable but not a dictionary
            try:
                unpacked_data = tuple(
                    report_data
                )  # Convert to tuple to safely check structure
                if len(unpacked_data) == 2:
                    data, file_type = unpacked_data
                    _logger.info(
                        f"Successfully unpacked: Data: {data}, File Type: {file_type}"
                    )
                    return {
                        "data": data,
                        "file_type": file_type,
                    }  # Modify as needed to fit your workflow
                else:
                    _logger.error(
                        f"Unexpected number of elements: expected 2, got {len(unpacked_data)}"
                    )
                    raise UserError(
                        f"Unexpected data structure: expected 2 elements, got {len(unpacked_data)}."
                    )
            except Exception as unpack_error:
                _logger.error("Error unpacking report data: %s", str(unpack_error))
                raise UserError(f"Error unpacking the report data: {str(unpack_error)}")

        except Exception as e:
            _logger.error("Error printing the report: %s", str(e))
            raise UserError(f"Error printing the report: {str(e)}")


#     def generate_pdf_report(self):
#         for record in self:
#             if not record.partner_id.whatsapp:
#                 raise UserError("No WhatsApp number to send the message to.")

#             # Find the report action by its report name
#             report_action = self.env['ir.actions.report'].search([('report_name', '=', 's')], limit=1)
#             if not report_action:
#                 raise UserError("Report not found. Check the report name and its configuration.")

#             try:
#                 # Get the report object
#                 report = self.env.ref(report_action.report_name)

#                 # Generate PDF using the report object
#                 pdf_result = report.render_qweb_pdf(self.ids)

#                 # Handle the PDF content correctly
#                 if isinstance(pdf_result, bytes):
#                     pdf_content = pdf_result
#                 elif isinstance(pdf_result, tuple) and len(pdf_result) == 2:
#                     pdf_content, _ = pdf_result
#                 else:
#                     raise UserError("Unexpected return type from render_qweb_pdf method.")

#                 # Ensure that pdf_content is in bytes format
#                 if not isinstance(pdf_content, bytes):
#                     raise UserError("The generated content is not a PDF file.")

#                 # Log the content size and type for debugging
#                 _logger.info("Generated PDF size: %d bytes", len(pdf_content))

#                 return pdf_content

#             except Exception as e:
#                 _logger.error("Error generating PDF report: %s", str(e))
#                 raise UserError(f"Error generating the PDF report: {str(e)}")

#     def send_pdf_report_via_whatsapp(self):
#         for record in self:
#             if not record.partner_id.whatsapp:
#                 raise UserError("No WhatsApp numbers to send messages to.")

#             # Fetch the WhatsApp server configuration
#             whatsapp_server = self.env['ir.whatsapp_server'].search([], limit=1)
#             if not whatsapp_server:
#                 raise UserError("WhatsApp server configuration not found.")

#             whatsapp_api_url = whatsapp_server.whatsapp_api_url
#             whatsapp_api_instance = whatsapp_server.whatsapp_api_instance
#             whatsapp_api_token = whatsapp_server.whatsapp_api_token

#             # Generate the PDF report
#             try:
#                 pdf_content = self.generate_pdf_report()
#                 if not isinstance(pdf_content, bytes):
#                     raise UserError("Report content is not in the expected format (binary).")

#                 # Save the file to a temporary location
#                 with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
#                     temp_file.write(pdf_content)
#                     temp_file_path = temp_file.name

#             except Exception as e:
#                 raise UserError(f"Error generating the PDF report: {str(e)}")

#             # Send the PDF file via WhatsApp
#             for partner in record.partner_id:
#                 whatsapp_list = partner.whatsapp.split(', ')
#                 for number in whatsapp_list:
#                     try:
#                         api_url = f"{whatsapp_api_url}/{whatsapp_api_instance}/send-file-base64"

#                         # Guess the MIME type of the PDF file
#                         mimetype, _ = mimetypes.guess_type(temp_file_path)
#                         if mimetype is None:
#                             mimetype = 'application/pdf'

#                         with open(temp_file_path, 'rb') as file_data:
#                             base64_content = base64.b64encode(file_data.read()).decode('utf-8')
#                             str_mimetype = 'data:' + mimetype + ';base64,'
#                             attachment = str_mimetype + base64_content

#                         message_data = {
#                             "phone": number,
#                             "base64": attachment,
#                             "caption": "Here is your PDF document.",
#                             "filename": temp_file_path.split('/')[-1]
#                         }

#                         headers = {
#                             "Accept": "application/json",
#                             "Content-Type": "application/json",
#                             "Authorization": f"Bearer {whatsapp_api_token}"
#                         }
#                         response = requests.post(api_url, data=json.dumps(message_data), headers=headers)

#                         if response.status_code in [200, 201]:
#                             _logger.info("PDF report sent successfully to %s", number)
#                         else:
#                             _logger.error("Failed to send PDF report to %s. Status code: %s", number, response.status_code)
#                             _logger.debug("Response: %s", response.text)

#                     except Exception as e:
#                         _logger.error("Error sending PDF report to %s: %s", number, str(e))
