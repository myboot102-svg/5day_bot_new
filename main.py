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
STATE_ADMIN_AGENTS = "admin_agents"

STATE_AGENT_DEPOSITS = "agent_deposits"
STATE_AGENT_WITHDRAWALS = "agent_withdrawals"


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

def user_keyboard(is_admin=False, is_agent=False):

    keyboard = [
        ["الباقات", "الإيداع"],
        ["السحب", "حالة الباقة"],
        ["حسابي", "الإحالة"],
        ["الدعم"],
    ]

    if is_admin:
        keyboard.append(["لوحة الإدارة"])

    elif is_agent:
        keyboard.append(["لوحة الوكيل"])

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
        ["إدارة الوكلاء"],
        ["رجوع"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# ==================================================
# كيبورد الوكيل
# ==================================================

def agent_keyboard():

    keyboard = [
        ["إيداعاتي", "سحوباتي"],
        ["إجمالي الإيداعات", "إجمالي السحوبات"],
        ["المستخدمين المرتبطين"],
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

    # الوكيل
    if user.get("role") == "agent":

        await update.message.reply_text(
            "مرحباً بك في 5DAY.",
            reply_markup=user_keyboard(
                is_agent=True
            )
        )

        return

    # المستخدم العادي
    await update.message.reply_text(
        "أهلاً بك في 5DAY.\n\n"
        "اختر من القائمة:",
        reply_markup=user_keyboard()
    )


# ==================================================
# القسم الرئيسي للمستخدم
# ==================================================

async def user_section(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
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

async def admin_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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
# لوحة الوكيل
# ==================================================

async def agent_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = get_user(
        update.effective_user.id,
        update
    )

    if user.get("role") != "agent":
        return

    user["state"] = STATE_NONE

    await update.message.reply_text(
        "لوحة الوكيل:",
        reply_markup=agent_keyboard()
    )


# ==================================================
# الأدمن - الأقسام
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
# الوكيل - الأقسام
# ==================================================

async def agent_section(
    update: Update,
    title: str,
    state: str
):

    user = get_user(
        update.effective_user.id,
        update
    )

    if user.get("role") != "agent":
        return

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

    role = user.get(
        "role",
        "user"
    )


    # ==================================================
    # الرجوع
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

        elif role == "agent":

            await update.message.reply_text(
                "القائمة الرئيسية:",
                reply_markup=user_keyboard(
                    is_agent=True
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
                update,
                context
            )

        return


    # ==================================================
    # لوحة الوكيل
    # ==================================================

    if text == "لوحة الوكيل":

        if role == "agent":
            await agent_panel(
                update,
                context
            )

        return


    # ==================================================
    # المستخدم
    # ==================================================

    if text == "الباقات":

        await user_section(
            update,
            context,
            "قسم الباقات.",
            STATE_PACKAGE
        )

        return


    if text == "الإيداع":

        await user_section(
            update,
            context,
            "قسم الإيداع.",
            STATE_DEPOSIT
        )

        return


    if text == "السحب":

        await user_section(
            update,
            context,
            "قسم السحب.",
            STATE_WITHDRAW
        )

        return


    if text == "حالة الباقة":

        await user_section(
            update,
            context,
            "قسم حالة الباقة.",
            STATE_PACKAGE
        )

        return


    if text == "حسابي":

        await user_section(
            update,
            context,
            "قسم حسابي.",
            STATE_NONE
        )

        return


    if text == "الإحالة":

        await user_section(
            update,
            context,
            "قسم الإحالة.",
            STATE_NONE
        )

        return


    if text == "الدعم":

        await user_section(
            update,
            context,
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

        elif text == "إدارة الوكلاء":

            await admin_section(
                update,
                "قسم إدارة الوكلاء.",
                STATE_ADMIN_AGENTS
            )

        return


    # ==================================================
    # الوكيل
    # ==================================================

    if role == "agent":

        if text == "إيداعاتي":

            await agent_section(
                update,
                "قسم إيداعاتي.",
                STATE_AGENT_DEPOSITS
            )

        elif text == "سحوباتي":

            await agent_section(
                update,
                "قسم سحوباتي.",
                STATE_AGENT_WITHDRAWALS
            )

        elif text == "إجمالي الإيداعات":

            await agent_section(
                update,
                "قسم إجمالي الإيداعات.",
                STATE_AGENT_DEPOSITS
            )

        elif text == "إجمالي السحوبات":

            await agent_section(
                update,
                "قسم إجمالي السحوبات.",
                STATE_AGENT_WITHDRAWALS
            )

        elif text == "المستخدمين المرتبطين":

            await agent_section(
                update,
                "قسم المستخدمين المرتبطين.",
                STATE_NONE
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
