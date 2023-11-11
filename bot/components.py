from telebot import types


def add_btns(num, btns):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton('На главную')
    if num == 2:
        markup.add(btns[0])
        markup.add(back)
    elif num == 3:
        markup.row(btns[0], btns[1])
        markup.row(back)
    elif num == 4:
        markup.row(btns[0], btns[1], btns[2])
        markup.row(back)
    return markup