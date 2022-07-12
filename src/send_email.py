import smtplib, ssl
from constants import PROVIDERS
from loguru import logger


def send_weather_report(
        number: str,
        message: str,
        provider: str,
        sender_credentials: tuple,
        subject: str = "WM",
        smtp_server: str = 'smtp.gmail.com',
        smtp_port: int = 465):
    sender_email, sender_password = sender_credentials
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'

    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, sender_password)
        email.sendmail(sender_email, receiver_email, email_message)
    logger.success(f'Weather report successfully sent to recipient {receiver_email}')


if __name__ == "__main__":
    from config import NUM, SENDER_CREDENTIALS
    message = "Hola mate"
    provider = "Verizon"
    send_weather_report(NUM, message, provider, SENDER_CREDENTIALS)