import os, json, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
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
        "Rustamova Oishabegim","To'lqinjonov Azizbek","To'lqinjonov Suhrobbek",
        "Tojimamatova Ruxshonaxon","Turdiyeva Muslimaxon","Xudoberganova Charosxon",
    ],
    "10-sinf": [
        "Abdupattoyeva Muborakxon","Alimirzayeva Yoqutxon","Bahriddinov Fazliddin",
        "Egamnazarova Behro'zabegim","Ergashyeva Mohigul","Ikromjonov Muhammadayyub",
        "In'omjonova Muniraxon","Inomjonova Zarnigorxon","Muhamadaliyev Abrorjon",
        "Muhiddinova Maftunaxon","Oripova Gulsanam","Rahimova Charosxon",
        "Rustamov Muhammadali","Tolibjonov Begali","Turg'unboyeva Sevara",
        "Tursunboyeva Muslima","Hoshmjonova Hilola","Abdug'aforov Iskandar",
        "Hoshmjonov Omadbek","Alijonova Dilnoza",
    ],
    "11-sinf": [
        "Abobakirov Ibodulloh","Abdug'aniyeva Niluzar","Abdullayeva Ruxshona",
        "Rasulova Jamilaxon","To'lqinova Durdonabonu","To'xtasinova Gulhayo",
        "Xonkeldiyeva Marjona",
    ],
}

DUPES = {"Suhrobbek","Charosxon"}

def get_ism(name):
    p = name.strip().split()
    if len(p) == 1: return p[0]
    fam_e = ("ov","ova","ev","eva","jonov","jonova","boyev","boyeva","iyev","iyeva",
             "matov","matova","nazarov","nazarova","qodirov","qodirova","aliyev",
             "aliyeva","yunov","yunova","xonov","xonova","murodov","murodova")
    return p[-1] if any(p[0].lower().endswith(e) for e in fam_e) else p[0]

def build_all():
    ism_cnt = {}
    for g, ns in STUDENTS.items():
        for n in ns:
            i = get_ism(n); ism_cnt[i] = ism_cnt.get(i, 0) + 1
    out = {}
    idx = 1
    for g, ns in STUDENTS.items():
        for n in ns:
            ism = get_ism(n)
            p = n.strip().split()
            if ism_cnt[ism] > 1:
                fam = p[0] if get_ism(n) == p[-1] else p[-1]
                disp = f"{fam} {ism[0]}."
            else:
                disp = ism
            out[str(idx)] = {"name": n, "grade": g, "display": disp}
            idx += 1
    return out

ALL = build_all()
DB = "db.json"
def load_db():
    try:
        with open(DB,"r",encoding="utf-8") as f: return json.load(f)
    except: return {}
def save_db(db):
    with open(DB,"w",encoding="utf-8") as f: json.dump(db,f,ensure_ascii=False,indent=2)

S_NAME,S_POS,S_GRADE,S_STU,S_VOICE,S_REVIEW,S_EXTRA,S_AFTER = range(8)

async def start(update,ctx):
    args = ctx.args or []
    if args and args[0].startswith("student_"):
        return await show_parent(update,ctx,args[0].replace("student_",""))
    ctx.user_data.clear()
    await update.message.reply_text(
        "Yangi Davr Xususiy Maktabi\nUstoz Fikri Tizimi\n\nIsmingiz va familiyangizni yozing:",
        reply_markup=ReplyKeyboardRemove())
    return S_NAME

async def get_name(update,ctx):
    ctx.user_data["name"] = update.message.text.strip()
    await update.message.reply_text(f"Rahmat {ctx.user_data['name']}!\n\nKim bo'lib ishlaysiz?\n(Masalan: Matematika o'qituvchisi, Sinf rahbari, Psixolog...)")
    return S_POS

async def get_pos(update,ctx):
    ctx.user_data["pos"] = update.message.text.strip()
    kb = [[InlineKeyboardButton("9-sinf (18 ta)",callback_data="g_9-sinf"),
           InlineKeyboardButton("10-sinf (20 ta)",callback_data="g_10-sinf")],
          [InlineKeyboardButton("11-sinf (7 ta)",callback_data="g_11-sinf")]]
    await update.message.reply_text("Qaysi sinf?",reply_markup=InlineKeyboardMarkup(kb))
    return S_GRADE

async def pick_grade(update,ctx):
    q=update.callback_query; await q.answer()
    ctx.user_data["grade"] = q.data.replace("g_","")
    return await _show_list(q,ctx,ctx.user_data["grade"])

async def _show_list(q,ctx,grade):
    db = load_db()
    teacher = ctx.user_data["name"]
    done = {sid for sid,fbs in db.items() for fb in fbs if fb.get("teacher")==teacher}
    rows,row,cnt = [],[],0
    for sid,info in ALL.items():
        if info["grade"]!=grade: continue
        cnt+=1
        lbl = f"{cnt}. {'✅ ' if sid in done else ''}{info['display']}"
        row.append(InlineKeyboardButton(lbl,callback_data=f"s_{sid}"))
        if len(row)==2: rows.append(row); row=[]
    if row: rows.append(row)
    rows.append([InlineKeyboardButton("Sinf tanlash",callback_data="back_grade")])
    txt = f"{grade} o'quvchilari (tartib raqami bilan):"
    try: await q.edit_message_text(txt,reply_markup=InlineKeyboardMarkup(rows))
    except: await q.message.reply_text(txt,reply_markup=InlineKeyboardMarkup(rows))
    return S_STU

async def pick_stu(update,ctx):
    q=update.callback_query; await q.answer()
    if q.data=="back_grade":
        kb=[[InlineKeyboardButton("9-sinf",callback_data="g_9-sinf"),
             InlineKeyboardButton("10-sinf",callback_data="g_10-sinf")],
            [InlineKeyboardButton("11-sinf",callback_data="g_11-sinf")]]
        await q.edit_message_text("Sinf tanlang:",reply_markup=InlineKeyboardMarkup(kb))
        return S_GRADE
    sid=q.data.replace("s_",""); s=ALL[sid]
    ctx.user_data["sid"]=sid; ctx.user_data["sname"]=s["name"]
    await q.edit_message_text(
        f"{s['name']} ({s['grade']})\n\n"
        f"Ovozli xabar yuboring:\n"
        f"1. Mikrofonni bosing va gapirishni boshlang\n"
        f"2. Tugatgach xabar keladi\n"
        f"3. Eshitib ko'rasiz, keyin tasdiqlaysiz")
    return S_VOICE

async def recv_voice(update,ctx):
    ctx.user_data["vfid"]=update.message.voice.file_id
    ctx.user_data["vdur"]=update.message.voice.duration
    kb=InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Tasdiqlash",callback_data="ok_voice"),
        InlineKeyboardButton("Qayta yozish",callback_data="redo_voice")]])
    await update.message.reply_voice(
        voice=update.message.voice.file_id,
        caption=f"Ovoz xabaringiz ({update.message.voice.duration} sek)\nEshitib ko'ring:",
        reply_markup=kb)
    return S_REVIEW

async def review_voice(update,ctx):
    q=update.callback_query; await q.answer()
    if q.data=="redo_voice":
        await q.edit_message_caption(caption="Qayta yozing — mikrofonni bosing:")
        return S_VOICE
    kb=InlineKeyboardMarkup([[InlineKeyboardButton("O'tkazib yuborish",callback_data="skip_extra")]])
    await q.edit_message_caption(caption="Ovoz tasdiqlandi! Qo'shimcha yozma fikr bo'lsa yozing:")
    await q.message.reply_text("Yozma fikr (ixtiyoriy):",reply_markup=kb)
    return S_EXTRA

async def recv_extra(update,ctx):
    ctx.user_data["extra"]=update.message.text.strip()
    return await _save(update.message,ctx)

async def skip_extra(update,ctx):
    q=update.callback_query; await q.answer()
    ctx.user_data["extra"]=""
    await q.edit_message_text("Saqlanmoqda...")
    return await _save(q.message,ctx)

async def _save(msg,ctx):
    sid=ctx.user_data["sid"]; db=load_db()
    if sid not in db: db[sid]=[]
    db[sid].append({"teacher":ctx.user_data["name"],"pos":ctx.user_data["pos"],
                    "type":"voice","file_id":ctx.user_data["vfid"],
                    "duration":ctx.user_data.get("vdur",0),"extra":ctx.user_data.get("extra","")})
    save_db(db)
    grade=ALL[sid]["grade"]
    kb=InlineKeyboardMarkup([[
        InlineKeyboardButton("Boshiga qaytish",callback_data="go_start"),
        InlineKeyboardButton("Davom ettirish",callback_data=f"cont_{grade.replace('-sinf','')}_{sid}")]])
    await msg.reply_text(
        f"{ctx.user_data['sname']} haqidagi fikr saqlandi!\n\nNima qilasiz?",
        reply_markup=kb)
    return S_AFTER

async def after_action(update,ctx):
    q=update.callback_query; await q.answer()
    if q.data=="go_start":
        ctx.user_data.clear()
        await q.edit_message_text("Ismingizni yozing:")
        return S_NAME
    if q.data.startswith("cont_"):
        parts=q.data.split("_",2)
        grade=parts[1]+"-sinf"
        ctx.user_data["grade"]=grade
        return await _show_list(q,ctx,grade)

async def show_parent(update,ctx,sid):
    if sid not in ALL:
        await update.message.reply_text("O'quvchi topilmadi."); return ConversationHandler.END
    s=ALL[sid]; db=load_db(); fbs=db.get(sid,[])
    if not fbs:
        await update.message.reply_text(f"{s['name']} haqida fikr yo'q."); return ConversationHandler.END
    await update.message.reply_text(f"{s['name']} ({s['grade']}) - {len(fbs)} ta fikr:")
    for i,fb in enumerate(fbs,1):
        head=f"{i}. {fb['teacher']} ({fb.get('pos','')})\n"
        if fb["type"]=="voice":
            await update.message.reply_text(head)
            await update.message.reply_voice(fb["file_id"])
            if fb.get("extra"): await update.message.reply_text(f"Qo'shimcha: {fb['extra']}")
        else:
            await update.message.reply_text(head+(fb.get("text") or fb.get("extra","")))
    await update.message.reply_text("Yangi Davr Xususiy Maktabi")
    return ConversationHandler.END

async def cmd_list(update,ctx):
    db=load_db()
    if not db: await update.message.reply_text("Hali fikr yoq."); return
    lines=[f"{ALL[s]['name']} ({ALL[s]['grade']}) - {len(v)} ta" for s,v in db.items() if s in ALL]
    await update.message.reply_text("Fikr qoldirilganlar:\n"+chr(10).join(lines))

async def cancel(update,ctx):
    await update.message.reply_text("Bekor qilindi. /start bosing.")
    return ConversationHandler.END

def main():
    if not TOKEN: raise ValueError("BOT_TOKEN not set!")
    app=Application.builder().token(TOKEN).build()
    conv=ConversationHandler(
        entry_points=[CommandHandler("start",start)],
        states={
            S_NAME:  [MessageHandler(filters.TEXT & ~filters.COMMAND,get_name)],
            S_POS:   [MessageHandler(filters.TEXT & ~filters.COMMAND,get_pos)],
            S_GRADE: [CallbackQueryHandler(pick_grade,pattern="^g_")],
            S_STU:   [CallbackQueryHandler(pick_stu,pattern="^(s_|back_grade)")],
            S_VOICE: [MessageHandler(filters.VOICE,recv_voice)],
            S_REVIEW:[CallbackQueryHandler(review_voice,pattern="^(ok_voice|redo_voice)$")],
            S_EXTRA: [MessageHandler(filters.TEXT & ~filters.COMMAND,recv_extra),
                      CallbackQueryHandler(skip_extra,pattern="^skip_extra$")],
            S_AFTER: [CallbackQueryHandler(after_action,pattern="^(go_start|cont_)")],
        },
        fallbacks=[CommandHandler("cancel",cancel)],
        allow_reentry=True,
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("list",cmd_list))
    print("Bot v4 ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES,drop_pending_updates=True)

if __name__=="__main__":
    main()
