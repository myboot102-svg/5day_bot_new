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


