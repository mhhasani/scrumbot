from khayyam import *
from telegram import (KeyboardButton, ReplyKeyboardMarkup,
                      Update, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackContext, CallbackQueryHandler, ConversationHandler,)
import sqlite3
from datetime import *

CHANNEl = "@Scrum_mhhasani_log"
# TEXTS
welcome_text = "به ربات اسکرام خوش اومدی🥳\n\nبرای این که بتونیم بهت خدمات بهتری بدیم لطفا یکم بیشتر از خودت به ما بگو🤓"
get_name_text = "لطفا نام و نام خانوادگیت رو برای ما تایپ کن و بفرست👇🏻"
home_text = "خوش‌ اومدی! گزینه مورد نظرت رو انتخاب کن"
new_user_text = "اطلاعاتت با موفقیت در ربات ثبت شد!"
get_phone_text = "دوست عزیزم ☺️\nما برای اینکه بتونیم بهت خدمات بهتری بدیم ، و بتونیم رضایتتو بیشتر از قبل جلب کنیم ، نیاز داریم که شماره تو داشته باشیم ☎️\nلازم نیست نگران چیزی باشی ، چون ما با چشمامون 👀 از اطلاعاتت محافظت میکنیم 💪🏻\n\nبرای به اشتراک گذاشتن شماره تلفنت ، روی دکمه زیر کلیک کن 🛎"
end_text = "ممنون بابت تکمیل اطلاعاتت!"
first_login_text = "لطفا اول اطلاعاتت رو ثبت کن!"
change_name_text = "اسمت با موفقیت تغییر کرد!"
unknown_text = "ای وای😱\nاین پیام برای ربات ما قابل فهم نیست.😕\n\nاگر اشکالی وجود داره و با فشردن دستور /start حل نشد ، به ما از طریق آیدی @mhhasani خبر بده."
cancel_text = "با موفقیت کنسل شد!"
add_task_text = "🔺برای افزودن فعالیت جدید عنوان فعالیتت رو توی یک خط وارد کن: "
added_activity_text = "✅فعالیت با موفقیت افزوده شد!\nهر موقع فعالیتت تموم شد میتونی روی دکمه ' اتمام فعالیت ' کلیک کنی👇"
backtomain_text = "به صفحه اصلی برگشتی!"
end_task_text = "اتمام این فعالیت ثبت شد!"
task_not_ended_text = "❌ شما فعالیتی دارید که به پایان نرسیده است!\nابتدا آن را به پایان رسانده و دوباره تلاش کنید..."
no_task_text = "فعالیتی وجود ندارد!"
task_already_ended_text = "این فعالیت قبلا به پایان رسیده است!"


def force_end_task_text(report):
    mabhas = report[3]
    dars = report[2]
    text = f"🔺 از شروع فعالیت مبحث {mabhas} از درس {dars} بیشتر از دو ساعت گذشته...\nما اتمام این فعالیت رو برات ثبت کردیم :)"
    return text


# BUTTONS
all_reshte = ['ریاضی', 'تجربی', 'انسانی', 'هنر']
all_paye = ['دهم', 'یازدهم', 'دوازدهم', 'فارغ التحصیل']
MAIN_BUTTON = ['مشاهده اطلاعات فردی', 'مشاهده گزارش ۳ روز اخیر',
               'افزودن فعالیت', 'مشاهده فعالیت جاری']
# KEYBOARDS
main_keyboard = [[KeyboardButton(MAIN_BUTTON[0])],
                 [KeyboardButton(MAIN_BUTTON[1])],
                 [KeyboardButton(MAIN_BUTTON[2])],
                 [KeyboardButton(MAIN_BUTTON[3])]]
start_reply_markup = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True)

phone_keyboard = [
    [KeyboardButton(text="اشتراک گذاری شماره تلفن", request_contact=True)]]
phone_reply_markup = ReplyKeyboardMarkup(
    phone_keyboard, one_time_keyboard=True)
# INLINE KEYBOARDS
keyboard = [
    [InlineKeyboardButton(
        "ویرایش نام و نام خانوادگی", callback_data='change_name')],
]
change_reply_markup = InlineKeyboardMarkup(keyboard)
# INFO STEPS
NOT_FOUND = -1
NAME = 1
RESHTE = 2
PAYE = 3
PHONE = 4
SUCCESSFUL = 5
# TASKS STEPS
ADD_TASK = 0


def do_sql_query(query, values, is_select_query=False):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute(query, values)
        if is_select_query:
            rows = cursor.fetchall()
            return rows
    finally:
        conn.commit()
        cursor.close()


def update_username(chat_id, username):
    query = "UPDATE User SET username = ? WHERE chat_id = ?"
    values = [username, str(chat_id)]
    try:
        do_sql_query(query, values)
    except:
        pass


def get_status(chat_id, username):
    update_username(chat_id, username)

    query = "SELECT * FROM User WHERE chat_id = ?"
    values = [chat_id]
    user = do_sql_query(query, values, True)

    if user:
        user = user[0]
        if not user[2]:
            return NAME
        elif not user[3]:
            return PHONE
        else:
            return SUCCESSFUL
    else:
        return NOT_FOUND


def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.from_user['username']

    status = get_status(chat_id, username)

    if status == NOT_FOUND:
        query = "INSERT INTO User (chat_id,username) VALUES (?,?)"
        values = [chat_id, username]
        do_sql_query(query, values)
        update.message.reply_text(text=welcome_text)
        update.message.reply_text(text=get_name_text)
        return NAME
    elif status == NAME:
        update.message.reply_text(text=get_name_text)
        return NAME
    elif status == PHONE:
        update.message.reply_text(text=get_phone_text)
        return PHONE
    else:
        update.message.reply_text(
            text=home_text, reply_markup=start_reply_markup)

        return ConversationHandler.END


def get_name(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    name = update.message.text

    query = "UPDATE User SET name = ? WHERE chat_id = ?"
    values = [name, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(
        text=get_phone_text, reply_markup=phone_reply_markup)
    return PHONE


def change_name(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    name = update.message.text

    query = "UPDATE User SET name = ? WHERE chat_id = ?"
    values = [name, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(text=change_name_text,
                              reply_markup=start_reply_markup)
    return ConversationHandler.END


def get_phone(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    contact = update.effective_message.contact
    phone = contact.phone_number

    query = "UPDATE User SET phone = ? WHERE chat_id = ?"
    values = [phone, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(text=new_user_text)
    return start(update, context)


def get_info(update: Update):
    chat_id = update.message.chat_id

    query = 'SELECT * FROM User WHERE chat_id = ?'
    values = [chat_id]
    user = do_sql_query(query, values, True)
    if not user:
        update.message.reply_text(text=first_login_text)
    else:
        user = user[0]
        name = user[2]
        phone = user[3]
        text = f"🧾دوست عزیزم اطلاعات کاربری تو به شرح زیره :\n\n🤓 نام و نام خانوادگی : {name}\n📞 شماره تلفن : {phone}"
        update.message.reply_text(text=text, reply_markup=change_reply_markup)


def end_time_keyboard(rep_id):
    keyboard = [[InlineKeyboardButton(
        "اتمام فعالیت", callback_data='end_time '+str(rep_id))]]
    return InlineKeyboardMarkup(keyboard)


def todays_task_text(chat_id, day=0):
    sql = "SELECT * FROM User WHERE chat_id = ?"
    user = do_sql_query(sql, [chat_id], True)[0]

    now = JalaliDate.today() + timedelta(hours=4.5)
    sql = "SELECT R.* FROM User S JOIN Report R ON S.chat_id = R.chat_id WHERE S.chat_id = ?"
    reports = do_sql_query(sql, [chat_id], True)
    now = now - timedelta(days=day)
    text = f"📆 تاریخ : {now.strftime('%d / %m / %Y')}\n"
    name = user[2].replace(' ', "_")
    sum_time = 0
    text += f"👤 #{name}"
    text += "\n\n➖➖➖➖➖\n👓 برنامه فعالیت های امروز :\n\n"
    for report in reports:
        start_time = JalaliDate(datetime.strptime(
            report[3], '%Y-%m-%d %H:%M:%S'))
        if start_time.strftime('%Y-%m-%d') == now.strftime('%Y-%m-%d'):
            text += f"🔸 موضوع فعالیت : {report[2]} \n"
            st = datetime.strptime(report[3], '%Y-%m-%d %H:%M:%S')
            if report[4]:
                et = datetime.strptime(report[4], '%Y-%m-%d %H:%M:%S')
                time = (et-st).seconds // 60
                text += f"🕒 مدت کار: {time} دقیقه"
                sum_time += time
            else:
                text += '🕒 در حال انجام...'
            text += "\n\n"
    hour = sum_time // 60
    minute = sum_time - hour * 60
    if hour != 0:
        if minute != 0:
            sum_time = f"{hour} ساعت و {minute} دقیقه"
        else:
            sum_time = f"{hour} ساعت"
    else:
        sum_time = f"{minute} دقیقه"
    text += f"➖➖➖➖➖\n🕰 مجموع ساعات کاری امروز : {sum_time}"

    return text


def update_channel(chat_id=None, update=None, query=None, context=None):
    new_message = False
    today = JalaliDate.today() + timedelta(hours=4.5)
    today = JalaliDate(today).strftime('%Y-%m-%d')
    sql = "SELECT * FROM User WHERE chat_id = ?"
    user = do_sql_query(sql, [chat_id], True)
    user_date = user[0][5]
    if user_date:
        if today != user_date:
            new_message = True
    else:
        new_message = True

    user_date = today

    if new_message:
        if update:
            message_id = update.message.bot.send_message(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
            ).message_id
        elif query:
            message_id = query.message.bot.send_message(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
            ).message_id
        elif context:
            message_id = context.bot.send_message(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
            ).message_id
        sql = "UPDATE User SET (day,message_id) = (?,?) WHERE chat_id = ?"
        do_sql_query(sql, [user_date, message_id, chat_id])
    else:
        message_id = user[0][4]
        if update:
            update.message.bot.edit_message_text(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
                message_id=message_id)
        elif query:
            query.message.bot.edit_message_text(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
                message_id=message_id
            )
        elif context:
            context.bot.edit_message_text(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
                message_id=message_id
            )


def add_task(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    topic = update.message.text.split("\n")

    if len(topic) != 1:
        update.message.reply_text(text=add_task_text)
        return ADD_TASK

    topic = topic[0]
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = "INSERT INTO Report (chat_id,topic,start_time) VALUES (?,?,?)"
    values = [chat_id, topic, start_time]
    do_sql_query(query, values)

    query = "SELECT seq FROM sqlite_sequence WHERE name = ?"
    rep_id = do_sql_query(query, ['Report'], True)[0][0]
    end_time_reply_markup = end_time_keyboard(rep_id)

    update.message.reply_text(text=added_activity_text,
                              reply_markup=end_time_reply_markup)
    update_channel(chat_id, update=update)
    return ConversationHandler.END


def view_current_task(update: Update):
    chat_id = update.message.chat_id

    now_time = datetime.now()

    query = "SELECT * FROM Report WHERE chat_id = ? AND end_time IS NULL"
    Reports = do_sql_query(query, [chat_id], True)

    if Reports:
        for report in Reports:
            start_time = datetime.strptime(
                report[3], '%Y-%m-%d %H:%M:%S')
            time = now_time - start_time
            minute = time.seconds // 60
            hour = (JalaliDatetime(start_time) +
                    timedelta(hours=4.5)).strftime('%H:%M')
            text = f"⭕️ شما فعالیت {report[2]} را در ساعت {hour} آغاز کرده اید و {minute} دقیقه از شروع آن گذشته است.\nهر موقع فعالیتت تموم شد میتونی روی دکمه ' اتمام فعالیت ' کلیک کنی👇"
            update.message.reply_text(
                text=text, reply_markup=end_time_keyboard(report[0]))
    else:
        update.message.reply_text(text=no_task_text)


def check_end_task(context: CallbackContext):
    now_time = datetime.now()

    query = "SELECT * FROM Report WHERE end_time IS NULL"
    Reports = do_sql_query(query, [], True)

    if Reports:
        for report in Reports:
            rep_id = report[0]
            chat_id = report[1]
            start_time = datetime.strptime(
                report[3], '%Y-%m-%d %H:%M:%S')
            time = now_time - start_time
            minute = time.seconds // 60
            if minute >= 120:
                end_time = start_time + timedelta(hours=2)
                end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
                query = "UPDATE Report SET end_time = ? WHERE id = ?"
                do_sql_query(query, [end_time, rep_id])
                context.bot.send_message(
                    text=force_end_task_text(report), chat_id=chat_id)
                update_channel(chat_id, context=context)


def message_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    if text not in MAIN_BUTTON:
        update.message.reply_text(text=unknown_text)

    elif text == MAIN_BUTTON[0]:
        get_info(update)

    elif text == MAIN_BUTTON[2]:
        query = "SELECT * FROM Report WHERE chat_id = ? AND end_time IS NULL"
        Reports = do_sql_query(query, [chat_id], True)

        if Reports:
            update.message.reply_text(text=task_not_ended_text)
            return ConversationHandler.END

        update.message.reply_text(text=add_task_text)
        return ADD_TASK

    elif text == MAIN_BUTTON[3]:
        view_current_task(update)

    elif text == MAIN_BUTTON[1]:
        update.message.reply_text(text=todays_task_text(chat_id, day=2))
        update.message.reply_text(text=todays_task_text(chat_id, day=1))
        update.message.reply_text(text=todays_task_text(chat_id, day=0))
    return ConversationHandler.END


def Inline_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    username = update.callback_query.from_user['username']

    if query.data == 'change_name':
        sql = "UPDATE User SET name = ? WHERE chat_id = ?"
        values = [None, str(chat_id)]
        do_sql_query(sql, values)

        query.message.reply_text(text=get_name_text)
        query.answer(text="تغییر نام و نام خانوادگی")

        return NAME


    elif query.data.split()[0] == 'end_time':
        id = query.data.split()[1]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = "SELECT end_time FROM Report WHERE id = ?"
        values = [id]
        end_time = do_sql_query(sql, values, True)
        if not end_time[0][0]:
            sql = "UPDATE Report SET end_time = ? WHERE id = ?"
            values = [now, id]
            do_sql_query(sql, values)

            query.message.bot.edit_message_text(
                text=end_task_text, message_id=message_id, chat_id=chat_id)
            update_channel(chat_id, query=query)
        else:
            query.message.bot.edit_message_text(
                text=task_already_ended_text, message_id=message_id, chat_id=chat_id)

        query.answer(text="اتمام فعالیت")


def cancel(update: Update, context: CallbackContext):
    """Cancels and ends the conversation."""
    update.message.reply_text(text=cancel_text)
    return ConversationHandler.END


def main():
    updater = Updater(
        "5554362279:AAH7WAdIbEKdbiu0a9ONuYM6ilOKRaYP6LE", use_context=True)

    dispatcher = updater.dispatcher
    j = updater.job_queue
    j.run_repeating(check_end_task, interval=300, first=1)

    get_name_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            PHONE: [MessageHandler(Filters.contact, get_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(get_name_handler)

    Inline_buttons_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(Inline_buttons)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, change_name)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(Inline_buttons_handler)

    Message_handler = ConversationHandler(
        entry_points=[MessageHandler(
            Filters.text & ~Filters.command, message_handler)],
        states={
            ADD_TASK: [MessageHandler(Filters.text & ~Filters.command, add_task)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(Message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
