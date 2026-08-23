import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


# ==========================================
# الإعدادات
# ==========================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8460661282


# ==========================================
# STATES
# ==========================================

STATE_NONE = "none"

STATE_DEPOSIT = "deposit"
STATE_WITHDRAW = "withdraw"
STATE_PACKAGES = "packages"
STATE_PACKAGE_STATUS = "package_status"
STATE_ACCOUNT = "account"
STATE_REFERRAL = "referral"
STATE_SUPPORT = "support"

STATE_ADMIN_USERS = "admin_users"
STATE_ADMIN_DEPOSITS = "admin_deposits"
STATE_ADMIN_WITHDRAWALS = "admin_withdrawals"
STATE_ADMIN_DEPOSIT_METHODS = "admin_deposit_methods"
STATE_ADMIN_WITHDRAW_METHODS = "admin_withdraw_methods"
STATE_ADMIN_BROADCAST = "admin_broadcast"
STATE_ADMIN_SUPPORT = "admin_support"
STATE_ADMIN_PACKAGES = "admin_packages"


# ==========================================
# كيبورد المستخدم
# ==========================================

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


# ==========================================
# كيبورد لوحة الإدارة
# ==========================================

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


# ==========================================
# رسالة الترحيب
# ==========================================

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


# ==========================================
# START
# ==========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    is_admin = user_id == ADMIN_ID

    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=user_keyboard(
            is_admin=is_admin
        )
    )


# ==========================================
# تشغيل البوت
# ==========================================

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

    app.run_polling()


# ==========================================
# تشغيل
# ==========================================

if __name__ == "__main__":
    main()
