import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN", "")

STUDENTS = {
    "9-sinf": ["Javohir Alijonov","Abdumannonov Muhammadshukur","Abdusalimov Xumoyunbek","Abdusattorov Murodulla","Abduxoliqova Shukronaxon","Bahromjonova Parizoda","Husanboyeva Nazokatxon","Isaxonov Fozilbek","Mashrabjonov Suhrobbek","Muroddjonov Muhammaddiyor","Nosirov Muhammabilol","Olimova Feruzaxon","Rustamova Oishabegim","To'lqinjonov Azizbek","To'lqinjonov Suhrobbek"],
    "10-sinf": ["Tojimamatova Ruxshonaxon","Turdiyeva Muslimaxon","Xudoberganova Charosxon","Abdupattoyeva Muborakxon","Alimirzayeva Yoqutxon","Bahriddinov Fazliddin","Egamnazarova Behro'zabegim","Ergashyeva Mohigul","Ikromjonov Muhammadayyub","In'omjonova Muniraxon","Inomjonova Zarnigorxon","Muhamadaliyev Abrorjon","Muhiddinova Maftunaxon","Oripova Gulsanam","Rahimova Charosxon"],
    "11-sinf": ["Rustamov Muhammadali","Tolibjonov Begali","Turg'unboyeva Sevara","Tursunboyeva Muslima","Hoshmjonova Hilola","Abdug'aforov Iskandar","Hoshmjonov Omadbek","Alijonova Dilnoza","Abobakirov Ibodulloh","Abdug'aniyeva Niluzar","Abdullayeva Ruxshona","Rasulova Jamilaxon","To'lqinova Durdonabonu","To'xtasinova Gulhayo","Xonkeldiyeva Marjona"],
}

ALL = {}
n = 1
for g, names in STUDENTS.items():
    for name in names:
        ALL[str(n)] = {"name": name, "grade": g}
        n += 1

DB = "db.json"
def load():
    try:
        with open(DB, "r", encoding="utf-8") as f: return json.load(f)
    except: return {}
def save(db):
    with open(DB, "w", encoding="utf-8") as f: json.dump(db, f, ensure_ascii=False, indent=2)

S_NAME, S_SUBJ, S_GRADE, S_STU, S_FB, S_AFTER = range(6)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    args = ctx.args or []
    if args and args[0].startswith("student_"):
        return await show_parent(update, ctx, args[0].replace("student_", ""))
    await update.message.reply_text(
        "Yangi Davr Maktabi - Ustoz Fikri Tizimi\n\nIsmingizni yozing:",
        reply_markup=ReplyKeyboardRemove()
    )
    return S_NAME

async def get_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["name"] = update.message.text.strip()
    await update.message.reply_text(f"Rahmat {ctx.user_data['name']}!\n\nQaysi fanni o'qitasiz?")
    return S_SUBJ

async def get_subj(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["subj"] = update.message.text.strip()
    kb = [[InlineKeyboardButton("9-sinf", callback_data="g_9-sinf"),
           InlineKeyboardButton("10-sinf", callback_data="g_10-sinf"),
           InlineKeyboardButton("11-sinf", callback_data="g_11-sinf")]]
    await update.message.reply_text("Qaysi sinf?", reply_markup=InlineKeyboardMarkup(kb))
    return S_GRADE

async def pick_grade(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    grade = q.data.replace("g_", "")
    ctx.user_data["grade"] = grade
    names = STUDENTS[grade]
    rows, row = [], []
    for name in names:
        sid = next(k for k,v in ALL.items() if v["name"]==name and v["grade"]==grade)
        row.append(InlineKeyboardButton(name.split()[0], callback_data=f"s_{sid}"))
        if len(row) == 3: rows.append(row); row = []
    if row: rows.append(row)
    await q.edit_message_text(f"{grade} - o'quvchini tanlang:", reply_markup=InlineKeyboardMarkup(rows))
    return S_STU

async def pick_stu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    sid = q.data.replace("s_", "")
    s = ALL[sid]
    ctx.user_data["sid"] = sid
    ctx.user_data["sname"] = s["name"]
    await q.edit_message_text(f"{s['name']} ({s['grade']})\n\nOvozli xabar yuboring yoki matn yozing:")
    return S_FB

async def recv_fb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sid = ctx.user_data["sid"]
    db = load()
    if sid not in db: db[sid] = []
    entry = {"teacher": ctx.user_data["name"], "subj": ctx.user_data["subj"]}
    if update.message.voice:
        entry["type"] = "voice"
        entry["file_id"] = update.message.voice.file_id
    elif update.message.text:
        entry["type"] = "text"
        entry["text"] = update.message.text
    else:
        await update.message.reply_text("Ovozli xabar yoki matn yuboring.")
        return S_FB
    db[sid].append(entry)
    save(db)
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Tugallash", callback_data="done"),
        InlineKeyboardButton("Boshqa o'quvchi", callback_data="more")
    ]])
    await update.message.reply_text(
        f"{ctx.user_data['sname'].split()[0]} haqidagi fikr saqlandi! Davom etasizmi?",
        reply_markup=kb
    )
    return S_AFTER

async def after(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "done":
        await q.edit_message_text("Rahmat! Barcha fikrlar saqlandi. /start bosib yana ishlatishingiz mumkin.")
        return ConversationHandler.END
    kb = [[InlineKeyboardButton("9-sinf", callback_data="g_9-sinf"),
           InlineKeyboardButton("10-sinf", callback_data="g_10-sinf"),
           InlineKeyboardButton("11-sinf", callback_data="g_11-sinf")]]
    await q.edit_message_text("Qaysi sinf?", reply_markup=InlineKeyboardMarkup(kb))
    return S_GRADE

async def show_parent(update: Update, ctx: ContextTypes.DEFAULT_TYPE, sid: str):
    if sid not in ALL:
        await update.message.reply_text("O'quvchi topilmadi.")
        return ConversationHandler.END
    s = ALL[sid]
    db = load()
    fbs = db.get(sid, [])
    if not fbs:
        await update.message.reply_text(f"{s['name']} haqida hali fikr qoldirilmagan.")
        return ConversationHandler.END
    await update.message.reply_text(f"{s['name']} ({s['grade']}) - {len(fbs)} ta ustoz fikri:")
    for fb in fbs:
        head = f"{fb['teacher']} - {fb['subj']}\n"
        if fb["type"] == "voice":
            await update.message.reply_text(head)
            await update.message.reply_voice(fb["file_id"])
        else:
            await update.message.reply_text(head + fb["text"])
    await update.message.reply_text("Yangi Davr Xususiy Maktabi")
    return ConversationHandler.END

async def cmd_list(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    db = load()
    if not db:
        await update.message.reply_text("Hali fikr yoq.")
        return
    lines = [f"{ALL[sid]['name']} - {len(v)} ta" for sid, v in db.items() if sid in ALL]
    await update.message.reply_text("Fikr qoldirilganlar:\n" + "\n".join(lines))

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bekor qilindi. /start bosing.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            S_NAME:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            S_SUBJ:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_subj)],
            S_GRADE: [CallbackQueryHandler(pick_grade, pattern="^g_")],
            S_STU:   [CallbackQueryHandler(pick_stu, pattern="^s_")],
            S_FB:    [MessageHandler(filters.VOICE, recv_fb),
                      MessageHandler(filters.TEXT & ~filters.COMMAND, recv_fb)],
            S_AFTER: [CallbackQueryHandler(after, pattern="^(done|more)$")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("list", cmd_list))
    print("Bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
