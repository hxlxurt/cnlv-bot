from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from pypinyin import pinyin, Style


router = Router()
import keyboards
from dictionary import d

class Translation(StatesGroup):
    active = State()
    cancel = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
    f"👋 Laipni lūdzam, {message.from_user.first_name}!\n\n"
    "📚 Es pārvēršu ķīniešu tekstu (hieroglifus vai pinyin) latviešu transkripcijā.\n\n"
    "✍️ Kā lietot:\n"
    "— Ievadi ķīniešu hieroglifus vai pinyin\n"
    "— Pinyin jāieraksta ar atstarpēm: qing wen - cjiņ veņ\n\n"
    "🔹 Piemēri:\n"
    "你好 → ņi hao\n"
    "qing wen → cjin veņ\n\n"
    "📌 Komandas:\n"
    "/translate — teksta tulkošanas režīms\n"
    "/cancel — iziet no tulkošanas režīma\n"
    "/help — palīdzība un piemēri\n\n"
    "🚀 Nospied /translate un nosūti tekstu tulkošanai!\n\n"
    "🆕 Atjauninājums v2.0:\n"
    "— Pievienots hieroglifu atbalsts\n"
    "— Uzlabota tulkošanas loģika\n"
    "— Uzlabots UX interfeiss (pogas un navigācija)",
    reply_markup=keyboards.main
)


@router.message(Command('help'))
async def cmd_help(message:Message):
    await message.answer('Šeit ir atbildes uz jautājumiem par bota darbības principiem',
                         reply_markup=keyboards.main)

@router.message(Command('translate'))
async def cmd_translate(message:Message, state: FSMContext):
    await state.set_state(Translation.active)
    await message.answer('Nosūtiet tekstu tulkošanai:', reply_markup=keyboards.back)

@router.message(Command('cancel'))
async def cmd_cancel(message:Message, state: FSMContext):
    await state.clear()
    await message.answer('❌ Tulkošanas režīms ir izslēgts', reply_markup=keyboards.back)


@router.callback_query(F.data == 'back')
async def cmd_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.answer('Jūs atgriezāties galvenajā izvēlnē', reply_markup=keyboards.main)

@router.callback_query(F.data == 'botinfo')
async def cmd_botinfo(callback: CallbackQuery):
    await callback.answer('Jūs izvēlējāties informāciju par botu')
    await callback.message.answer(
    '📘 Kā darbojas bots\n'
    'Ievadiet ķīniešu hieroglifus vai piņjiņs (ar atstarpēm: qing wen - cjiņ veņ),\n'
    'un bots pārvērš tos latviešu transkripcijā.\n\n'

    '📚 Bots darbojas, balstoties uz vārdnīcu «Lielā ķīniešu–latviešu vārdnīca» (Pēteris Pildegovičs).',
    reply_markup=keyboards.back
)


@router.callback_query(F.data == 'botexample')
async def cmd_botexample(callback: CallbackQuery):
    await callback.answer('Jūs izvēlējāties bota darbības piemēru')
    await callback.message.answer(
    '🔹 Piemērs:\n'
    'Ievade: 你好 → Rezultāts: ņi hao\n'
    'Ievade: qing wen → Rezultāts: cjin veņ\n\n',
    reply_markup=keyboards.back
)
    
@router.callback_query(F.data == 'to_translate')
async def cmd_startbot(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Translation.active)
    await callback.answer('Jūs sākāt teksta tulkošanas režīmu')
    await callback.message.answer('Ievadiet tekstu tulkošanai:', reply_markup=keyboards.back)


def has_chinese(text: str) -> bool:
    return any('\u4e00' <= c <= '\u9fff' for c in text)


def normalize_text(text: str):
    if has_chinese(text):
        return [item[0] for item in pinyin(text, style=Style.NORMAL)]
    else:
        return text.split()


@router.message(Translation.active)
async def cmd_processtranslation(message: Message):

    words = normalize_text(message.text)

    result = []

    for word in words:
        translated = d.get(word)

        if translated is None:
            translated = word

        result.append(translated)

    final_text = ' '.join(result)

    await message.answer(final_text)
