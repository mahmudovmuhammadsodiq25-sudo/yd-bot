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

S_NAME,S_ROLE,S_DETAIL,S_GRADE,S_STU,S_VOICE,S_REVIEW,S_EXTRA,S_AFTER = range(9)

# ── /start ────────────────────────────────────────────────────────────────
async def start(update, ctx):
    args = ctx.args or []
    if args and args[0].startswith("student_"):
        return await show_parent_menu(update, ctx, args[0].replace("student_",""))
    ctx.user_data.clear()
    await update.message.reply_text(
        "Yangi Davr Xususiy Maktabi\nUstoz Fikri Tizimi\n\n"
        "Ismingiz va familiyangizni yozing:",
        reply_markup=ReplyKeyboardRemove())
    return S_NAME

async def get_name(update, ctx):
    ctx.user_data["name"] = update.message.text.strip()
    kb = [[
        InlineKeyboardButton("📚 Fan o'qituvchisi", callback_data="r_teacher"),
        InlineKeyboardButton("🏫 Maktab xodimi", callback_data="r_staff"),
    ]]
    await update.message.reply_text(
        f"Rahmat {ctx.user_data['name']}!\n\n"
        "Siz kim sifatida fikr bildirasiz?",
        reply_markup=InlineKeyboardMarkup(kb))
    return S_ROLE

async def pick_role(update, ctx):
    q = update.callback_query; await q.answer()
    role = q.data.replace("r_","")
    ctx.user_data["role"] = role
    if role == "teacher":
        await q.edit_message_text(
            f"📚 Fan o'qituvchisi: {ctx.user_data['name']}\n\n"
            "Qaysi fanni o'qitasiz?\n"
            "(Masalan: Matematika, Ingliz tili, Ona tili, IT, Fizika...)")
    else:
        await q.edit_message_text(
            f"🏫 Maktab xodimi: {ctx.user_data['name']}\n\n"
            "Lavozimingiz nima?\n"
            "(Masalan: Direktor, Direktor o'rinbosari, Sinf rahbari, Psixolog...)")
    return S_DETAIL

async def get_detail(update, ctx):
    ctx.user_data["detail"] = update.message.text.strip()
    kb = [[InlineKeyboardButton("9-sinf (18 ta)", callback_data="g_9-sinf"),
           InlineKeyboardButton("10-sinf (20 ta)", callback_data="g_10-sinf")],
          [InlineKeyboardButton("11-sinf (7 ta)", callback_data="g_11-sinf")]]
    await update.message.reply_text("Qaysi sinf o'quvchisi haqida fikr bildirasiz?",
                                     reply_markup=InlineKeyboardMarkup(kb))
    return S_GRADE

async def pick_grade(update, ctx):
    q = update.callback_query; await q.answer()
    ctx.user_data["grade"] = q.data.replace("g_","")
    return await _show_list(q, ctx, ctx.user_data["grade"])

async def _show_list(q, ctx, grade):
    db = load_db()
    teacher = ctx.user_data["name"]
    done = {sid for sid,fbs in db.items() for fb in fbs if fb.get("teacher")==teacher}
    rows, row, cnt = [], [], 0
    for sid, info in ALL.items():
        if info["grade"] != grade: continue
        cnt += 1
        lbl = f"{cnt}. {'✅ ' if sid in done else ''}{info['display']}"
        row.append(InlineKeyboardButton(lbl, callback_data=f"s_{sid}"))
        if len(row)==2: rows.append(row); row = []
    if row: rows.append(row)
    rows.append([InlineKeyboardButton("🔙 Sinf tanlash", callback_data="back_grade")])
    txt = f"{grade} o'quvchilari (tartib raqami bilan):\n(✅ — siz fikr bildirganlar)"
    try: await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(rows))
    except: await q.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(rows))
    return S_STU

async def pick_stu(update, ctx):
    q = update.callback_query; await q.answer()
    if q.data == "back_grade":
        kb = [[InlineKeyboardButton("9-sinf", callback_data="g_9-sinf"),
               InlineKeyboardButton("10-sinf", callback_data="g_10-sinf")],
              [InlineKeyboardButton("11-sinf", callback_data="g_11-sinf")]]
        await q.edit_message_text("Sinf tanlang:", reply_markup=InlineKeyboardMarkup(kb))
        return S_GRADE
    sid = q.data.replace("s_",""); s = ALL[sid]
    ctx.user_data["sid"] = sid; ctx.user_data["sname"] = s["name"]
    await q.edit_message_text(
        f"{s['name']} ({s['grade']})\n\n"
        f"🎙 Ovozli xabar yuboring:\n"
        f"1. Mikrofonni bosing va gapiring\n"
        f"2. Tugatgach, ovoz eshitiladi\n"
        f"3. Tasdiqlash yoki qayta yozish")
    return S_VOICE

async def recv_voice(update, ctx):
    ctx.user_data["vfid"] = update.message.voice.file_id
    ctx.user_data["vdur"] = update.message.voice.duration
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Tasdiqlash", callback_data="ok_voice"),
        InlineKeyboardButton("🔄 Qayta yozish", callback_data="redo_voice")]])
    await update.message.reply_voice(
        voice=update.message.voice.file_id,
        caption=f"Ovoz xabaringiz ({update.message.voice.duration} sek)\nEshitib ko'ring:",
        reply_markup=kb)
    return S_REVIEW

async def review_voice(update, ctx):
    q = update.callback_query; await q.answer()
    if q.data == "redo_voice":
        await q.edit_message_caption(caption="Qayta yozing — mikrofonni bosing:")
        return S_VOICE
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("➡️ O'tkazib yuborish", callback_data="skip_extra")]])
    await q.edit_message_caption(caption="✅ Ovoz tasdiqlandi! Qo'shimcha yozma fikr bo'lsa yozing:")
    await q.message.reply_text("Yozma fikr (ixtiyoriy):", reply_markup=kb)
    return S_EXTRA

async def recv_extra(update, ctx):
    ctx.user_data["extra"] = update.message.text.strip()
    return await _save(update.message, ctx)

async def skip_extra(update, ctx):
    q = update.callback_query; await q.answer()
    ctx.user_data["extra"] = ""
    await q.edit_message_text("Saqlanmoqda...")
    return await _save(q.message, ctx)

async def _save(msg, ctx):
    sid = ctx.user_data["sid"]; db = load_db()
    if sid not in db: db[sid] = []
    db[sid].append({
        "teacher": ctx.user_data["name"],
        "role": ctx.user_data["role"],
        "detail": ctx.user_data["detail"],
        "type": "voice",
        "file_id": ctx.user_data["vfid"],
        "duration": ctx.user_data.get("vdur", 0),
        "extra": ctx.user_data.get("extra", ""),
    })
    save_db(db)
    grade = ALL[sid]["grade"]
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🏠 Boshiga qaytish", callback_data="go_start"),
        InlineKeyboardButton("➡️ Davom ettirish", callback_data=f"cont_{grade.replace('-sinf','')}_{sid}")]])
    await msg.reply_text(f"✅ {ctx.user_data['sname']} haqidagi fikr saqlandi!\n\nNima qilasiz?", reply_markup=kb)
    return S_AFTER

async def after_action(update, ctx):
    q = update.callback_query; await q.answer()
    if q.data == "go_start":
        ctx.user_data.clear()
        await q.edit_message_text("Ismingizni yozing:")
        return S_NAME
    if q.data.startswith("cont_"):
        parts = q.data.split("_", 2)
        grade = parts[1] + "-sinf"
        ctx.user_data["grade"] = grade
        return await _show_list(q, ctx, grade)

# ═════════════ OTA-ONA QISMI ═════════════════════════════════════════════
async def show_parent_menu(update, ctx, sid):
    if sid not in ALL:
        await update.message.reply_text("O'quvchi topilmadi.")
        return ConversationHandler.END
    s = ALL[sid]
    db = load_db()
    fbs = db.get(sid, [])
    if not fbs:
        await update.message.reply_text(
            f"📭 {s['name']} ({s['grade']}) haqida hali fikr qoldirilmagan.\n"
            f"Bir ozdan so'ng qayta tekshiring.")
        return ConversationHandler.END
    
    # Fikrlarni rolga ajratamiz
    teacher_fbs = [f for f in fbs if f.get("role") == "teacher"]
    staff_fbs = [f for f in fbs if f.get("role") == "staff"]
    # Eski yozuvlar uchun (role yo'q bo'lsa - teacher deb hisoblanadi)
    legacy_fbs = [f for f in fbs if "role" not in f]
    teacher_fbs.extend(legacy_fbs)
    
    ctx.user_data["parent_sid"] = sid
    
    kb_rows = []
    if teacher_fbs:
        kb_rows.append([InlineKeyboardButton(
            f"📚 Fan ustozlar fikri ({len(teacher_fbs)} ta)",
            callback_data=f"pcat_t_{sid}")])
    if staff_fbs:
        kb_rows.append([InlineKeyboardButton(
            f"🏫 Maktab xodimlari fikri ({len(staff_fbs)} ta)",
            callback_data=f"pcat_s_{sid}")])
    
    await update.message.reply_text(
        f"👨‍👩‍👧 {s['name']} ({s['grade']})\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Jami: {len(fbs)} ta fikr\n\n"
        f"Bo'limni tanlang:",
        reply_markup=InlineKeyboardMarkup(kb_rows))
    return ConversationHandler.END

async def parent_category(update, ctx):
    q = update.callback_query; await q.answer()
    parts = q.data.split("_")
    cat = parts[1]  # 't' or 's'
    sid = parts[2]
    s = ALL.get(sid)
    if not s:
        await q.edit_message_text("Xato"); return
    db = load_db()
    fbs = db.get(sid, [])
    
    if cat == "t":
        items = [f for f in fbs if f.get("role") == "teacher" or "role" not in f]
        title = "📚 Fan ustozlar fikri"
    else:
        items = [f for f in fbs if f.get("role") == "staff"]
        title = "🏫 Maktab xodimlari fikri"
    
    if not items:
        await q.edit_message_text(f"{title} - bo'sh."); return
    
    # Tugmalar: har bir fan/lavozim alohida
    kb_rows = []
    for i, fb in enumerate(items):
        detail = fb.get("detail", fb.get("pos", "?"))
        teacher = fb.get("teacher", "?")
        # Tugma matni: Fan/Lavozim — Ustoz ismi
        btn_text = f"{detail} — {teacher}"
        if len(btn_text) > 50: btn_text = btn_text[:47] + "..."
        kb_rows.append([InlineKeyboardButton(btn_text, callback_data=f"pfb_{sid}_{cat}_{i}")])
    kb_rows.append([InlineKeyboardButton("🔙 Orqaga", callback_data=f"pback_{sid}")])
    
    await q.edit_message_text(
        f"{title}\n━━━━━━━━━━━━━━━━━━━━\n{s['name']}\n\n"
        f"Quyidagilardan tanlang:",
        reply_markup=InlineKeyboardMarkup(kb_rows))

async def parent_show_fb(update, ctx):
    q = update.callback_query; await q.answer()
    parts = q.data.split("_")
    sid = parts[1]; cat = parts[2]; idx = int(parts[3])
    db = load_db()
    fbs = db.get(sid, [])
    if cat == "t":
        items = [f for f in fbs if f.get("role") == "teacher" or "role" not in f]
    else:
        items = [f for f in fbs if f.get("role") == "staff"]
    if idx >= len(items): return
    fb = items[idx]
    s = ALL[sid]
    
    detail = fb.get("detail", fb.get("pos", ""))
    teacher = fb.get("teacher", "?")
    role_label = "Fan ustozi" if (fb.get("role") == "teacher" or "role" not in fb) else "Maktab xodimi"
    
    header = (f"👤 O'quvchi: {s['name']}\n"
              f"━━━━━━━━━━━━━━━━━━━━\n"
              f"🧑‍🏫 {teacher}\n"
              f"📌 {role_label}: {detail}")
    
    await q.message.reply_text(header)
    
    if fb.get("type") == "voice" and fb.get("file_id"):
        await q.message.reply_voice(
            voice=fb["file_id"],
            caption=f"🎙 Ovozli fikr ({fb.get('duration', 0)} sek)")
    
    if fb.get("extra"):
        await q.message.reply_text(f"💬 Qo'shimcha yozma fikr:\n\n{fb['extra']}")
    elif fb.get("text"):
        await q.message.reply_text(f"💬 Yozma fikr:\n\n{fb['text']}")
    
    # Orqaga tugmasi
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔙 Ro'yxatga qaytish", callback_data=f"pcat_{cat}_{sid}"),
        InlineKeyboardButton("🏠 Bosh menyu", callback_data=f"pback_{sid}")]])
    await q.message.reply_text("Davom etish:", reply_markup=kb)

async def parent_back(update, ctx):
    q = update.callback_query; await q.answer()
    sid = q.data.replace("pback_", "")
    s = ALL.get(sid)
    if not s: return
    db = load_db()
    fbs = db.get(sid, [])
    teacher_fbs = [f for f in fbs if f.get("role") == "teacher" or "role" not in f]
    staff_fbs = [f for f in fbs if f.get("role") == "staff"]
    
    kb_rows = []
    if teacher_fbs:
        kb_rows.append([InlineKeyboardButton(
            f"📚 Fan ustozlar fikri ({len(teacher_fbs)} ta)",
            callback_data=f"pcat_t_{sid}")])
    if staff_fbs:
        kb_rows.append([InlineKeyboardButton(
            f"🏫 Maktab xodimlari fikri ({len(staff_fbs)} ta)",
            callback_data=f"pcat_s_{sid}")])
    
    await q.message.reply_text(
        f"👨‍👩‍👧 {s['name']} ({s['grade']})\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Jami: {len(fbs)} ta fikr\n\nBo'limni tanlang:",
        reply_markup=InlineKeyboardMarkup(kb_rows))

# ── Admin /list ───────────────────────────────────────────────────────────
async def cmd_list(update, ctx):
    db = load_db()
    if not db: await update.message.reply_text("Hali fikr yo'q."); return
    lines = []
    for sid, fbs in db.items():
        if sid in ALL:
            t = sum(1 for f in fbs if f.get("role")=="teacher" or "role" not in f)
            s = sum(1 for f in fbs if f.get("role")=="staff")
            lines.append(f"{ALL[sid]['name']} ({ALL[sid]['grade']}) - Ustoz:{t}, Xodim:{s}")
    await update.message.reply_text("Fikr qoldirilganlar:\n" + "\n".join(lines))

async def cancel(update, ctx):
    await update.message.reply_text("Bekor qilindi. /start bosing.")
    return ConversationHandler.END

def main():
    if not TOKEN: raise ValueError("BOT_TOKEN not set!")
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            S_NAME:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            S_ROLE:   [CallbackQueryHandler(pick_role, pattern="^r_")],
            S_DETAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_detail)],
            S_GRADE:  [CallbackQueryHandler(pick_grade, pattern="^g_")],
            S_STU:    [CallbackQueryHandler(pick_stu, pattern="^(s_|back_grade)")],
            S_VOICE:  [MessageHandler(filters.VOICE, recv_voice)],
            S_REVIEW: [CallbackQueryHandler(review_voice, pattern="^(ok_voice|redo_voice)$")],
            S_EXTRA:  [MessageHandler(filters.TEXT & ~filters.COMMAND, recv_extra),
                       CallbackQueryHandler(skip_extra, pattern="^skip_extra$")],
            S_AFTER:  [CallbackQueryHandler(after_action, pattern="^(go_start|cont_)")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    app.add_handler(conv)
    # Parent view callbacks (outside conversation)
    app.add_handler(CallbackQueryHandler(parent_category, pattern="^pcat_"))
    app.add_handler(CallbackQueryHandler(parent_show_fb, pattern="^pfb_"))
    app.add_handler(CallbackQueryHandler(parent_back, pattern="^pback_"))
    app.add_handler(CommandHandler("list", cmd_list))
    print("Bot v5 ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
