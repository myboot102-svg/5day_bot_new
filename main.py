import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8460661282


def user_menu():
    keyboard = [
        [
            InlineKeyboardButton("💰 الباقات", callback_data="packages"),
            InlineKeyboardButton("💳 الإيداع", callback_data="deposit"),
        ],
        [
            InlineKeyboardButton("💸 السحب", callback_data="withdraw"),
            InlineKeyboardButton("📦 حالة الباقة", callback_data="package_status"),
        ],
        [
            InlineKeyboardButton("👤 حسابي", callback_data="account"),
            InlineKeyboardButton("🔗 الإحالة", callback_data="referral"),
        ],
        [
            InlineKeyboardButton("🎧 الدعم", callback_data="support"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def admin_menu():
    keyboard = [
        [
            InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users"),
            InlineKeyboardButton("💳 الإيداعات", callback_data="admin_deposits"),
        ],
        [
            InlineKeyboardButton("💸 السحوبات", callback_data="admin_withdrawals"),
            InlineKeyboardButton("🏦 طرق الإيداع", callback_data="admin_deposit_methods"),
        ],
        [
            InlineKeyboardButton("💰 طرق السحب", callback_data="admin_withdraw_methods"),
            InlineKeyboardButton("📢 رسالة جماعية", callback_data="admin_broadcast"),
        ],
        [
            InlineKeyboardButton("🎧 رسائل الدعم", callback_data="admin_support"),
            InlineKeyboardButton("📦 إدارة الباقات", callback_data="admin_packages"),
        ],
        [
            InlineKeyboardButton("🤝 إدارة الوكلاء", callback_data="admin_agents"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def back_user():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_user")]
    ])


def back_admin():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_admin")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id == ADMIN_ID:
        await update.message.reply_text(
            "مرحباً بك في لوحة إدارة 5DAY.",
            reply_markup=admin_menu()
        )
    else:
        await update.message.reply_text(
            "هلا بيج بـ 5DAY.\n\nاختاري من القائمة:",
            reply_markup=user_menu()
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id

    if data == "packages":
        await query.edit_message_text(
            "💰 الباقات الاستثمارية\n\n"
            "قريباً راح تظهر الباقات هنا.",
            reply_markup=back_user()
        )

    elif data == "deposit":
        await query.edit_message_text(
            "💳 الإيداع\n\n"
            "اختاري طريقة الإيداع من هنا.",
            reply_markup=back_user()
        )

    elif data == "withdraw":
        await query.edit_message_text(
            "💸 السحب\n\n"
            "اختاري طريقة السحب من هنا.",
            reply_markup=back_user()
        )

    elif data == "package_status":
        await query.edit_message_text(
            "📦 حالة الباقة\n\n"
            "ما عندج باقة فعالة حالياً.",
            reply_markup=back_user()
        )

    elif data == "account":
        await query.edit_message_text(
            f"👤 حسابي\n\n"
            f"🆔 الآيدي: {user_id}\n"
            f"💰 الرصيد: 0\n"
            f"📦 الباقات: 0",
            reply_markup=back_user()
        )

    elif data == "referral":
        await query.edit_message_text(
            "🔗 رابط الإحالة\n\n"
            "راح يظهر رابط الإحالة هنا.",
            reply_markup=back_user()
        )

    elif data == "support":
        await query.edit_message_text(
            "🎧 الدعم\n\n"
            "اكتبي رسالتج حتى يتم إرسالها للدعم.",
            reply_markup=back_user()
        )

    elif data.startswith("admin_"):

        if user_id != ADMIN_ID:
            return

        admin_pages = {
            "admin_users": "👥 المستخدمين\n\nهنا راح تظهر قائمة المستخدمين.",
            "admin_deposits": "💳 الإيداعات\n\nهنا راح تظهر طلبات الإيداع.",
            "admin_withdrawals": "💸 السحوبات\n\nهنا راح تظهر طلبات السحب.",
            "admin_deposit_methods": "🏦 طرق الإيداع\n\nهنا راح تدير طرق الإيداع.",
            "admin_withdraw_methods": "💰 طرق السحب\n\nهنا راح تدير طرق السحب.",
            "admin_broadcast": "📢 رسالة جماعية\n\nهنا راح ترسل رسالة لجميع المستخدمين.",
            "admin_support": "🎧 رسائل الدعم\n\nهنا راح تظهر رسائل المستخدمين.",
            "admin_packages": "📦 إدارة الباقات\n\nهنا راح تدير الباقات.",
            "admin_agents": "🤝 إدارة الوكلاء\n\nهنا راح تدير الوكلاء.",
        }

        await query.edit_message_text(
            admin_pages.get(data, "القسم غير موجود."),
            reply_markup=back_admin()
        )

    elif data == "back_user":
        await query.edit_message_text(
            "اختاري من القائمة:",
            reply_markup=user_menu()
        )

    elif data == "back_admin":
        await query.edit_message_text(
            "لوحة الإدارة:",
            reply_markup=admin_menu()
        )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN غير موجود في Variables")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("5DAY Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
