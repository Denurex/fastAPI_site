# from email.message import EmailMessage
#
# from pydantic import EmailStr
# import smtplib
# from config import settings
# from tasks.celeryy import celery_app
#
#
# def create_booking_confirm_template(booking:dict,
#                                     email_to:EmailStr):
#     email = EmailMessage()
#
#     email['Subject'] = "Confirm booking"
#     email["From"] = settings.SMTP_USER
#     email['To'] = email_to
#
#     email.set_content(
#         f'''
#             <h1>Conf booking</h1>
#             {booking['date_from']}
#         '''
#     )
#
#
# @celery_app.task
# def send_booking_confirmation(booking:dict,
#                               email_to:EmailStr):
#     msg_content = create_booking_confirm_template(booking,email_to)
#
#     with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
#         server.login(settings.SMTP_USER, settings.SMTP_PASS)
#         server.send(msg_content)