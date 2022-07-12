import weather
import send_email
from loguru import logger


if __name__ == "__main__":

    weather_report = weather.generate_weather_report()
    logger.success(weather_report)

    from config import NUM, SENDER_CREDENTIALS
    provider = "Verizon"
    send_email.send_weather_report(NUM, weather_report, provider, SENDER_CREDENTIALS)

