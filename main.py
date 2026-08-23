import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


# ==================================================
# الإعدادات
# ==================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8460661282


# ==================================================
# STATES
# ==================================================

STATE_NONE = "none"

STATE_DEPOSIT = "deposit"
STATE_WITHDRAW = "withdraw"
STATE_PACKAGE = "package"
STATE_SUPPORT = "support"

STATE_ADMIN_USERS = "admin_users"
STATE_ADMIN_DEPOSITS = "admin_deposits"
STATE_ADMIN_WITHDRAWALS = "admin_withdrawals"
STATE_ADMIN_DEPOSIT_METHODS = "admin_deposit_methods"
STATE_ADMIN_WITHDRAW_METHODS = "admin_withdraw_methods"
STATE_ADMIN_BROADCAST = "admin_broadcast"
STATE_ADMIN_SUPPORT = "admin_support"
STATE_ADMIN_PACKAGES = "admin_packages"


# ==================================================
# مستخدمين مؤقتين
# ==================================================

users = {}


# ==================================================
# إنشاء مستخدم
# ==================================================

def get_user(user_id, update=None):

    if user_id not in users:

        name = ""
        username = ""

        if update and update.effective_user:
            name = update.effective_user.first_name or ""
            username = update.effective_user.username or ""

        users[user_id] = {
            "user_id": user_id,
            "name": name,
            "username": username,
            "role": "user",
            "state": STATE_NONE,
        }

    return users[user_id]


# ==================================================
# كيبورد المستخدم
# ==================================================

def user_keyboard(is_admin=False):

    keyboard = [
        ["الباقات", "حالة الباقة"],
        ["الإيداع", "السحب"],
        ["حسابي", "الإحالة"],
        ["الدعم"],
    ]

    if is_admin:
        keyboard.append(["لوحة الإدارة"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# ==================================================
# كيبورد الأدمن
# ==================================================

def admin_keyboard():

    keyboard = [
        ["المستخدمين", "الإيداعات"],
        ["السحوبات", "طرق الإيداع"],
        ["طرق السحب", "رسالة جماعية"],
        ["رسائل الدعم", "إدارة الباقات"],
        ["رجوع"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# ==================================================
# كيبورد الرجوع
# ==================================================

def back_keyboard():

    return ReplyKeyboardMarkup(
        [["رجوع"]],
        resize_keyboard=True
    )


# ==================================================
# START
# ==================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    user = get_user(
        user_id,
        update
    )

    # الأدمن
    if user_id == ADMIN_ID:

        user["role"] = "admin"

        await update.message.reply_text(
            "مرحباً بك في 5DAY.",
            reply_markup=user_keyboard(
                is_admin=True
            )
        )

        return

    # المستخدم
    await update.message.reply_text(
        "أهلاً بك في 5DAY.\n\n"
        "اختر من القائمة:",
        reply_markup=user_keyboard()
    )


# ==================================================
# قسم المستخدم
# ==================================================

async def user_section(
    update: Update,
    title: str,
    state: str
):

    user_id = update.effective_user.id

    user = get_user(
        user_id,
        update
    )

    user["state"] = state

    await update.message.reply_text(
        title,
        reply_markup=back_keyboard()
    )


# ==================================================
# لوحة الأدمن
# ==================================================

async def admin_panel(update: Update):

    if update.effective_user.id != ADMIN_ID:
        return

    user = get_user(
        update.effective_user.id,
        update
    )

    user["state"] = STATE_NONE

    await update.message.reply_text(
        "لوحة الإدارة:",
        reply_markup=admin_keyboard()
    )


# ==================================================
# قسم الأدمن
# ==================================================

async def admin_section(
    update: Update,
    title: str,
    state: str
):

    if update.effective_user.id != ADMIN_ID:
        return

    user = get_user(
        update.effective_user.id,
        update
    )

    user["state"] = state

    await update.message.reply_text(
        title,
        reply_markup=back_keyboard()
    )


# ==================================================
# Message Router
# ==================================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    text = update.message.text

    user_id = update.effective_user.id

    user = get_user(
        user_id,
        update
    )

    # ==================================================
    # رجوع
    # ==================================================

    if text == "رجوع":

        user["state"] = STATE_NONE

        if user_id == ADMIN_ID:

            await update.message.reply_text(
                "القائمة الرئيسية:",
                reply_markup=user_keyboard(
                    is_admin=True
                )
            )

        else:

            await update.message.reply_text(
                "القائمة الرئيسية:",
                reply_markup=user_keyboard()
            )

        return


    # ==================================================
    # لوحة الإدارة
    # ==================================================

    if text == "لوحة الإدارة":

        if user_id == ADMIN_ID:

            await admin_panel(
                update
            )

        return


    # ==================================================
    # المستخدم
    # ==================================================

    if text == "الباقات":

        await user_section(
            update,
            "قسم الباقات.",
            STATE_PACKAGE
        )

        return


    if text == "الإيداع":

        await user_section(
            update,
            "قسم الإيداع.",
            STATE_DEPOSIT
        )

        return


    if text == "السحب":

        await user_section(
            update,
            "قسم السحب.",
            STATE_WITHDRAW
        )

        return


    if text == "حالة الباقة":

        await user_section(
            update,
            "قسم حالة الباقة.",
            STATE_PACKAGE
        )

        return


    if text == "حسابي":

        await user_section(
            update,
            "قسم حسابي.",
            STATE_NONE
        )

        return


    if text == "الإحالة":

        await user_section(
            update,
            "قسم الإحالة.",
            STATE_NONE
        )

        return


    if text == "الدعم":

        await user_section(
            update,
            "قسم الدعم.",
            STATE_SUPPORT
        )

        return


    # ==================================================
    # الأدمن
    # ==================================================

    if user_id == ADMIN_ID:

        if text == "المستخدمين":

            await admin_section(
                update,
                "قسم المستخدمين.",
                STATE_ADMIN_USERS
            )

        elif text == "الإيداعات":

            await admin_section(
                update,
                "قسم الإيداعات.",
                STATE_ADMIN_DEPOSITS
            )

        elif text == "السحوبات":

            await admin_section(
                update,
                "قسم السحوبات.",
                STATE_ADMIN_WITHDRAWALS
            )

        elif text == "طرق الإيداع":

            await admin_section(
                update,
                "قسم طرق الإيداع.",
                STATE_ADMIN_DEPOSIT_METHODS
            )

        elif text == "طرق السحب":

            await admin_section(
                update,
                "قسم طرق السحب.",
                STATE_ADMIN_WITHDRAW_METHODS
            )

        elif text == "رسالة جماعية":

            await admin_section(
                update,
                "قسم الرسالة الجماعية.",
                STATE_ADMIN_BROADCAST
            )

        elif text == "رسائل الدعم":

            await admin_section(
                update,
                "قسم رسائل الدعم.",
                STATE_ADMIN_SUPPORT
            )

        elif text == "إدارة الباقات":

            await admin_section(
                update,
                "قسم إدارة الباقات.",
                STATE_ADMIN_PACKAGES
            )

        return


# ==================================================
# MAIN
# ==================================================

def main():

    if not BOT_TOKEN:

        raise ValueError(
            "BOT_TOKEN غير موجود في Railway Variables"
        )

    app = Application.builder().token(
        BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print(
        "5DAY Bot is running..."
    )

    app.run_polling()


# ==================================================
# تشغيل البوت
# ==================================================

if __name__ == "__main__":
    main()
