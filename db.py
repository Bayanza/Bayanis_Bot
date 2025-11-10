import sqlite3
import telebot
from telebot import types
import datetime

bot = telebot.TeleBot("")
conn = sqlite3.connect("bot_db.db", check_same_thread=False)
cursor = conn.cursor()
date = datetime.datetime.now().strftime('%Y-%m-%d')
time = datetime.datetime.now().strftime('%H:%M:%S')


def add_row(message, category):
    if message.chat.type == 'private':
        if message.text.isdigit():
            cursor.execute("INSERT INTO 'expences' (category, sum, added_date, added_time, id_added) VALUES(?,?,?,?,?)", (category, str(message.text), date, time, str(message.from_user.id)))
            conn.commit()
            bot.send_message(message.chat.id, "Записал:" + ' ' + category + ' ' + str(message.text))
        else:
            bot.send_message(message.chat.id, "Цифры давай")


def draw_report(uid):
    report = cursor.execute("SELECT category, sum(sum) FROM expences WHERE id_added = ? GROUP BY category", (uid,))
    conn.commit()
    return report


def get_menu(level):
    items = cursor.execute("SELECT name FROM menu WHERE level = ?", (level,)).fetchall()
    return items


"""
CREATE TABLE "expences" (
	"category" CHAR(50) NULL,
	"sum" INTEGER NULL,
	"added_date" DATE NULL,
	"added_time" TIME NULL,
	"id_added" INTEGER NULL
)
;

"""
