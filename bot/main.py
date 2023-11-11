import datetime
from datetime import datetime

import telebot
from telebot import types

import utils
import components
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

user_states = {}
user_tokens = {}
user_rtokens = {}
role = {}
login = {}


@bot.message_handler(commands=["start"])
def start_func(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в телеграмм-бот для выездных сотрудников банка!",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    auth(message.chat.id)


def auth(chat_id):
    bot.send_message(
        chat_id,
        "Авторизуйтесь, чтобы продолжить.\nУкажите Ваш адрес электронной почты, указанный в системе:",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    user_states[chat_id] = "waiting_for_login"


def to_go(chat_id):
    if chat_id in role:
        if role[chat_id] == 1:
            go(chat_id)
        elif role[chat_id] == 2:
            go_manager(chat_id)
    else:
        auth(chat_id)


def go(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Список задач")
    btn2 = types.KeyboardButton("Профиль")
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(chat_id, "Выберите категорию:", reply_markup=markup)


def go_manager(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сотрудники")
    btn2 = types.KeyboardButton("Все задачи")
    btn3 = types.KeyboardButton("Филиалы")
    btn4 = types.KeyboardButton("Профиль")
    markup.row(btn1, btn2)
    markup.add(btn3, btn4)
    bot.send_message(chat_id, "Выберите категорию:", reply_markup=markup)


def check_role(message):
    if message.chat.id in role:
        if role[message.chat.id] == 1:
            return 1
        elif role[message.chat.id] == 2:
            return 2


@bot.message_handler(func=lambda message: message.text == "Сотрудники")
def show_emps(message):
    if check_role(message) == 1:
        return
    msg = message
    if message.chat.id in user_tokens:
        curr_token = user_tokens[message.chat.id]
    else:
        # TODO: нужен global или нет?
        user_rtokens[message.chat.id] = None
        user_tokens[message.chat.id] = None
        auth(msg.chat.id)
        return
    response = utils.users_employees_all(curr_token)

    if response.status_code == 200:
        response_data = response.json()
        counter = 0
        text_msg = ""
        bot.send_message(message.chat.id, "Актуальный список сотрудников:")
        for item in response_data["items"]:
            # if item['user']['is_active']==True:
            #     stat = '🟢'
            # else:
            #     stat = '⚪'
            text_msg += f"*{item['user']['lastname']} {item['user']['firstname']} {item['user']['patronymic']}* ({item['grade']['name']})\n📍_{item['office']['address']}_\n\n"
            if counter == 10:
                counter = 0
                bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")
                text_msg = ""
            else:
                counter += 1
        if counter != 0:
            bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")

        to_go(msg.chat.id)
    elif (
        response.status_code == 401
        and response.json()["detail"] == "Срок действия токена истек"
    ):
        bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
        refresh(msg)
        show_emps(msg)
    else:
        error_data = response.json()
        print(error_data["detail"])

        bot.send_message(message.chat.id, f"Произошла ошибка.")
        to_go(msg.chat.id)


@bot.message_handler(func=lambda message: message.text == "Филиалы")
def show_points(message):
    if check_role(message) == 1:
        return
    msg = message
    if message.chat.id in user_tokens:
        curr_token = user_tokens[message.chat.id]
    else:
        user_rtokens[message.chat.id] = None
        user_tokens[message.chat.id] = None
        auth(msg.chat.id)
        return
    response = utils.offices_all(curr_token)

    if response.status_code == 200:
        response_data = response.json()
        counter = 0
        text_msg = ""
        for item in response_data["items"]:
            text_msg += f"📍{item['address']}\n\n"
            if counter == 10:
                counter = 0
                bot.send_message(message.chat.id, text_msg)
                text_msg = ""
            else:
                counter += 1
        if counter != 0:
            bot.send_message(message.chat.id, text_msg)

        to_go(msg.chat.id)
    elif (
        response.status_code == 401
        and response.json()["detail"] == "Срок действия токена истек"
    ):
        bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
        refresh(msg)
        show_emps(msg)
    else:
        error_data = response.json()
        print(error_data["detail"])

        bot.send_message(message.chat.id, f"Произошла ошибка.")
        to_go(msg.chat.id)


@bot.message_handler(func=lambda message: message.text == "Все задачи")
def show_all_tasks(message):
    if check_role(message) == 1:
        return
    msg = message
    if message.chat.id in user_tokens:
        curr_token = user_tokens[message.chat.id]
    else:
        user_rtokens[message.chat.id] = None
        user_tokens[message.chat.id] = None
        auth(msg.chat.id)
        return
    response = utils.tasks()

    if response.status_code == 200:
        response_data = response.json()
        counter = 0
        text_msg = ""
        for num, item in enumerate(response_data["items"]):
            if item["priority"]["value"] == 3:
                emoji_status = "⚠️"
            else:
                emoji_status = ""
            if (
                item.get("employee")
                and item["employee"].get("user")
                and item["employee"]["user"].get("lastname")
            ):
                emp = f"{item['employee']['user']['lastname']} {item['employee']['user']['firstname']} {item['employee']['user']['patronymic']}"
            else:
                emp = "не назначен"
            text_msg += f"*Задача #: {item['id']}* ({str(item['status']['name']).lower()}) {emoji_status}\n{item['type']['name']}\n{item['priority']['name']} приоритет\nИсполнитель: {emp}\n📍_{item['point']['address']}_\n\n"
            if counter == 5:
                counter = 0
                bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")
                text_msg = ""
            else:
                counter += 1
        if counter != 0:
            bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")

        btn1 = types.KeyboardButton("Архив всех задач")
        markup = components.add_btns(2, [btn1])
        bot.send_message(message.chat.id, "Далее...", reply_markup=markup)
    elif (
        response.status_code == 401
        and response.json()["detail"] == "Срок действия токена истек"
    ):
        bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
        refresh(msg)
        show_emps(msg)
    elif (
        response.status_code == 404
        and response.json()["detail"] == "Объекты не найдены"
    ):
        bot.send_message(message.chat.id, f"На данный момент задач нет.")
        btn1 = types.KeyboardButton("Архив всех задач")
        markup = components.add_btns(2, [btn1])
        bot.send_message(message.chat.id, "Далее...", reply_markup=markup)
    else:
        error_data = response.json()
        print(error_data["detail"])

        bot.send_message(message.chat.id, f"Произошла ошибка.")
        to_go(msg.chat.id)


@bot.message_handler(func=lambda message: message.text == "Список задач")
def show_tasks(message):
    if check_role(message) == 2:
        return
    msg = message
    if message.chat.id in user_tokens:
        curr_token = user_tokens[message.chat.id]
    else:
        user_rtokens[message.chat.id] = None
        user_tokens[message.chat.id] = None
        auth(msg.chat.id)
        return
    response = utils.users_profile(curr_token)
    if response.status_code == 200:
        response = utils.tasks_id(response.json()["id"])
        if response.status_code == 200:
            response_data = response.json()
            counter = 0
            text_msg = ""
            for item in response_data["items"]:
                if item["priority"]["value"] == 3:
                    emoji_status = "⚠️"
                else:
                    emoji_status = ""

                text_msg += f"*Задача #: {item['id']}* {emoji_status}\n{item['type']['name']}\n{item['priority']['name']} приоритет\n📍_{item['point']['address']}_\n\n"
                if counter == 5:
                    counter = 0
                    bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")
                    text_msg = ""
                else:
                    counter += 1
            if counter != 0:
                bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("Текущая задача")
            markup.row(btn1)
            btn2 = types.KeyboardButton("Архив задач")
            btn3 = types.KeyboardButton("На главную")
            markup.row(btn2, btn3)
            bot.send_message(message.chat.id, "Далее...", reply_markup=markup)
        elif (
            response.status_code == 401
            and response.json()["detail"] == "Срок действия токена истек"
        ):
            bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
            refresh(msg)
            show_emps(msg)
        elif (
            response.status_code == 404
            and response.json()["detail"] == "Объекты не найдены"
        ):
            bot.send_message(message.chat.id, f"На данные момент задач нет.")
            btn1 = types.KeyboardButton("Архив задач")
            markup = components.add_btns(2, [btn1])
            bot.send_message(message.chat.id, "Далее...", reply_markup=markup)
        else:
            error_data = response.json()
            print(error_data["detail"])

            bot.send_message(message.chat.id, f"Произошла ошибка.")
            to_go(msg.chat.id)
    elif (
        response.status_code == 401
        and response.json()["detail"] == "Срок действия токена истек"
    ):
        bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
        refresh(msg)
        get_req_profile(msg)
    else:
        error_data = response.json()
        print(error_data["detail"])

        bot.send_message(message.chat.id, f"Произошла ошибка.")
        to_go(msg.chat.id)


@bot.message_handler(func=lambda message: message.text == "Архив всех задач")
def archieve_all(message):
    if check_role(message) == 1:
        return
    if message.chat.id in user_tokens:
        curr_token = user_tokens[message.chat.id]
    else:
        user_rtokens[message.chat.id] = None
        user_tokens[message.chat.id] = None
        auth(message.chat.id)
        return
    response = utils.tasks_history()
    if response.status_code == 200:
        response_data = response.json()
        counter = 0
        text_msg = ""
        for num, item in enumerate(response_data["items"]):
            if (
                item.get("employee")
                and item["employee"].get("id")
                and item["employee"]["id"].get("lastname")
            ):
                emp = f"{item['employee']['id']['lastname']} {item['employee']['id']['firstname']} {item['employee']['id']['patronymic']}"
            else:
                emp = "не назначен"
            if item["feedback_value"] == None:
                mark = False
            else:
                mark = True
            if item["feedback_description"] == "":
                review = False
            else:
                review = True
            if item["date_begin"] == None:
                is_dated = False
            else:
                is_dated = True
            text_msg += f"*Задача #: {item['id']}*"
            if is_dated == True:
                text_msg += f"        _{datetime.strptime(item['date_begin'], '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M')}_"
            text_msg += f"\n{item['type']['name']}\nИсполнитель: {emp}"
            if mark == True:
                text_msg += f"\nОценка: "
                for i in range(int(item["feedback_value"])):
                    text_msg += "⭐"
            if review == True:
                text_msg += f"\nОтзыв сотрудника: \"{item['feedback_description']}\""
            text_msg += f"\n📍_{item['point']['address']}_\n\n"
            # text_msg += f"Задача #: {item['id']}\n{item['type']['name']}\n{item['point']['address']}\n{item['priority']['name']} приоритет\n{item['status']['name']} в данный момент\nИсполнитель: {item['employee']['user']['lastname']} {item['employee']['user']['firstname']} {item['employee']['user']['patronymic']}\n\n"
            if counter == 5:
                counter = 0
                bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")
                text_msg = ""
            else:
                counter += 1
        if counter != 0:
            bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")

        to_go(message.chat.id)

    else:
        error_data = response.json()
        print(error_data["detail"])
        bot.send_message(message.chat.id, "Произошла ошибка", parse_mode="Markdown")


@bot.message_handler(func=lambda message: message.text == "Архив задач")
def archieve(message):
    msg = message
    if check_role(message) == 2:
        return
    if message.chat.id in user_tokens:
        curr_token = user_tokens[message.chat.id]
    else:
        user_rtokens[message.chat.id] = None
        user_tokens[message.chat.id] = None
        auth(message.chat.id)
        return
    response = utils.users_profile(curr_token)
    response_res = response.json()["id"]
    if response.status_code == 200:
        response = utils.tasks_history_id(response_res)
        if response.status_code == 200:
            response_data = response.json()
            counter = 0
            text_msg = ""
            for num, item in enumerate(response_data["items"]):
                if item["feedback_value"] == 0 or item["feedback_value"] == None:
                    mark = False
                else:
                    mark = True
                if item["feedback_description"] == "":
                    review = False
                else:
                    review = True
                if item["date_begin"] == None:
                    is_dated = False
                else:
                    is_dated = True
                text_msg += f"*Задача #: {item['id']}*"
                if is_dated == True:
                    text_msg += f"        _{datetime.strptime(item['date_begin'], '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M')}_"
                text_msg += f"\n{item['type']['name']}"
                if mark == True:
                    text_msg += f"\nОценка: "
                    for i in range(int(item["feedback_value"])):
                        text_msg += "⭐"
                if review == True:
                    text_msg += (
                        f"\nОтзыв сотрудника: \"{item['feedback_description']}\""
                    )
                text_msg += f"\n📍_{item['point']['address']}_\n\n"
                if counter == 5:
                    counter = 0
                    bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")
                    text_msg = ""
                else:
                    counter += 1
            if counter != 0:
                bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")

            to_go(message.chat.id)

        else:
            error_data = response.json()
            print(error_data["detail"])
            bot.send_message(message.chat.id, "Произошла ошибка", parse_mode="Markdown")
    elif (
        response.status_code == 401
        and response.json()["detail"] == "Срок действия токена истек"
    ):
        bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
        refresh(msg)
        get_req_profile(msg)
    else:
        error_data = response.json()
        print(error_data["detail"])

        bot.send_message(message.chat.id, f"Произошла ошибка.")
        to_go(msg.chat.id)


@bot.message_handler(func=lambda message: message.text == "Текущая задача")
def current_activate(message):
    if check_role(message) == 2:
        return
    current(message)


def current(message):
    if check_role(message) == 2:
        return
    msg = message
    if message.chat.id in user_tokens:
        curr_token = user_tokens[message.chat.id]
    else:
        # TODO: нужен global или нет?
        user_rtokens[message.chat.id] = None
        user_tokens[message.chat.id] = None
        auth(msg.chat.id)
        return
    response = utils.users_profile(curr_token)
    if response.status_code == 200:
        response = utils.tasks_id(response.json()["id"])

        if response.status_code == 200:
            response_data = response.json()
            counter = 0

            for item in response_data["items"]:
                if item["priority"]["value"] == 3:
                    emoji_status = "⚠️"
                else:
                    emoji_status = ""
                if item["status"]["id"] == 4:
                    counter = 1
                    text_msg = f"*Задача #: {item['id']}* ({str(item['status']['name']).lower()}) {emoji_status}\n{item['type']['name']}\n{item['priority']['name']} приоритет\n📍_{item['point']['address']}_\n\n"
                    bot.send_message(message.chat.id, text_msg, parse_mode="Markdown")
            if counter == 0:
                bot.send_message(
                    message.chat.id,
                    "У Вас нет принятых задач.\n\nПримите одну задачу из Вашего списка задач, чтобы сделать её текущей.",
                    parse_mode="Markdown",
                )
                btn1 = types.KeyboardButton("Выбрать задачу")
                btn2 = types.KeyboardButton("Список задач")
                markup = components.add_btns(3, [btn1, btn2])
                bot.send_message(message.chat.id, "Далее...", reply_markup=markup)
            else:
                btn1 = types.KeyboardButton("Завершить")
                btn2 = types.KeyboardButton("Есть проблема")
                markup = components.add_btns(3, [btn1, btn2])
                bot.send_message(message.chat.id, "Далее...", reply_markup=markup)

    elif (
        response.status_code == 401
        and response.json()["detail"] == "Срок действия токена истек"
    ):
        bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
        refresh(msg)
        get_req_profile(msg)
    else:
        error_data = response.json()
        print(error_data["detail"])

        bot.send_message(message.chat.id, f"Произошла ошибка.")
        to_go(msg.chat.id)


@bot.message_handler(func=lambda message: message.text == "Есть проблема")
def choose_task(message):
    msg = message
    if check_role(message) == 2:
        return
    user_states[message.chat.id] = "waiting_for_problem"
    bot.send_message(
        message.chat.id, f"Опишите проблему:", reply_markup=types.ReplyKeyboardRemove()
    )


@bot.message_handler(func=lambda message: message.text == "Выбрать задачу")
def choose_task(message):
    if check_role(message) == 2:
        return
    user_states[message.chat.id] = "waiting_for_task"
    bot.send_message(
        message.chat.id,
        f"Укажите номер задачи, которую Вы хотите принять:",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.message_handler(func=lambda message: message.text == "Завершить")
def current_compl_t(message):
    msg = message
    if check_role(message) == 2:
        return
    if message.chat.id in user_tokens:
        curr_token = user_tokens[message.chat.id]
    else:
        user_rtokens[message.chat.id] = None
        user_tokens[message.chat.id] = None
        auth(msg.chat.id)
        return
    response = utils.users_profile(curr_token)
    if response.status_code == 200:
        response = utils.tasks_id(response.json()["id"])

        if response.status_code == 200:
            response_data = response.json()
            counter = 0

            for item in response_data["items"]:
                if item["status"]["id"] == 4:
                    counter = 1
                    temp = item["id"]
                    break
            if counter == 0:
                bot.send_message(
                    message.chat.id, "Произошла ошибка.", parse_mode="Markdown"
                )
                to_go(msg.chat.id)
            else:
                response = finish(int(temp), curr_token)
                if response.status_code == 200:
                    bot.send_message(
                        message.chat.id,
                        "Поздравляем Вас с завершением задачи!\nБлагодарим за Ваш труд!",
                        parse_mode="Markdown",
                    )
                else:
                    error_data = response.json()
                    print(error_data["detail"])

                    bot.send_message(message.chat.id, f"Произошла ошибка.")
                to_go(msg.chat.id)
        elif (
            response.status_code == 401
            and response.json()["detail"] == "Срок действия токена истек"
        ):
            bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
            refresh(msg)
            show_emps(msg)
        else:
            error_data = response.json()
            print(error_data["detail"])

            bot.send_message(message.chat.id, f"Произошла ошибка.")
            to_go(msg.chat.id)
    elif (
        response.status_code == 401
        and response.json()["detail"] == "Срок действия токена истек"
    ):
        bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
        refresh(msg)
        get_req_profile(msg)
    else:
        error_data = response.json()
        print(error_data["detail"])

        bot.send_message(message.chat.id, f"Произошла ошибка.")
        to_go(msg.chat.id)


def finish(id, token):
    response = utils.complete_task(id, token)
    return response


@bot.message_handler(func=lambda message: message.text == "На главную")
def to_main(message):
    to_go(message.chat.id)


@bot.message_handler(func=lambda message: message.text == "Профиль")
def profile_activate(message):
    get_req_profile(message)


def refresh(message):
    msg = message
    chat_id = message.chat.id
    if chat_id in user_rtokens:
        temp_token = user_rtokens[chat_id]
    else:
        # TODO: нужен global или нет?
        user_rtokens[chat_id] = None
        user_tokens[chat_id] = None
        auth(msg.chat.id)
        return
    response = utils.auth_refresh_token(temp_token)

    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
        user_tokens[message.chat.id] = access_token
        user_rtokens[message.chat.id] = refresh_token
        bot.send_message(message.chat.id, f"Токен обновлён.")
    else:
        error_data = response.json()
        print(error_data["detail"])

        bot.send_message(message.chat.id, f"Произошла ошибка.")
        auth(msg.chat.id)


def get_req_profile(message):
    msg = message
    if message.chat.id in user_tokens:
        curr_token = user_tokens[message.chat.id]
    else:
        auth(msg.chat.id)
        return

    response = utils.users_profile(curr_token)

    if response.status_code == 200:
        response_data = response.json()
        profile(message, response_data)
    elif (
        response.status_code == 401
        and response.json()["detail"] == "Срок действия токена истек"
    ):
        bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
        refresh(msg)
        get_req_profile(msg)
    else:
        error_data = response.json()
        print(error_data["detail"])

        bot.send_message(message.chat.id, f"Произошла ошибка.")
        to_go(msg.chat.id)


def profile(message, rdata):
    bot.send_message(
        message.chat.id,
        f'Фамилия: {rdata["lastname"]}\nИмя: {rdata["firstname"]}\nОтчество: {rdata["patronymic"]}\nEmail: {rdata["email"]}',
    )
    btn1 = types.KeyboardButton("Изменить данные")
    btn2 = types.KeyboardButton("Выйти из аккаунта")
    markup = components.add_btns(3, [btn1, btn2])
    bot.send_message(message.chat.id, "Далее...", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Изменить данные")
def edit_profile(message):
    bot.send_message(message.chat.id, "Выберите поле для редактирования:")
    btn1 = types.KeyboardButton("Изменить фамилию")
    btn2 = types.KeyboardButton("Изменить имя")
    btn3 = types.KeyboardButton("Изменить отчество")
    markup = components.add_btns(4, [btn1, btn2, btn3])
    bot.send_message(message.chat.id, "Далее...", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Выйти из аккаунта")
def out_profile(message):
    if message.chat.id in user_tokens:
        user_tokens[message.chat.id] = None
    else:
        print("error")
    bot.send_message(message.chat.id, "Вы вышли из аккаунта.")
    return auth(message.chat.id)


@bot.message_handler(func=lambda message: message.text == "Изменить фамилию")
def edit_profile_surname(message):
    user_states[message.chat.id] = "waiting_for_surname"
    bot.send_message(
        message.chat.id,
        "Укажите новую фамилию:",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.message_handler(func=lambda message: message.text == "Изменить имя")
def edit_profile_name(message):
    user_states[message.chat.id] = "waiting_for_name"
    bot.send_message(
        message.chat.id, "Укажите новое имя:", reply_markup=types.ReplyKeyboardRemove()
    )


@bot.message_handler(func=lambda message: message.text == "Изменить отчество")
def edit_profile_patr(message):
    user_states[message.chat.id] = "waiting_for_patr"
    bot.send_message(
        message.chat.id,
        "Укажите новое отчество:",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.message_handler(func=lambda message: True)
def login_func(message):
    # Проверяем текущее состояние пользователя
    if user_states.get(message.chat.id) == "waiting_for_login":
        login[message.chat.id] = message.text
        user_states[message.chat.id] = "waiting_for_password"
        bot.send_message(message.chat.id, "Введите Ваш пароль:")

    elif user_states.get(message.chat.id) == "waiting_for_password":
        msg = message
        password = message.text
        user_states[message.chat.id] = None
        bot.send_message(message.chat.id, "Спасибо!")

        response = utils.auth_signin(login[message.chat.id], password)
        login[message.chat.id] = None

        if response.status_code == 200:
            response_data = response.json()
            access_token = response_data["access_token"]
            refresh_token = response_data["refresh_token"]
            # token_type = response_data['token_type']

            role[message.chat.id] = utils.users_profile(access_token).json()["role_id"]
            bot.send_message(message.chat.id, f"Вы успешно вошли в аккаунт.")
            user_tokens[message.chat.id] = access_token
            user_rtokens[message.chat.id] = refresh_token

            to_go(message.chat.id)
        else:
            error_data = response.json()
            print(error_data["detail"])

            bot.send_message(message.chat.id, f"Произошла ошибка.")
            auth(msg.chat.id)

    elif user_states.get(message.chat.id) == "waiting_for_surname":
        msg = message
        if message.chat.id in user_tokens:
            curr_token = user_tokens[message.chat.id]
        else:
            auth(msg.chat.id)
            return

        response = utils.users_profile(curr_token)
        if response.status_code == 200:
            response = utils.users(
                response.json()["firstname"],
                message.text,
                response.json()["patronymic"],
                curr_token,
            )

            user_states[message.chat.id] = None
            if response.status_code == 200:
                bot.send_message(message.chat.id, f"Данные успешно изменены.")
                get_req_profile(msg)
            elif (
                response.status_code == 401
                and response.json()["detail"] == "Срок действия токена истек"
            ):
                bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
                refresh(msg)
                get_req_profile(msg)
            else:
                bot.send_message(message.chat.id, f"Произошла ошибка.")
                get_req_profile(msg)
        elif (
            response.status_code == 401
            and response.json()["detail"] == "Срок действия токена истек"
        ):
            bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
            refresh(msg)
            get_req_profile(msg)
        else:
            error_data = response.json()
            print(error_data["detail"])

            bot.send_message(message.chat.id, f"Произошла ошибка.")
            to_go(msg.chat.id)

    elif user_states.get(message.chat.id) == "waiting_for_name":
        msg = message
        if message.chat.id in user_tokens:
            curr_token = user_tokens[message.chat.id]
        else:
            auth(msg.chat.id)
            return

        response = utils.users_profile(curr_token)

        if response.status_code == 200:
            response = utils.users(
                message.text,
                response.json()["lastname"],
                response.json()["patronymic"],
                curr_token,
            )

            user_states[message.chat.id] = None
            if response.status_code == 200:
                bot.send_message(message.chat.id, f"Данные успешно изменены.")
                get_req_profile(msg)
            elif (
                response.status_code == 401
                and response.json()["detail"] == "Срок действия токена истек"
            ):
                bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
                refresh(msg)
                get_req_profile(msg)
            else:
                bot.send_message(message.chat.id, f"Произошла ошибка.")
                get_req_profile(msg)
        elif (
            response.status_code == 401
            and response.json()["detail"] == "Срок действия токена истек"
        ):
            bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
            refresh(msg)
            get_req_profile(msg)
        else:
            error_data = response.json()
            print(error_data["detail"])

            bot.send_message(message.chat.id, f"Произошла ошибка.")
            to_go(msg.chat.id)

    elif user_states.get(message.chat.id) == "waiting_for_patr":
        msg = message
        if message.chat.id in user_tokens:
            curr_token = user_tokens[message.chat.id]
        else:
            bot.send_message(message.chat.id, f"Ошибка авторизации.")
            auth(msg.chat.id)
            return

        response = utils.users_profile(curr_token)

        if response.status_code == 200:
            response = utils.users(
                response.json()["firstname"],
                response.json()["lastname"],
                message.text,
                curr_token,
            )

            user_states[message.chat.id] = None
            if response.status_code == 200:
                bot.send_message(message.chat.id, f"Данные успешно изменены.")
                get_req_profile(msg)
            elif (
                response.status_code == 401
                and response.json()["detail"] == "Срок действия токена истек"
            ):
                bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
                refresh(msg)
                get_req_profile(msg)
            else:
                bot.send_message(message.chat.id, f"Произошла ошибка.")
                get_req_profile(msg)
        elif (
            response.status_code == 401
            and response.json()["detail"] == "Срок действия токена истек"
        ):
            bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
            refresh(msg)
            get_req_profile(msg)
        else:
            error_data = response.json()
            print(error_data["detail"])

            bot.send_message(message.chat.id, f"Произошла ошибка.")
            to_go(msg.chat.id)

    elif user_states.get(message.chat.id) == "waiting_for_task":
        msg = message
        if message.chat.id in user_tokens:
            curr_token = user_tokens[message.chat.id]
        else:
            bot.send_message(message.chat.id, f"Ошибка авторизации.")
            auth(msg.chat.id)
            return
        user_states[msg.chat.id] = None
        response = utils.accept_task(msg.text, curr_token)
        if response.status_code == 200:
            bot.send_message(message.chat.id, f"Задача принята.")
            current(msg)
        elif (
            response.status_code == 401
            and response.json()["detail"] == "Срок действия токена истек"
        ):
            bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
            refresh(msg)
            get_req_profile(msg)
        else:
            bot.send_message(message.chat.id, f"Произошла ошибка.")
            print(response.status_code)
            to_go(msg.chat.id)
    elif user_states.get(message.chat.id) == "waiting_for_problem":
        msg = message
        if message.chat.id in user_tokens:
            curr_token = user_tokens[message.chat.id]
        else:
            bot.send_message(message.chat.id, f"Ошибка авторизации.")
            auth(msg.chat.id)
            return
        user_states[msg.chat.id] = None

        response = utils.users_profile(curr_token)

        if response.status_code == 200:
            response = utils.tasks_id(response.json()["id"])

            if response.status_code == 200:
                response_data = response.json()
                counter = 0
                for item in response_data["items"]:
                    if item["status"]["id"] == 4:
                        counter = 1
                        temp = item["id"]
                        break
                if counter == 0:
                    bot.send_message(
                        message.chat.id,
                        "У Вас нет принятых задач.\n\nПримите одну задачу из Вашего списка задач, чтобы сделать её текущей.",
                        parse_mode="Markdown",
                    )
                    btn1 = types.KeyboardButton("Выбрать задачу")
                    btn2 = types.KeyboardButton("Список задач")
                    markup = components.add_btns(3, [btn1, btn2])
                    bot.send_message(message.chat.id, "Далее...", reply_markup=markup)
                else:
                    response = utils.cancelled(msg.text, curr_token, temp)
                    if response.status_code == 200:
                        bot.send_message(
                            message.chat.id,
                            f"Ваш менеджер оповещён о проблеме.\nТекущая задача снята.",
                        )
                        current(msg)
                    elif (
                        response.status_code == 401
                        and response.json()["detail"] == "Срок действия токена истек"
                    ):
                        bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
                        refresh(msg)
                        get_req_profile(msg)
                    else:
                        bot.send_message(message.chat.id, f"Произошла ошибка.")
                        print(response.status_code)
                        to_go(msg.chat.id)

            elif (
                response.status_code == 401
                and response.json()["detail"] == "Срок действия токена истек"
            ):
                bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
                refresh(msg)
                show_emps(msg)
            else:
                error_data = response.json()
                print(error_data["detail"])

                bot.send_message(message.chat.id, f"Произошла ошибка.")
                to_go(msg.chat.id)
        elif (
            response.status_code == 401
            and response.json()["detail"] == "Срок действия токена истек"
        ):
            bot.send_message(message.chat.id, f"Токен истёк, обновляем.")
            refresh(msg)
            get_req_profile(msg)
        else:
            error_data = response.json()
            print(error_data["detail"])

            bot.send_message(message.chat.id, f"Произошла ошибка.")
            to_go(msg.chat.id)
    else:
        bot.send_message(message.chat.id, "Есть команда /start")


if __name__ == "__main__":
    bot.infinity_polling()
