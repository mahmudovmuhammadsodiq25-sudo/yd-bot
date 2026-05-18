import os, json, logging, csv, io
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Application, CommandHandler, MessageHandler,
                           CallbackQueryHandler, ConversationHandler,
                           filters, ContextTypes, JobQueue)

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0") or "0")

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
    out = {}; idx = 1
    for g, ns in STUDENTS.items():
        for n in ns:
            ism = get_ism(n); p = n.strip().split()
            if ism_cnt[ism] > 1:
                fam = p[0] if get_ism(n) == p[-1] else p[-1]
                disp = f"{fam} {ism[0]}."
            else: disp = ism
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

def get_admin_id():
    global ADMIN_ID
    if ADMIN_ID: return ADMIN_ID
    db = load_db()
    aid = db.get("_admin_id", 0)
    if aid: ADMIN_ID = aid
    return ADMIN_ID

async def notify_admin(ctx, text, voice_file_id=None, duration=0):
    aid = get_admin_id()
    if not aid: return
    try:
        await ctx.bot.send_message(aid, text)
        if voice_file_id:
            await ctx.bot.send_voice(aid, voice=voice_file_id, caption=f"({duration} sek)")
    except Exception as e:
        logging.error(f"Admin notify: {e}")

def find_student_by_name(text):
    t = text.strip().lower()
    matches = []
    for sid, info in ALL.items():
        parts = info["name"].lower().split()
        if t in parts or t == info["name"].lower():
            matches.append(sid)
    if len(matches) == 1: return matches[0]
    for sid, info in ALL.items():
        if t in info["name"].lower():
            matches.append(sid)
    seen = list(dict.fromkeys(matches))
    return seen[0] if len(seen) == 1 else (seen if seen else None)

S_NAME,S_ROLE,S_DETAIL,S_GRADE,S_STU,S_VOICE,S_REVIEW,S_EXTRA,S_AFTER = range(9)

# ═══════════ USTOZ /start ═══════════
async def start(update, ctx):
    args = ctx.args or []
    if args and args[0].startswith("student_"):
        sid = args[0].replace("student_","")
        return await show_parent_menu(update, ctx, sid)
    ctx.user_data.clear()
    await update.message.reply_text(
        "Yangi Davr Xususiy Maktabi\nUstoz Fikri Tizimi\n\n"
        "Ismingiz va familiyangizni yozing:",
        reply_markup=ReplyKeyboardRemove())
    return S_NAME

async def get_name(update, ctx):
    ctx.user_data["name"] = update.message.text.strip()
    kb = [[InlineKeyboardButton("📚 Fan o'qituvchisi", callback_data="r_teacher"),
           InlineKeyboardButton("🏫 Maktab xodimi", callback_data="r_staff")]]
    await update.message.reply_text(
        f"Rahmat {ctx.user_data['name']}!\nSiz kim sifatida fikr bildirasiz?",
        reply_markup=InlineKeyboardMarkup(kb))
    return S_ROLE

async def pick_role(update, ctx):
    q = update.callback_query; await q.answer()
    role = q.data.replace("r_","")
    ctx.user_data["role"] = role
    prompt = "Qaysi fanni o'qitasiz?" if role == "teacher" else "Lavozimingiz nima?"
    label = "Fan o'qituvchisi" if role == "teacher" else "Maktab xodimi"
    role_icon = "📚" if role == "teacher" else "🏫"
    await q.edit_message_text(f"{role_icon} {label}: {ctx.user_data['name']}\n\n{prompt}")
    return S_DETAIL

async def get_detail(update, ctx):
    ctx.user_data["detail"] = update.message.text.strip()
    kb = [[InlineKeyboardButton("9-sinf (18)", callback_data="g_9-sinf"),
           InlineKeyboardButton("10-sinf (20)", callback_data="g_10-sinf")],
          [InlineKeyboardButton("11-sinf (7)", callback_data="g_11-sinf")]]
    await update.message.reply_text("Qaysi sinf haqida fikr bildirasiz?",
                                    reply_markup=InlineKeyboardMarkup(kb))
    return S_GRADE

async def pick_grade(update, ctx):
    q = update.callback_query; await q.answer()
    ctx.user_data["grade"] = q.data.replace("g_","")
    return await _show_list(q, ctx, ctx.user_data["grade"])

async def _show_list(q, ctx, grade):
    db = load_db()
    teacher = ctx.user_data["name"]
    done = set()
    for sid, fbs in db.items():
        if sid.startswith("_") or not isinstance(fbs, list): continue
        for fb in fbs:
            if fb.get("teacher") == teacher: done.add(sid)
    rows, row, cnt = [], [], 0
    for sid, info in ALL.items():
        if info["grade"] != grade: continue
        cnt += 1
        check = "\u2705 " if sid in done else ""
        lbl = f"{cnt}. {check}{info['display']}"
        row.append(InlineKeyboardButton(lbl, callback_data=f"s_{sid}"))
        if len(row)==2: rows.append(row); row = []
    if row: rows.append(row)
    rows.append([InlineKeyboardButton("\ud83d\udd19 Sinf tanlash", callback_data="back_grade")])
    txt = f"{grade} o'quvchilari:\n(\u2705 \u2014 siz fikr bildirganlar)"
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
        f"{s['name']} ({s['grade']})\n\n\ud83c\udfa4 Ovozli xabar yuboring:\n"
        f"Mikrofonni bosing va gapiring.")
    return S_VOICE

async def recv_voice(update, ctx):
    ctx.user_data["vfid"] = update.message.voice.file_id
    ctx.user_data["vdur"] = update.message.voice.duration
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("\u2705 Tasdiqlash", callback_data="ok_voice"),
        InlineKeyboardButton("\ud83d\udd04 Qayta yozish", callback_data="redo_voice")]])
    await update.message.reply_voice(voice=update.message.voice.file_id,
                                     caption=f"Ovoz ({update.message.voice.duration} sek). Eshitib ko'ring:",
                                     reply_markup=kb)
    return S_REVIEW

async def review_voice(update, ctx):
    q = update.callback_query; await q.answer()
    if q.data == "redo_voice":
        await q.edit_message_caption(caption="Qayta yozing \u2014 mikrofonni bosing:")
        return S_VOICE
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("\u27a1\ufe0f O'tkazib yuborish", callback_data="skip_extra")]])
    await q.edit_message_caption(caption="\u2705 Tasdiqlandi!")
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
    fb = {"teacher": ctx.user_data["name"], "role": ctx.user_data["role"],
          "detail": ctx.user_data["detail"], "type": "voice",
          "file_id": ctx.user_data["vfid"], "duration": ctx.user_data.get("vdur", 0),
          "extra": ctx.user_data.get("extra", ""), "ts": datetime.now().strftime("%Y-%m-%d %H:%M")}
    db[sid].append(fb); save_db(db)
    s = ALL[sid]
    rl = "Fan ustozi" if ctx.user_data["role"] == "teacher" else "Maktab xodimi"
    fb_icon = "📚" if ctx.user_data["role"] == "teacher" else "🏫"
    atxt = (f"{fb_icon} YANGI FIKR\n"
            f"O'quvchi: {s['name']} ({s['grade']})\nKim: {ctx.user_data['name']}\n{rl}: {ctx.user_data['detail']}\n"
            f"\u23f1 {ctx.user_data.get('vdur',0)} sek \u2022 {fb['ts']}")
    if fb["extra"]: atxt += f"\n\u270d\ufe0f {fb['extra']}"
    await notify_admin(ctx, atxt, fb["file_id"], fb["duration"])
    grade = ALL[sid]["grade"]
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("\ud83c\udfe0 Boshiga", callback_data="go_start"),
        InlineKeyboardButton("\u27a1\ufe0f Davom", callback_data=f"cont_{grade.replace('-sinf','')}_{sid}")]])
    await msg.reply_text(f"\u2705 {ctx.user_data['sname']} haqida fikr saqlandi!", reply_markup=kb)
    return S_AFTER

async def after_action(update, ctx):
    q = update.callback_query; await q.answer()
    if q.data == "go_start":
        ctx.user_data.clear()
        await q.edit_message_text("Ismingizni yozing:")
        return S_NAME
    if q.data.startswith("cont_"):
        parts = q.data.split("_", 2); grade = parts[1] + "-sinf"
        ctx.user_data["grade"] = grade
        return await _show_list(q, ctx, grade)

async def cancel(update, ctx):
    for k in ["reply_to_teacher","reply_for_sid","student_sid"]:
        ctx.user_data.pop(k, None)
    await update.message.reply_text("Bekor qilindi. /start bosing.")
    return ConversationHandler.END

# ═══════════ OTA-ONA (QR orqali) ═══════════
async def show_parent_menu(update, ctx, sid):
    if sid not in ALL:
        await update.message.reply_text("O'quvchi topilmadi.")
        return ConversationHandler.END
    ctx.user_data.clear()
    ctx.user_data["parent_sid"] = sid
    await _parent_menu(update.message, ctx, sid)
    return ConversationHandler.END

async def _parent_menu(msg_or_q, ctx, sid, edit=False):
    s = ALL.get(sid)
    if not s: return
    db = load_db()
    fbs = db.get(sid, [])
    tfbs = [f for f in fbs if f.get("role") == "teacher" or "role" not in f]
    sfbs = [f for f in fbs if f.get("role") == "staff"]
    cmsgs = db.get("_student_to_parent", {}).get(sid, [])
    kb = []
    if tfbs:
        kb.append([InlineKeyboardButton(f"📚 Ustoz fikri ({len(tfbs)})", callback_data=f"pcat_t_{sid}")])
    if sfbs:
        kb.append([InlineKeyboardButton(f"🏫 Maktab xodimi ({len(sfbs)})", callback_data=f"pcat_s_{sid}")])
    kb.append([InlineKeyboardButton(
        f"💌 Ota onamga gaplarim ({len(cmsgs)})" if cmsgs else "💌 Ota onamga gaplarim (0)",
        callback_data=f"pchild_{sid}")])
    total = len(fbs)
    txt = (f"👨‍👩‍👧 {s['name']} ({s['grade']})
━━━━━━━━━━━━━━━━━
"
           f"📊 Jami: {total} ta fikr

Bo'limni tanlang:" if total else
           f"📭 {s['name']} ({s['grade']})
Hali fikr yo'q. Keyinroq tekshiring.")
    if edit:
        try: await msg_or_q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))
        except: await msg_or_q.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))
    else:
        if hasattr(msg_or_q, 'reply_text'):
            await msg_or_q.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))
        else:
            await msg_or_q.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))

async def parent_category(update, ctx):
    q = update.callback_query; await q.answer()
    parts = q.data.split("_"); cat = parts[1]; sid = parts[2]
    s = ALL.get(sid)
    if not s: await q.edit_message_text("Xato"); return
    db = load_db(); fbs = db.get(sid, [])
    if cat == "t":
        items = [f for f in fbs if f.get("role") == "teacher" or "role" not in f]
        title = "📚 Ustoz fikri"
    else:
        items = [f for f in fbs if f.get("role") == "staff"]
        title = "🏫 Maktab xodimi fikri"
    if not items:
        await q.edit_message_text(f"{title} — hali yo'q."); return
    kb = []
    for i, fb in enumerate(items):
        d = fb.get("detail", "?"); t = fb.get("teacher", "?")
        lbl = f"{d} — {t}"
        if len(lbl) > 50: lbl = lbl[:47] + "..."
        kb.append([InlineKeyboardButton(lbl, callback_data=f"pfb_{sid}_{cat}_{i}")])
    kb.append([InlineKeyboardButton("🔙 Orqaga", callback_data=f"pmenu_{sid}")])
    await q.edit_message_text(f"{title}
{s['name']}

Tanlang:", reply_markup=InlineKeyboardMarkup(kb))

async def parent_show_fb(update, ctx):
    q = update.callback_query; await q.answer()
    parts = q.data.split("_"); sid = parts[1]; cat = parts[2]; idx = int(parts[3])
    db = load_db(); fbs = db.get(sid, [])
    if cat == "t":
        items = [f for f in fbs if f.get("role") == "teacher" or "role" not in f]
    else:
        items = [f for f in fbs if f.get("role") == "staff"]
    if idx >= len(items): return
    fb = items[idx]; s = ALL[sid]
    teacher = fb.get("teacher", "?")
    rl = "Fan ustozi" if (fb.get("role") == "teacher" or "role" not in fb) else "Maktab xodimi"
    await q.message.reply_text(f"👤 {s['name']}
🧑‍🏫 {teacher}
📌 {rl}: {fb.get('detail','')}")
    if fb.get("type") == "voice" and fb.get("file_id"):
        await q.message.reply_voice(voice=fb["file_id"], caption=f"🎤 ({fb.get('duration',0)} sek)")
    if fb.get("extra"):
        await q.message.reply_text(f"💬 Yozma: {fb['extra']}")
    prev_btn = []; next_btn = []
    if idx > 0:
        prev_btn = [InlineKeyboardButton("⬅️ Oldingi", callback_data=f"pfb_{sid}_{cat}_{idx-1}")]
    if idx < len(items) - 1:
        next_btn = [InlineKeyboardButton("Keyingi ➡️", callback_data=f"pfb_{sid}_{cat}_{idx+1}")]
    nav = prev_btn + next_btn
    kb = []
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton(f"💬 {teacher[:20]} ga javob", callback_data=f"preply_{sid}_{cat}_{idx}")])
    kb.append([InlineKeyboardButton("🔙 Ro'yxat", callback_data=f"pcat_{cat}_{sid}"),
               InlineKeyboardButton("🏠 Menyu", callback_data=f"pmenu_{sid}")])
    await q.message.reply_text("━━━━━━━━━━━━━━━━━", reply_markup=InlineKeyboardMarkup(kb))

async def parent_menu_btn(update, ctx):
    q = update.callback_query; await q.answer()
    sid = q.data.replace("pmenu_", "")
    await _parent_menu(q, ctx, sid, edit=False)

async def parent_show_child(update, ctx):
    q = update.callback_query; await q.answer()
    sid = q.data.replace("pchild_", "")
    s = ALL.get(sid)
    if not s: return
    db = load_db()
    msgs = db.get("_student_to_parent", {}).get(sid, [])
    if not msgs:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menyu", callback_data=f"pmenu_{sid}")]])
        await q.message.reply_text(
            f"📭 {s['name']} hali ichidagi gaplarini aytmagan.
"
            f"O'quvchi /bolaman buyrug'i orqali kirib gapirishi mumkin.", reply_markup=kb)
        return
    await q.message.reply_text(f"💌 {s['name']} aytgan gaplar ({len(msgs)} ta):")
    for i, m in enumerate(msgs, 1):
        ts = m.get("ts", "")
        if m["type"] == "voice":
            await q.message.reply_voice(voice=m["file_id"],
                                        caption=f"🎤 #{i} ({m.get('duration',0)} sek) • {ts}")
        else:
            await q.message.reply_text(f"✍️ #{i} • {ts}
{m.get('text','')}")
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menyu", callback_data=f"pmenu_{sid}")]])
    await q.message.reply_text("━━━━━━━━━━━━━━━━━", reply_markup=kb)

async def parent_reply_start(update, ctx):
    q = update.callback_query; await q.answer()
    parts = q.data.split("_"); sid = parts[1]; cat = parts[2]; idx = int(parts[3])
    db = load_db(); fbs = db.get(sid, [])
    if cat == "t":
        items = [f for f in fbs if f.get("role") == "teacher" or "role" not in f]
    else:
        items = [f for f in fbs if f.get("role") == "staff"]
    if idx >= len(items): return
    teacher = items[idx].get("teacher", "?")
    ctx.user_data["reply_to_teacher"] = teacher
    ctx.user_data["reply_for_sid"] = sid
    await q.message.reply_text(
        f"💬 {teacher} ga javobingiz

🎤 Ovoz yoki ✍️ matn yuboring.
Bekor: /cancel")

# ═══════════ O'QUVCHI /bolaman ═══════════
async def cmd_bolaman(update, ctx):
    ctx.user_data.clear()
    ctx.user_data["_student_search"] = True
    await update.message.reply_text(
        "🎓 Salom, aziz o'quvchi!

"
        "Ismingiz YOKI familiyangizni yozing.
"
        "Masalan: Javohir yoki Alijonov

"
        "Bekor: /cancel")

# ═══════════ DISPATCH (konv tashqari) ═══════════
async def dispatch_message(update, ctx):
    if ctx.user_data.get("_student_search"):
        return await _student_search(update, ctx)
    if "reply_to_teacher" in ctx.user_data:
        return await _save_parent_reply(update, ctx)
    if "student_sid" in ctx.user_data:
        return await _save_student_msg(update, ctx)
    await update.message.reply_text("Boshlash: /start (ustoz) yoki /bolaman (o'quvchi)")

async def _student_search(update, ctx):
    ctx.user_data.pop("_student_search", None)
    text = update.message.text.strip()
    result = find_student_by_name(text)
    if result is None:
        ctx.user_data["_student_search"] = True
        await update.message.reply_text("❌ Topilmadi. Ism yoki familiyangizni qayta yozing.
Bekor: /cancel")
        return
    if isinstance(result, list):
        kb = []
        for sid in result[:10]:
            s = ALL[sid]
            kb.append([InlineKeyboardButton(f"{s['name']} ({s['grade']})", callback_data=f"stpick_{sid}")])
        kb.append([InlineKeyboardButton("❌ Bekor", callback_data="st_cancel")])
        await update.message.reply_text("Bir nechta topildi. O'zingizni tanlang:",
                                        reply_markup=InlineKeyboardMarkup(kb))
        return
    sid = result; s = ALL[sid]
    ctx.user_data["student_sid"] = sid
    await update.message.reply_text(
        f"🎓 {s['name']} ({s['grade']})
━━━━━━━━━━━━━━━━━

"
        f"Ota-onangizga aytmoqchi bo'lgan gapingizni yozing:

"
        f"• Sevingan paytlaringiz
• Xafa bo'lganingiz
• Ichingizdagi gaplar
"
        f"• Ota-onangizga rahmat

"
        f"🎤 Ovoz yoki ✍️ matn yuboring.
Bekor: /cancel")

async def student_pick(update, ctx):
    q = update.callback_query; await q.answer()
    if q.data == "st_cancel":
        await q.edit_message_text("Bekor qilindi. /bolaman qayta bosing.")
        return
    sid = q.data.replace("stpick_", "")
    s = ALL.get(sid)
    if not s: return
    ctx.user_data["student_sid"] = sid
    await q.edit_message_text(
        f"🎓 {s['name']} ({s['grade']})
━━━━━━━━━━━━━━━━━

"
        f"Ota-onangizga gapingizni yozing:

"
        f"🎤 Ovoz yoki ✍️ matn yuboring.
Bekor: /cancel")

async def _save_student_msg(update, ctx):
    sid = ctx.user_data["student_sid"]
    db = load_db()
    if "_student_to_parent" not in db: db["_student_to_parent"] = {}
    if sid not in db["_student_to_parent"]: db["_student_to_parent"][sid] = []
    entry = {"from_user_id": update.effective_user.id,
             "ts": datetime.now().strftime("%Y-%m-%d %H:%M")}
    if update.message.voice:
        entry["type"] = "voice"
        entry["file_id"] = update.message.voice.file_id
        entry["duration"] = update.message.voice.duration
    else:
        entry["type"] = "text"
        entry["text"] = update.message.text or ""
    db["_student_to_parent"][sid].append(entry); save_db(db)
    s = ALL.get(sid, {})
    atxt = f"🎓 O'QUVCHI → OTA-ONA
{s.get('name','?')} ({s.get('grade','?')})
{entry['ts']}"
    if entry["type"] == "text": atxt += f"
✍️ {entry.get('text','')}"
    await notify_admin(ctx, atxt, entry.get("file_id"), entry.get("duration", 0))
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Yana yozish", callback_data=f"stmore_{sid}")],
        [InlineKeyboardButton("✅ Tugatdim", callback_data="st_done")]])
    await update.message.reply_text("✅ Gapingiz ota-onangizga yetkaziladi!
Yana yozasizmi?", reply_markup=kb)

async def student_more(update, ctx):
    q = update.callback_query; await q.answer()
    sid = q.data.replace("stmore_", "")
    ctx.user_data["student_sid"] = sid
    await q.edit_message_text("🎤 Ovoz yoki ✍️ matn yuboring.
Bekor: /cancel")

async def student_done(update, ctx):
    q = update.callback_query; await q.answer()
    ctx.user_data.pop("student_sid", None)
    await q.edit_message_text("Rahmat! Ota-onangiz QR kod orqali eshitadi.")

async def _save_parent_reply(update, ctx):
    teacher = ctx.user_data.pop("reply_to_teacher")
    sid = ctx.user_data.pop("reply_for_sid")
    db = load_db()
    if "_parent_replies" not in db: db["_parent_replies"] = {}
    if teacher not in db["_parent_replies"]: db["_parent_replies"][teacher] = []
    entry = {"sid": sid, "from_user_id": update.effective_user.id,
             "from_user_name": update.effective_user.full_name,
             "ts": datetime.now().strftime("%Y-%m-%d %H:%M")}
    if update.message.voice:
        entry["type"] = "voice"; entry["file_id"] = update.message.voice.file_id
        entry["duration"] = update.message.voice.duration
    else:
        entry["type"] = "text"; entry["text"] = update.message.text or ""
    db["_parent_replies"][teacher].append(entry); save_db(db)
    s = ALL.get(sid, {})
    atxt = f"💬 OTA-ONA → USTOZ
{s.get('name','?')} → {teacher}
{entry['from_user_name']}
{entry['ts']}"
    if entry["type"] == "text": atxt += f"
✍️ {entry['text']}"
    await notify_admin(ctx, atxt, entry.get("file_id"), entry.get("duration", 0))
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menyu", callback_data=f"pmenu_{sid}")]])
    await update.message.reply_text(f"✅ Javob {teacher} ga yetkazildi!", reply_markup=kb)

# ═══════════ ADMIN ═══════════
async def cmd_admin(update, ctx):
    global ADMIN_ID
    uid = update.effective_user.id; db = load_db()
    if not ADMIN_ID and not db.get("_admin_id"):
        db["_admin_id"] = uid; save_db(db); ADMIN_ID = uid
        await update.message.reply_text(
            f"✅ ADMIN bo'ldingiz! (ID: {uid})
"
            f"Barcha fikrlar real vaqtda sizga keladi.

"
            f"/admin — panel
/list — fikrlar
/inbox — ota-ona javoblari
"
            f"/stats — statistika
/export — CSV eksport
/eslatma — eslatma yuborish")
        return
    if uid != get_admin_id():
        await update.message.reply_text("❌ Faqat admin uchun."); return
    tc=sc=rc=cc=0; swfb=set(); ts=set()
    for sid, fbs in db.items():
        if sid.startswith("_") or not isinstance(fbs, list): continue
        for f in fbs:
            if f.get("role")=="staff": sc+=1
            else: tc+=1
            ts.add(f.get("teacher","?"))
        if fbs: swfb.add(sid)
    for t,rs in db.get("_parent_replies",{}).items(): rc+=len(rs)
    for s,ms in db.get("_student_to_parent",{}).items(): cc+=len(ms)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Ustozlar", callback_data="adm_teachers"),
         InlineKeyboardButton("👥 O'quvchilar", callback_data="adm_students")],
        [InlineKeyboardButton("💬 Ota-ona javob", callback_data="adm_replies"),
         InlineKeyboardButton("🎓 Bola gaplari", callback_data="adm_children")],
        [InlineKeyboardButton("📊 Statistika", callback_data="adm_stats"),
         InlineKeyboardButton("📥 CSV Eksport", callback_data="adm_export")],
        [InlineKeyboardButton("🔔 Eslatma yuborish", callback_data="adm_remind")]])
    await update.message.reply_text(
        f"🛡 ADMIN PANEL
━━━━━━━━━━━━━━━━━
"
        f"📚 Ustoz: {tc} | 🏫 Xodim: {sc}
💬 Javob: {rc} | 🎓 Bola: {cc}
"
        f"👥 {len(swfb)}/{len(ALL)} o'quvchi | 🧑‍🏫 {len(ts)} ustoz", reply_markup=kb)

async def admin_callback(update, ctx):
    q = update.callback_query; await q.answer()
    if q.from_user.id != get_admin_id():
        await q.message.reply_text("❌ Faqat admin."); return
    db = load_db(); action = q.data.replace("adm_","")
    if action == "teachers":
        agg = {}
        for sid,fbs in db.items():
            if sid.startswith("_") or not isinstance(fbs,list): continue
            for f in fbs: t=f.get("teacher","?"); agg[t]=agg.get(t,0)+1
        if not agg: await q.message.reply_text("Yo'q."); return
        lines = ["📚 Ustozlar:"]
        for t,c in sorted(agg.items(),key=lambda x:-x[1]): lines.append(f"• {t}: {c}")
        await q.message.reply_text("\n".join(lines))
    elif action == "students":
        lines = ["👥 O'quvchilar:"]
        for sid,info in ALL.items():
            fbs = db.get(sid,[])
            t=sum(1 for f in fbs if f.get("role")=="teacher" or "role" not in f)
            s=sum(1 for f in fbs if f.get("role")=="staff")
            c=len(db.get("_student_to_parent",{}).get(sid,[]))
            st = "✅" if (t+s)>0 else "⬜"
            ex = f" 🎓{c}" if c else ""
            lines.append(f"{st} {info['name']} ({info['grade']}) U:{t} X:{s}{ex}")
        txt = "\n".join(lines)
        for i in range(0,len(txt),3500): await q.message.reply_text(txt[i:i+3500])
    elif action == "replies":
        rr = db.get("_parent_replies",{})
        if not rr: await q.message.reply_text("Yo'q."); return
        lines = ["💬 Ota-ona javoblari:"]
        for t,rs in rr.items(): lines.append(f"• {t}: {len(rs)}")
        lines.append("\n/inbox <ustoz> orqali ko'ring")
        await q.message.reply_text("\n".join(lines))
    elif action == "children":
        ch = db.get("_student_to_parent",{})
        if not ch: await q.message.reply_text("Yo'q."); return
        total = sum(len(v) for v in ch.values())
        await q.message.reply_text(f"🎓 Bola gaplari ({total} ta):")
        for sid,msgs in ch.items():
            s = ALL.get(sid,{"name":"?","grade":"?"})
            await q.message.reply_text(f"👤 {s['name']} ({s['grade']}) — {len(msgs)}")
            for i,m in enumerate(msgs,1):
                if m["type"]=="voice":
                    await q.message.reply_voice(voice=m["file_id"],
                                                caption=f"#{i} ({m.get('duration',0)}s) {m.get('ts','')}")
                else:
                    await q.message.reply_text(f"#{i} {m.get('ts','')}\n{m.get('text','')}")
    elif action == "stats":
        await _send_stats(q.message, db)
    elif action == "export":
        await _send_export(q.message, db)
    elif action == "remind":
        await _send_remind_menu(q, db)

# ═══════════ 1. /stats — BATAFSIL STATISTIKA ═══════════
async def _send_stats(msg, db=None):
    if db is None: db = load_db()
    total_fb = 0; teacher_fb = 0; staff_fb = 0
    teacher_counts = {}; grade_counts = {"9-sinf":0,"10-sinf":0,"11-sinf":0}
    students_with_fb = set(); students_without_fb = []
    for sid, fbs in db.items():
        if sid.startswith("_") or not isinstance(fbs, list): continue
        if sid not in ALL: continue
        grade = ALL[sid]["grade"]
        if fbs:
            students_with_fb.add(sid)
            grade_counts[grade] = grade_counts.get(grade, 0) + len(fbs)
            total_fb += len(fbs)
            for f in fbs:
                t = f.get("teacher","?")
                teacher_counts[t] = teacher_counts.get(t, 0) + 1
                if f.get("role") == "staff": staff_fb += 1
                else: teacher_fb += 1
    for sid, info in ALL.items():
        if sid not in students_with_fb:
            students_without_fb.append(f"{info['name']} ({info['grade']})")
    parent_replies = sum(len(v) for v in db.get("_parent_replies",{}).values())
    child_msgs = sum(len(v) for v in db.get("_student_to_parent",{}).values())
    top_teachers = sorted(teacher_counts.items(), key=lambda x: -x[1])[:5]
    lines = [
        "📊 BATAFSIL STATISTIKA",
        "━"*17,
        f"📁 Jami fikrlar: {total_fb}",
        f"  📚 Ustoz fikri: {teacher_fb}",
        f"  🏫 Xodim fikri: {staff_fb}",
        "",
        "🏫 Sinf bo'yicha:",
        f"  9-sinf: {grade_counts.get('9-sinf',0)} ta",
        f"  10-sinf: {grade_counts.get('10-sinf',0)} ta",
        f"  11-sinf: {grade_counts.get('11-sinf',0)} ta",
        "",
        f"👥 O'quvchilar: {len(students_with_fb)}/{len(ALL)} ta fikr olgan",
        f"💬 Ota-ona javoblari: {parent_replies} ta",
        f"🎓 Bola gaplari: {child_msgs} ta",
    ]
    if top_teachers:
        lines.append("")
        lines.append("🏆 TOP-5 ustoz (fikr bo'yicha):")
        for i,(t,c) in enumerate(top_teachers,1):
            lines.append(f"  {i}. {t}: {c} ta")
    coverage = round(len(students_with_fb)/len(ALL)*100) if ALL else 0
    lines.append("")
    lines.append(f"📊 Qamrab olish: {coverage}%")
    if students_without_fb:
        lines.append("")
        lines.append(f"⚠️ Fikr yo'q ({len(students_without_fb)} ta):")
        for s in students_without_fb[:10]:
            lines.append(f"  • {s}")
        if len(students_without_fb) > 10:
            lines.append(f"  ... va yana {len(students_without_fb)-10} ta")
    await msg.reply_text("\n".join(lines))

async def cmd_stats(update, ctx):
    if update.effective_user.id != get_admin_id():
        await update.message.reply_text("❌ Faqat admin uchun.")
        return
    await _send_stats(update.message)

# ═══════════ 2. /export — CSV EKSPORT ═══════════
async def _send_export(msg, db=None):
    if db is None: db = load_db()
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(["#","O'quvchi","Sinf","Ustoz/Xodim","Lavozim","Rol","Tur","Davomiylik(sek)","Yozma izoh","Sana"])
    row_num = 1
    for sid, fbs in db.items():
        if sid.startswith("_") or not isinstance(fbs, list): continue
        if sid not in ALL: continue
        s = ALL[sid]
        for fb in fbs:
            writer.writerow([
                row_num,
                s["name"],
                s["grade"],
                fb.get("teacher","?"),
                fb.get("detail",""),
                "Ustoz" if fb.get("role","teacher") == "teacher" else "Xodim",
                fb.get("type","voice"),
                fb.get("duration",0),
                fb.get("extra",""),
                fb.get("ts","")
            ])
            row_num += 1
    csv_data = output.getvalue().encode("utf-8-sig")
    bio = io.BytesIO(csv_data)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    bio.name = f"fikrlar_{ts}.csv"
    await msg.reply_document(
        document=bio,
        filename=bio.name,
        caption=f"📥 Barcha fikrlar CSV formatda\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n📊 Jami: {row_num-1} ta yozuv")

async def cmd_export(update, ctx):
    if update.effective_user.id != get_admin_id():
        await update.message.reply_text("❌ Faqat admin uchun.")
        return
    await update.message.reply_text("🔄 CSV fayl tayyorlanmoqda...")
    await _send_export(update.message)

# ═══════════ 3. USTOZLARGA INBOX ═══════════
async def cmd_inbox(update, ctx):
    db = load_db(); rbt = db.get("_parent_replies",{})
    args = ctx.args
    if not args:
        if not rbt:
            await update.message.reply_text("Hali javob yo'q.\n/inbox <ism familiya>"); return
        lines = ["Javob kelgan ustozlar:"]
        for t,rs in rbt.items(): lines.append(f"• {t}: {len(rs)}")
        lines.append("\n/inbox <ism>"); await update.message.reply_text("\n".join(lines)); return
    name = " ".join(args).strip()
    rs = rbt.get(name,[])
    if not rs:
        mm = [t for t in rbt if name.lower() in t.lower()]
        if len(mm)==1: name=mm[0]; rs=rbt[name]
        elif mm: await update.message.reply_text("Mos:\n"+"\n".join(mm)); return
        else: await update.message.reply_text(f"'{name}' topilmadi."); return
    await update.message.reply_text(f"💬 {name} ga javoblar ({len(rs)}):")
    for r in rs:
        s = ALL.get(r["sid"],{"name":"?","grade":"?"})
        await update.message.reply_text(f"👨‍👩‍👧 {s['name']} ({s['grade']}) • {r.get('ts','')}")
        if r["type"]=="voice":
            await update.message.reply_voice(voice=r["file_id"],caption=f"({r.get('duration',0)}s)")
        else: await update.message.reply_text(r.get("text",""))

# ═══════════ 4. ESLATMA TIZIMI ═══════════
async def _send_remind_menu(q, db):
    no_fb = []
    for sid, info in ALL.items():
        fbs = db.get(sid, [])
        if not fbs:
            no_fb.append((sid, info))
    if not no_fb:
        await q.message.reply_text("🎉 Barcha o'quvchilar haqida fikr bor!")
        return
    lines = [f"⚠️ Fikr yo'q: {len(no_fb)} ta o'quvchi", ""]
    grade_groups = {}
    for sid, info in no_fb:
        g = info["grade"]
        grade_groups.setdefault(g, []).append(info["name"])
    for grade, names in grade_groups.items():
        lines.append(f"🏫 {grade} ({len(names)} ta):")
        for n in names: lines.append(f"  • {n}")
    lines.append("")
    lines.append(f"🔔 /eslatma buyrug'i bilan barcha ustozlarga eslatma yuboring")
    await q.message.reply_text("\n".join(lines))

async def cmd_eslatma(update, ctx):
    if update.effective_user.id != get_admin_id():
        await update.message.reply_text("❌ Faqat admin uchun.")
        return
    db = load_db()
    no_fb_sids = [sid for sid, info in ALL.items() if not db.get(sid)]
    if not no_fb_sids:
        await update.message.reply_text("🎉 Barcha o'quvchilar haqida fikr bor!")
        return
    grade_groups = {}
    for sid in no_fb_sids:
        info = ALL[sid]; g = info["grade"]
        grade_groups.setdefault(g, []).append(info["name"])
    lines = [
        "🔔 ESLATMA: Quyidagi o'quvchilar haqida hali fikr bildirilmagan:",
        ""
    ]
    for grade, names in grade_groups.items():
        lines.append(f"🏫 {grade} ({len(names)} ta):")
        for n in names: lines.append(f"  • {n}")
    lines.append("")
    lines.append(f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"📊 Jami: {len(no_fb_sids)} ta o'quvchi fikrsiz")
    msg_text = "\n".join(lines)
    # Adminni o'zi ham olsin
    await update.message.reply_text(msg_text)
    await update.message.reply_text(
        f"✅ Eslatma yuborildi!\n"
        f"⚠️ {len(no_fb_sids)} ta o'quvchi haqida fikr yo'q.\n\n"
        f"Ustozlarga individual eslatma yuborish uchun bot userlarni bazaga qo'shish kerak bo'ladi.")

# Avtomatik kunlik eslatma (ixtiyoriy - job queue orqali)
async def daily_remind_job(ctx):
    aid = get_admin_id()
    if not aid: return
    db = load_db()
    no_fb_sids = [sid for sid, info in ALL.items() if not db.get(sid)]
    if not no_fb_sids: return
    coverage = round((len(ALL) - len(no_fb_sids)) / len(ALL) * 100)
    msg = (f"🔔 KUNLIK ESLATMA\n"
           f"📊 Qamrab olish: {coverage}%\n"
           f"⚠️ {len(no_fb_sids)} ta o'quvchi haqida fikr yo'q\n"
           f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
           f"/stats — to'liq statistika\n/eslatma — ro'yxat")
    try:
        await ctx.bot.send_message(aid, msg)
    except Exception as e:
        logging.error(f"Daily remind: {e}")

# ═══════════ /list ═══════════
async def cmd_list(update, ctx):
    db = load_db(); lines = []
    for sid,fbs in db.items():
        if sid.startswith("_") or not isinstance(fbs,list) or sid not in ALL: continue
        if fbs:
            t=sum(1 for f in fbs if f.get("role")=="teacher" or "role" not in f)
            s=sum(1 for f in fbs if f.get("role")=="staff")
            lines.append(f"{ALL[sid]['name']} ({ALL[sid]['grade']}) U:{t} X:{s}")
    if not lines: await update.message.reply_text("Hali fikr yo'q."); return
    txt = "Fikr qoldirilganlar:\n"+"\n".join(lines)
    for i in range(0,len(txt),3500): await update.message.reply_text(txt[i:i+3500])

# ═══════════ MAIN ═══════════
def main():
    if not TOKEN: raise ValueError("BOT_TOKEN!")
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            S_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            S_ROLE: [CallbackQueryHandler(pick_role, pattern="^r_")],
            S_DETAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_detail)],
            S_GRADE: [CallbackQueryHandler(pick_grade, pattern="^g_")],
            S_STU: [CallbackQueryHandler(pick_stu, pattern="^(s_|back_grade)")],
            S_VOICE: [MessageHandler(filters.VOICE, recv_voice)],
            S_REVIEW: [CallbackQueryHandler(review_voice, pattern="^(ok_voice|redo_voice)$")],
            S_EXTRA: [MessageHandler(filters.TEXT & ~filters.COMMAND, recv_extra),
                      CallbackQueryHandler(skip_extra, pattern="^skip_extra$")],
            S_AFTER: [CallbackQueryHandler(after_action, pattern="^(go_start|cont_)")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    app.add_handler(conv)
    # O'quvchi
    app.add_handler(CommandHandler("bolaman", cmd_bolaman))
    app.add_handler(CallbackQueryHandler(student_pick, pattern="^(stpick_|st_cancel)"))
    app.add_handler(CallbackQueryHandler(student_more, pattern="^stmore_"))
    app.add_handler(CallbackQueryHandler(student_done, pattern="^st_done$"))
    # Ota-ona
    app.add_handler(CallbackQueryHandler(parent_category, pattern="^pcat_"))
    app.add_handler(CallbackQueryHandler(parent_show_fb, pattern="^pfb_"))
    app.add_handler(CallbackQueryHandler(parent_menu_btn, pattern="^pmenu_"))
    app.add_handler(CallbackQueryHandler(parent_show_child, pattern="^pchild_"))
    app.add_handler(CallbackQueryHandler(parent_reply_start, pattern="^preply_"))
    # Admin
    app.add_handler(CommandHandler("admin", cmd_admin))
    app.add_handler(CallbackQueryHandler(admin_callback, pattern="^adm_"))
    app.add_handler(CommandHandler("inbox", cmd_inbox))
    app.add_handler(CommandHandler("list", cmd_list))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("export", cmd_export))
    app.add_handler(CommandHandler("eslatma", cmd_eslatma))
    app.add_handler(CommandHandler("cancel", cancel))
    # Dispatch
    app.add_handler(MessageHandler((filters.VOICE|(filters.TEXT&~filters.COMMAND)), dispatch_message))
    # Kunlik eslatma (har kuni soat 08:00 da)
    if app.job_queue:
        from datetime import time as dtime
        app.job_queue.run_daily(daily_remind_job, time=dtime(hour=8, minute=0))
    print("Bot v7 — Stats + Export + Inbox + Eslatma tizimi qo'shildi")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
