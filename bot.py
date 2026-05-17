import os, json, logging
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Application, CommandHandler, MessageHandler,
                          CallbackQueryHandler, ConversationHandler,
                          filters, ContextTypes)

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN", "")

STUDENTS = {
    "9-sinf": [
        "Javohir Alijonov","Abdumannonov Muhammadshukur","Abdusalimov Xumoyunbek",
        "Abdusattorov Murodulla","Abduxoliqova Shukronaxon","Bahromjonova Parizoda",
        "Husanboyeva Nazokatxon","Isaxonov Fozilbek","Mashrabjonov Suhrobbek",
        "Muroddjonov Muhammaddiyor","Nosirov Muhammabilol","Olimova Feruzaxon",
        "Rustamova Oishabegim","To’lqinjonov Azizbek","To’lqinjonov Suhrobbek",
    ],
    "10-sinf": [
        "Tojimamatova Ruxshonaxon","Turdiyeva Muslimaxon","Xudoberganova Charosxon",
        "Abdupattoyeva Muborakxon","Alimirzayeva Yoqutxon","Bahriddinov Fazliddin",
        "Egamnazarova Behro’zabegim","Ergashyeva Mohigul","Ikromjonov Muhammadayyub",
        "In’omjonova Muniraxon","Inomjonova Zarnigorxon","Muhamadaliyev Abrorjon",
        "Muhiddinova Maftunaxon","Oripova Gulsanam","Rahimova Charosxon",
    ],
    "11-sinf": [
        "Rustamov Muhammadali","Tolibjonov Begali","Turg’unboyeva Sevara",
        "Tursunboyeva Muslima","Hoshmjonova Hilola","Abdug’aforov Iskandar",
        "Hoshmjonov Omadbek","Alijonova Dilnoza","Abobakirov Ibodulloh",
        "Abdug’aniyeva Niluzar","Abdullayeva Ruxshona","Rasulova Jamilaxon",
        "To’lqinova Durdonabonu","To’xtasinova Gulhayo","Xonkeldiyeva Marjona",
    ],
}

ALL_STUDENTS = {}
idx = 1
for grade, names in STUDENTS.items():
    for name in names:
        ALL_STUDENTS[str(idx)] = {"name": name, "grade": grade}
        idx += 1

DB_FILE = "db.json"
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {}
def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(db, f, ensure_ascii=False, indent=2)

TNAME, TSUBJECT, TGRADE, TSTUDENT, TFEEDBACK, TAFTER = range(6)

async def start(update, ctx):
    args = ctx.args
    if args and args[0].startswith("student_"):
        sid = args[0].replace("student_", "")
        return await parent_view(update, ctx, sid)
    await update.message.reply_text(
        "*Yangi Davr Xususiy Maktabi*\n_Ustoz Fikri Tizimi_\n\nAssalomu alaykum! Ismingiz va familiyangizni yozing:",
        parse_mode="Markdown", reply_markup=ReplyKeyboardRemove()
    )
    return TNAME

async def get_name(update, ctx):
    ctx.user_data["name"] = update.message.text.strip()
    await update.message.reply_text(f"Rahmat, *{ctx.user_data['name']}*!\n\nQaysi fanni o’qitasiz?", parse_mode="Markdown")
    return TSUBJECT

async def get_subject(update, ctx):
    ctx.user_data["subject"] = update.message.text.strip()
    kb = [[InlineKeyboardButton("9-sinf", callback_data="g_9-sinf"),
           InlineKeyboardButton("10-sinf", callback_data="g_10-sinf"),
           InlineKeyboardButton("11-sinf", callback_data="g_11-sinf")]]
    await update.message.reply_text("Qaysi sinf?", reply_markup=InlineKeyboardMarkup(kb))
    return TGRADE

async def pick_grade(update, ctx):
    q = update.callback_query; await q.answer()
    grade = q.data.replace("g_", "")
    ctx.user_data["grade"] = grade
    names = STUDENTS[grade]
    btns, row = [], []
    for name in names:
        sid = next(k for k,v in ALL_STUDENTS.items() if v["name"]==name and v["grade"]==grade)
        row.append(InlineKeyboardButton(name.split()[0], callback_data=f"s_{sid}"))
        if len(row)==3: btns.append(row); row=[]
    if row: btns.append(row)
    await q.edit_message_text(f"*{grade}* o’quvchilarini tanlang:", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(btns))
    return TSTUDENT

async def pick_student(update, ctx):
    q = update.callback_query; await q.answer()
    sid = q.data.replace("s_", "")
    s = ALL_STUDENTS[sid]
    ctx.user_data["sid"] = sid; ctx.user_data["sname"] = s["name"]
    await q.edit_message_text(
        f"*{s['name']}* ({s['grade']})\n\nU0001f3a4 Ovozli xabar yuboring yoki matn yozing:",
        parse_mode="Markdown")
    return TFEEDBACK

async def recv_feedback(update, ctx):
    sid = ctx.user_data["sid"]
    db = load_db()
    if sid not in db: db[sid] = []
    entry = {"teacher": ctx.user_data["name"], "subject": ctx.user_data["subject"]}
    if update.message.voice:
        entry["type"]="voice"; entry["file_id"]=update.message.voice.file_id
    elif update.message.text:
        entry["type"]="text"; entry["text"]=update.message.text
    else:
        await update.message.reply_text("Ovozli xabar yoki matn yuboring.")
        return TFEEDBACK
    db[sid].append(entry); save_db(db)
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Tugallash", callback_data="done"),
                                InlineKeyboardButton("Boshqa o’quvchi", callback_data="more")]])
    await update.message.reply_text(f"Fikr saqlandi! Yana boshqasi?", reply_markup=kb)
    return TAFTER

async def after(update, ctx):
    q = update.callback_query; await q.answer()
    if q.data=="done":
        await q.edit_message_text("Rahmat! /start bosib davom eting.")
        return ConversationHandler.END
    kb = [[InlineKeyboardButton("9-sinf",callback_data="g_9-sinf"),
           InlineKeyboardButton("10-sinf",callback_data="g_10-sinf"),
           InlineKeyboardButton("11-sinf",callback_data="g_11-sinf")]]
    await q.edit_message_text("Qaysi sinf?", reply_markup=InlineKeyboardMarkup(kb))
    return TGRADE

async def parent_view(update, ctx, sid):
    if sid not in ALL_STUDENTS:
        await update.message.reply_text("O’quvchi topilmadi."); return ConversationHandler.END
    s = ALL_STUDENTS[sid]
    db = load_db()
    feedbacks = db.get(sid, [])
    if not feedbacks:
        await update.message.reply_text(f"*{s['name']}* haqida hali fikr yo’q.", parse_mode="Markdown")
        return ConversationHandler.END
    await update.message.reply_text(f"*{s['name']}* ({s['grade']}) — {len(feedbacks)} ta ustoz fikri:", parse_mode="Markdown")
    for fb in feedbacks:
        head = f"*{fb['teacher']}* — {fb['subject']}\n"
        if fb["type"]=="voice":
            await update.message.reply_text(head, parse_mode="Markdown")
            await update.message.reply_voice(fb["file_id"])
        else:
            await update.message.reply_text(head+fb["text"], parse_mode="Markdown")
    await update.message.reply_text("_Yangi Davr Maktabi_", parse_mode="Markdown")
    return ConversationHandler.END

async def cmd_list(update, ctx):
    db = load_db()
    if not db: await update.message.reply_text("Hali fikr yo’q."); return
    lines = [f"• {ALL_STUDENTS[sid]['name']} — {len(v)} ta" for sid,v in db.items() if sid in ALL_STUDENTS]
    await update.message.reply_text("*Fikr qoldirilganlar:*\n"+chr(10).join(lines), parse_mode="Markdown")

async def cancel(update, ctx):
    await update.message.reply_text("Bekor qilindi. /start bosing.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TNAME:     [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            TSUBJECT:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_subject)],
            TGRADE:    [CallbackQueryHandler(pick_grade, pattern="^g_")],
            TSTUDENT:  [CallbackQueryHandler(pick_student, pattern="^s_")],
            TFEEDBACK: [MessageHandler(filters.VOICE, recv_feedback),
                        MessageHandler(filters.TEXT & ~filters.COMMAND, recv_feedback)],
            TAFTER:    [CallbackQueryHandler(after, pattern="^(done|more)$")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("list", cmd_list))
    print("Bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
