import telebot
import sqlite3
import argparse

parser = argparse.ArgumentParser()
token = '5126330996:AAHQYMz3s0-QNPkmzvlNm4P_sg2EowU-CAs'
bot = telebot.TeleBot(token=token)


def db_connect(arg):
    con = sqlite3.connect('flats.db', check_same_thread=False)
    cur = con.cursor()
    if arg == True:
        cur.execute('''CREATE TABLE users
                           (user_id text, username text, PRIMARY KEY (user_id))''')
        con.commit()

    return con, cur


def main():
    @bot.message_handler(commands=['start'])
    def handle_start_help(message):
        # print(message.chat.username)
        bot.send_message(message.chat.id, "Начал отслеживать новые варианты")
        cur.execute('''insert or ignore into users values (?,?);''', (message.chat.id, message.chat.username))
        con.commit()

    bot.polling(non_stop=True)


if __name__ == '__main__':
    parser.add_argument("-v", "--verbose", help="if you are running for the first time",
                        action="store_true")
    args = parser.parse_args()
    con, cur = db_connect(arg=args.verbose)
    main()
