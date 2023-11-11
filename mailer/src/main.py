from fastapi import FastAPI, Query
from pydantic import EmailStr
from jinja2 import Template

from src.config import settings
from src.const import *
from src.schemas import MessageSchema
from src.sender import createServer, post


serverSMTP = createServer()

app = FastAPI()


@app.get("/reset_password/")
async def root(email: EmailStr, url: str):
    html = open(settings.PATH_TEMPLATE, encoding="utf-8").read()
    template = Template(html)
    if serverSMTP is not None:
        res = post(
            serverSMTP,
            settings.EMAIL_SENDER,
            email,
            template.render(
                logo=settings.LOGO_URL,
                header="Восстановление пароля",
                reason="запросили сброс пароля для своей учетной записи Mistybit.",
                message="Нажмите кнопку ниже, чтобы сменить пароль.",
                button_name="Восстановить",
                url=url,
                company_name=COMPANY_NAME,
            ),
            SUBJECT_RECOVER_PASSWORD,
            settings.PASSWORD,
        )
        return res if res else MessageSchema(mailer_result=SUCCSESS)
    return MessageSchema(mailer_result=FAILDED)


@app.get("/warning_signin/")
async def root(email: EmailStr):
    html = open(settings.PATH_TEMPLATE, encoding="utf-8").read()
    template = Template(html)
    if serverSMTP is not None:
        res = post(
            serverSMTP,
            settings.EMAIL_SENDER,
            email,
            template.render(
                logo=settings.LOGO_URL,
                header=f"{WARNING}!",
                reason="кто-то вошел на ваш аккаунт на платформе Mistybit.",
                company_name=COMPANY_NAME,
            ),
            SUBJECT_SIGNIN,
            settings.PASSWORD,
        )
        return res if res else MessageSchema(mailer_result=SUCCSESS)
    return MessageSchema(mailer_result=FAILDED)


@app.get("/greeting/")
async def root(email: EmailStr, url: str, name: str | None = Query(default=None)):
    html = open(settings.PATH_TEMPLATE, encoding="utf-8").read()
    template = Template(html)
    if serverSMTP is not None:
        res = post(
            serverSMTP,
            settings.EMAIL_SENDER,
            email,
            template.render(
                logo=settings.LOGO_URL,
                header=f"Добро пожаловать{', ' if name else ''} {name if name else ''}!",
                reason="вы зарегистрировались на платформе Mistybit. Нажмите кнопку ниже, чтобы активировать учетную запись",
                button_name="Активировать",
                url=url,
                company_name=COMPANY_NAME,
            ),
            SUBJECT_GREETING,
            settings.PASSWORD,
        )
        return res if res else MessageSchema(mailer_result=SUCCSESS)
    return MessageSchema(mailer_result=FAILDED)


@app.get("/any_message/")
async def root(email: EmailStr, message: str):
    html = open(settings.PATH_TEMPLATE, encoding="utf-8").read()
    template = Template(html)
    if serverSMTP is not None:
        res = post(
            serverSMTP,
            settings.EMAIL_SENDER,
            email,
            template.render(
                logo=settings.LOGO_URL,
                header="Уведомление!",
                reason="вам пришло сообщение с платформы Mistybit.",
                message=message,
                company_name=COMPANY_NAME,
            ),
            MESSAGE,
            settings.PASSWORD,
        )
        return res if res else MessageSchema(mailer_result=SUCCSESS)
    return MessageSchema(mailer_result=FAILDED)
