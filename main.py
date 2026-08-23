import os

from datetime import datetime, timedelta

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)


# ==============================
# الإعدادات
# ==============================

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8460661282



# ==============================
# حالات البوت
# ==============================

STATE_NONE = "none"

STATE_DEPOSIT = "deposit"
STATE_WITHDRAW = "withdraw"
STATE_PACKAGE = "package"
STATE_PACKAGE_CONFIRM = "package_confirm"
STATE_SUPPORT = "support"

# حالات الأدمن
STATE_ADMIN_USERS = "admin_users"
STATE_ADMIN_SEARCH = "admin_search"
STATE_ADMIN_USER_ACTION = "admin_user_action"

STATE_ADMIN_DEPOSITS = "admin_deposits"
STATE_ADMIN_WITHDRAWALS = "admin_withdrawals"

STATE_ADMIN_DEPOSIT_METHODS = "admin_deposit_methods"
STATE_ADMIN_WITHDRAW_METHODS = "admin_withdraw_methods"

STATE_ADMIN_BROADCAST = "admin_broadcast"
STATE_ADMIN_SUPPORT = "admin_support"

STATE_ADMIN_PACKAGES = "admin_packages"



# ==============================
# البيانات الأساسية
# ==============================

users = {}

deposit_requests = []

withdraw_requests = []

support_requests = {}

packages = {}

deposit_methods = {}

withdraw_methods = {}


# ==============================
# الإعدادات المالية
# ==============================

MIN_DEPOSIT = 10000

MIN_WITHDRAW = 8000

WITHDRAW_FEE = 1000

PROFIT_PER_10000 = 500

INVESTMENT_DAYS = 5


# ==============================
# إعدادات الباقات
# ==============================

MIN_PACKAGE = 10000

MAX_PACKAGE = 15000000

PACKAGE_DURATION = 5

PROFIT_PER_10000 = 500


# ==============================
# المحافظ
# ==============================

deposit_methods = {}

withdraw_methods = {}



# ==============================
# بيانات المستخدم
# ==============================

def create_user():
    return {
        "balance": 0,

        "package": None,

        "joined_at": datetime.now(),

        "total_packages": 0,

        "total_days": 0,

        "total_deposits": 0,

        "capital": 0,

        "total_withdrawals": 0,

        "total_profit": 0,

        "referrals": 0,

        "referral_earnings": 0,

        "referrer": None,

        "blocked": False,
    }



# ==============================
# دوال المستخدم
# ==============================

def get_user(user_id):

    if user_id not in users:
        users[user_id] = create_user()

    return users[user_id]


# ==============================
# دوال الـ State
# ==============================

def set_state(context, state):

    context.user_data["state"] = state


def get_state(context):

    return context.user_data.get(
        "state",
        STATE_NONE
    )


def clear_state(context):

    context.user_data.pop(
        "state",
        None
    )


# ==============================
# كيبورد المستخدم
# ==============================

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


# ==============================
# كيبورد الأدمن
# ==============================

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


# ==============================
# رسالة الترحيب
# ==============================

WELCOME_MESSAGE = """
أهلاً بك في بوت 5day للاستثمار الذكي.

يسعدنا انضمامك إلينا، نحن نوفر لك منصة آمنة وموثوقة لنمو رأس مالك من خلال خطط استثمارية قصيرة الأمد.

تعريف برنامج الاستثمار:

مدة الاستثمار: 5 أيام فقط لكل دورة استثمارية.

نظام الأرباح: تحصل على ربح 500 دينار لكل 10,000 دينار.

الشروط والأحكام:

- يحق لكل مستخدم باقة واحدة فقط.
- يتم تجميد رأس المال لمدة 5 أيام.
- يمكن سحب الأرباح يومياً.
- يمكن التجديد بعد انتهاء الباقة.
- تتحرر الأرباح مع رأس المال بعد انتهاء المدة.
"""

# ==============================
# أمر /start
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user_id = update.effective_user.id

    # إنشاء المستخدم إذا أول مرة يدخل
    user = get_user(user_id)

    # التحقق إذا المستخدم محظور
    if user.get("blocked"):
        await update.message.reply_text(
            "هذا الحساب محظور."
        )
        return

    # إذا أدمن
    if user_id == ADMIN_ID:

        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=user_keyboard(
                is_admin=True
            )
        )

    # إذا مستخدم عادي
    else:

        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=user_keyboard()
        )


# ==============================
# Handler الأزرار الأساسية
# ==============================

async def handle_user_buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    text = update.message.text
    user_id = update.effective_user.id

    user = get_user(user_id)

    if user.get("blocked"):
        await update.message.reply_text(
            "هذا الحساب محظور."
        )
        return

    # ------------------------------
    # لوحة الإدارة
    # ------------------------------

    if text == "لوحة الإدارة":

        if user_id != ADMIN_ID:
            return

        await update.message.reply_text(
            "لوحة الإدارة:",
            reply_markup=admin_keyboard()
        )

        return

    # ------------------------------
    # أزرار المستخدم
    # ------------------------------

    sections = {
        "الباقات": "قسم الباقات.",
        "حالة الباقة": "قسم حالة الباقة.",
        "الإيداع": "قسم الإيداع.",
        "السحب": "قسم السحب.",
        "حسابي": "قسم حسابي.",
        "الإحالة": "قسم الإحالة.",
        "الدعم": "قسم الدعم.",
    }

    if text in sections:

        await update.message.reply_text(
            sections[text]
        )

        return

    # ------------------------------
    # رجوع
    # ------------------------------

    if text == "رجوع":

        await update.message.reply_text(
            "القائمة الرئيسية.",
            reply_markup=user_keyboard(
                is_admin=(user_id == ADMIN_ID)
            )
        )

        return


# ==============================
# تشغيل البوت
# ==============================

def main():

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN غير موجود في Railway Variables"
        )

    app = ApplicationBuilder().token(
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
            handle_user_buttons
        )
    )

    print("5DAY Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
