import asyncio
import logging
import os
import json
import random
import string
from datetime import datetime, date
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice, PreCheckoutQuery, Message
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8544087301:AAG5zpzLBbuuLm3khbg4c6_GZcqBgSFFy10")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7693087447"))
WEB_URL = os.getenv("WEB_URL", "https://your-app.railway.app")
STARS_PRICE = int(os.getenv("STARS_PRICE", "0"))  # 50 Telegram Stars

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

DB_FILE = "data/users.json"
DOCS_FILE = "data/documents.json"

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_pin():
    return str(random.randint(1000, 9999))

def generate_doc_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

# ─── States ───────────────────────────────────────────────────────────────────
class Form(StatesGroup):
    fish = State()
    jinsi = State()
    jshshr = State()
    yoshi = State()
    yashash = State()
    ish_joyi = State()
    tashxis = State()
    shifokor = State()
    boshlik = State()
    boshlanish = State()
    tugash = State()
    muassasa = State()

# ─── /start ───────────────────────────────────────────────────────────────────
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    users = load_json(DB_FILE)
    uid = str(message.from_user.id)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Hujjat yaratish", callback_data="create_doc")],
        [InlineKeyboardButton(text="⭐ Obuna sotib olish", callback_data="buy_sub")],
        [InlineKeyboardButton(text="📁 Mening hujjatlarim", callback_data="my_docs")],
    ])

    has_sub = users.get(uid, {}).get("subscribed", False)
    sub_text = "✅ Obunangiz faol" if has_sub else "❌ Obuna yo'q"

    await message.answer(
        f"👋 *DMED Documents Botiga xush kelibsiz!*\n\n"
        f"Bu bot sizga mehnatga layoqatsizlik ma'lumotnomasi yaratishga yordam beradi.\n\n"
        f"💳 Holat: {sub_text}\n"
        f"💰 Narx: {STARS_PRICE} ⭐ Stars\n\n"
        f"Hujjat yaratish uchun avval obuna sotib oling.",
        parse_mode="Markdown",
        reply_markup=kb
    )

# ─── Buy subscription ─────────────────────────────────────────────────────────
@dp.callback_query(F.data == "buy_sub")
async def buy_subscription(callback: types.CallbackQuery):
    users = load_json(DB_FILE)
    uid = str(callback.from_user.id)
    if users.get(uid, {}).get("subscribed"):
        await callback.answer("✅ Sizda allaqachon faol obuna bor!", show_alert=True)
        return

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="🏥 DMED Hujjat Generatori",
        description=f"1 ta mehnatga layoqatsizlik ma'lumotnomasi yaratish huquqi. {STARS_PRICE} Telegram Stars.",
        payload="doc_subscription",
        currency="XTR",
        prices=[LabeledPrice(label="Obuna", amount=STARS_PRICE)],
        protect_content=False,
    )
    await callback.answer()

@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    users = load_json(DB_FILE)
    uid = str(message.from_user.id)
    if uid not in users:
        users[uid] = {}
    users[uid]["subscribed"] = True
    users[uid]["paid_at"] = datetime.now().isoformat()
    users[uid]["name"] = message.from_user.full_name
    save_json(DB_FILE, users)

    await message.answer(
        "✅ *To'lov qabul qilindi!*\n\n"
        "Endi hujjat yaratishingiz mumkin.\n"
        "Quyidagi tugmani bosing 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Hujjat yaratish", callback_data="create_doc")]
        ])
    )

# ─── Create document ──────────────────────────────────────────────────────────
@dp.callback_query(F.data == "create_doc")
async def create_doc(callback: types.CallbackQuery, state: FSMContext):
    users = load_json(DB_FILE)
    uid = str(callback.from_user.id)

    if not users.get(uid, {}).get("subscribed"):
        await callback.answer("❌ Avval obuna sotib oling!", show_alert=True)
        return

    await state.set_state(Form.fish)
    await callback.message.answer(
        "📝 *Hujjat ma'lumotlarini kiriting*\n\n"
        "1️⃣ Bemorning *FISh* (To'liq ism)ni kiriting:\n"
        "_(Misol: KARIMOV SHERALI ZOKIRJON O'G'LI)_",
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.message(Form.fish)
async def form_fish(message: Message, state: FSMContext):
    await state.update_data(fish=message.text.upper())
    await state.set_state(Form.jinsi)
    await message.answer(
        "2️⃣ *Jinsi:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="👨 Erkak", callback_data="gender_erkak"),
                InlineKeyboardButton(text="👩 Ayol", callback_data="gender_ayol"),
            ]
        ])
    )

@dp.callback_query(F.data.startswith("gender_"))
async def form_gender(callback: types.CallbackQuery, state: FSMContext):
    gender = "erkak" if callback.data == "gender_erkak" else "ayol"
    await state.update_data(jinsi=gender)
    await state.set_state(Form.jshshr)
    await callback.message.answer(
        "3️⃣ *JShShIR* (14 raqamli shaxsiy raqam):\n"
        "_(Misol: 50203056600029)_",
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.message(Form.jshshr)
async def form_jshshr(message: Message, state: FSMContext):
    jshshr = message.text.strip()
    if not jshshr.isdigit() or len(jshshr) != 14:
        await message.answer("❌ JShShIR 14 ta raqamdan iborat bo'lishi kerak. Qayta kiriting:")
        return
    await state.update_data(jshshr=jshshr)
    await state.set_state(Form.yoshi)
    await message.answer(
        "4️⃣ *Yoshi* (raqamda):\n_(Misol: 20)_",
        parse_mode="Markdown"
    )

@dp.message(Form.yoshi)
async def form_yoshi(message: Message, state: FSMContext):
    yoshi = message.text.strip()
    if not yoshi.isdigit():
        await message.answer("❌ Yoshni raqamda kiriting. Misol: 20")
        return
    await state.update_data(yoshi=yoshi)
    await state.set_state(Form.yashash)
    await message.answer(
        "5️⃣ *Yashash manzili:*\n_(Misol: Toshkent sh., Yunusobod t., 5-uy)_",
        parse_mode="Markdown"
    )

@dp.message(Form.yashash)
async def form_yashash(message: Message, state: FSMContext):
    await state.update_data(yashash=message.text)
    await state.set_state(Form.ish_joyi)
    await message.answer(
        "6️⃣ *Ish/o'qish joyi:*\n_(Misol: TDIU yoki Yoʻq)_",
        parse_mode="Markdown"
    )

@dp.message(Form.ish_joyi)
async def form_ish(message: Message, state: FSMContext):
    await state.update_data(ish_joyi=message.text)
    await state.set_state(Form.tashxis)
    await message.answer(
        "7️⃣ *Tashxis (KXT-10 kodi va nomi):*\n"
        "_(Misol: J22: Quyi nafas yo'llarining aniqlangan o'tkir respirator infeksiyasi)_",
        parse_mode="Markdown"
    )

@dp.message(Form.tashxis)
async def form_tashxis(message: Message, state: FSMContext):
    await state.update_data(tashxis=message.text)
    await state.set_state(Form.shifokor)
    await message.answer(
        "8️⃣ *Davolovchi shifokor FISh:*\n_(Misol: AMONOVA D.R.)_",
        parse_mode="Markdown"
    )

@dp.message(Form.shifokor)
async def form_shifokor(message: Message, state: FSMContext):
    await state.update_data(shifokor=message.text.upper())
    await state.set_state(Form.boshlik)
    await message.answer(
        "9️⃣ *Bo'lim boshlig'i FISh:*\n_(Misol: HASANOVA SH.A.)_",
        parse_mode="Markdown"
    )

@dp.message(Form.boshlik)
async def form_boshlik(message: Message, state: FSMContext):
    await state.update_data(boshlik=message.text.upper())
    await state.set_state(Form.boshlanish)
    await message.answer(
        "🔟 *Ishdan ozod boshlanish sanasi:*\n_(Misol: 23.02.2026)_",
        parse_mode="Markdown"
    )

@dp.message(Form.boshlanish)
async def form_boshlanish(message: Message, state: FSMContext):
    await state.update_data(boshlanish=message.text.strip())
    await state.set_state(Form.tugash)
    await message.answer(
        "1️⃣1️⃣ *Ishdan ozod tugash sanasi:*\n_(Misol: 25.02.2026)_",
        parse_mode="Markdown"
    )

@dp.message(Form.tugash)
async def form_tugash(message: Message, state: FSMContext):
    await state.update_data(tugash=message.text.strip())
    await state.set_state(Form.muassasa)
    await message.answer(
        "1️⃣2️⃣ *Hujjat berilgan muassasa:*\n_(Misol: Oliygoh yoki 34-sonli oilaviy poliklinika)_",
        parse_mode="Markdown"
    )

@dp.message(Form.muassasa)
async def form_muassasa(message: Message, state: FSMContext):
    await state.update_data(muassasa=message.text)
    data = await state.get_data()
    await state.clear()

    # Generate doc
    doc_id = generate_doc_id()
    pin = generate_pin()
    today = datetime.now().strftime("%d.%m.%Y")
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    doc_number = "01TSH " + ''.join(random.choices(string.digits, k=9))

    document = {
        "doc_id": doc_id,
        "pin": pin,
        "created_at": now,
        "user_id": str(message.from_user.id),
        "data": {
            "fish": data["fish"],
            "jinsi": data["jinsi"],
            "jshshr": data["jshshr"],
            "yoshi": data["yoshi"],
            "yashash": data["yashash"],
            "ish_joyi": data["ish_joyi"],
            "tashxis": data["tashxis"],
            "shifokor": data["shifokor"],
            "boshlik": data["boshlik"],
            "boshlanish": data["boshlanish"],
            "tugash": data["tugash"],
            "muassasa": data["muassasa"],
            "sana": today,
            "doc_number": doc_number,
        }
    }

    docs = load_json(DOCS_FILE)
    docs[doc_id] = document
    save_json(DOCS_FILE, docs)

    # Remove subscription (1 use)
    users = load_json(DB_FILE)
    uid = str(message.from_user.id)
    users[uid]["subscribed"] = False
    save_json(DB_FILE, users)

    doc_url = f"{WEB_URL}/doc/{doc_id}"

    await message.answer(
        f"✅ *Hujjat muvaffaqiyatli yaratildi!*\n\n"
        f"🔗 Havola: `{doc_url}`\n\n"
        f"🔐 *PIN kod: `{pin}`*\n\n"
        f"📱 QR kodni skanerlang yoki havolaga kiring, PIN kodni kiriting — hujjat ochiladi.\n\n"
        f"⚠️ PIN kodni hech kimga bermang!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Hujjatni ochish", url=doc_url)],
            [InlineKeyboardButton(text="⭐ Yana hujjat yaratish", callback_data="buy_sub")],
        ])
    )

# ─── My documents ─────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "my_docs")
async def my_docs(callback: types.CallbackQuery):
    docs = load_json(DOCS_FILE)
    uid = str(callback.from_user.id)
    user_docs = [(k, v) for k, v in docs.items() if v.get("user_id") == uid]

    if not user_docs:
        await callback.answer("📭 Hujjatlaringiz topilmadi.", show_alert=True)
        return

    text = "📁 *Sizning hujjatlaringiz:*\n\n"
    buttons = []
    for doc_id, doc in user_docs[-5:]:
        d = doc["data"]
        text += f"👤 {d['fish']}\n📅 {doc['created_at']}\n🔗 `{WEB_URL}/doc/{doc_id}`\n🔐 PIN: `{doc['pin']}`\n\n"
        buttons.append([InlineKeyboardButton(
            text=f"📄 {d['fish'][:20]}...",
            url=f"{WEB_URL}/doc/{doc_id}"
        )])

    await callback.message.answer(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await callback.answer()

# ─── Admin stats ──────────────────────────────────────────────────────────────
@dp.message(Command("stats"))
async def admin_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    users = load_json(DB_FILE)
    docs = load_json(DOCS_FILE)
    await message.answer(
        f"📊 *Admin statistika:*\n\n"
        f"👥 Jami foydalanuvchilar: {len(users)}\n"
        f"📄 Jami hujjatlar: {len(docs)}\n"
        f"✅ Faol obunalar: {sum(1 for u in users.values() if u.get('subscribed'))}",
        parse_mode="Markdown"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
