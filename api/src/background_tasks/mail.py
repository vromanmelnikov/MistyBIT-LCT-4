import requests

from src.config import CeleryConnection, settings
from src.phrases import SEND_FAILED


class MailService:
    def send(self, path: str, **kwargs):
        try:
            result = requests.get(f"{settings.URL_MAILER}/{path}", kwargs)
            print(result)
            if result.status_code != 200:
                print(SEND_FAILED)
            else:
                print(result.text)
            return result
        except Exception as e:
            print(e)


mailer_core = MailService()


@CeleryConnection.task
def send_url(email: str, url: str):
    mailer_core.send("reset_password", email=email, url=url)


@CeleryConnection.task
def send_greeting(email: str, url: str, name: str | None = None):
    mailer_core.send("greeting", email=email, url=url, name=name)


@CeleryConnection.task
def send_warn_signin(email: str):
    mailer_core.send("warning_signin", email=email)


@CeleryConnection.task
def send_any_message(email: str, message: str):
    mailer_core.send("any_message", email=email, message=message)
