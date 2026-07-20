from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot  
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from quiz import QUESTIONS

router = Router()

# автор

def get_author_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text = 'Мой Telegram', url = 't.me/Noneqwer2')],
            [InlineKeyboardButton(text = 'Мой TikTok', url = 'https://vt.tiktok.com/ZSX6XjDdh/')],
            [InlineKeyboardButton(text = 'Мой GitHub', url = 'https://github.com/volkovssivan-max')],
            [InlineKeyboardButton(text = 'Более подробная информация обо мне', callback_data='info_more')]
        ]
    )
    return keyboard

# start_quiz

class QuizStates(StatesGroup):
    answering = State()
def get_options_keyboard(options: list) -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text=opt)] for opt in options]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


@router.message(Command('start_quiz'))
async def get_start_quiz(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(current_question=0, score=0)
    await message.answer(" Давай начнем викторину!")
    await send_question(message, state)
    
@router.message(Command('cancel'))
async def cancel_quiz(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        await message.answer("Вы сейчас не проходите викторину.")
        return
        
    await state.clear()
    await message.answer("Викторина прервана. Результаты сброшены.", reply_markup=ReplyKeyboardRemove())


async def send_question(message: Message, state: FSMContext):
    data = await state.get_data()
    q_index = data["current_question"]
    
    
    if q_index < len(QUESTIONS):
        question = QUESTIONS[q_index]
        kb = get_options_keyboard(question["options"])
        await state.set_state(QuizStates.answering)
        await message.answer(f"Вопрос {q_index + 1}: {question['text']}", reply_markup=kb)
    else:
        score = data["score"]
        await message.answer(
            f"🎉 Викторина окончена!\nВы набрали: {score} из {len(QUESTIONS)} баллов.",
            reply_markup = ReplyKeyboardRemove()
        )
        await state.clear()

@router.message(QuizStates.answering, ~F.text.startwith('/'))
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    q_index = data["current_question"]
    score = data["score"]
    
    current_question = QUESTIONS[q_index]
    user_answer = message.text

    if user_answer == current_question["correct"]:
        score += 1
        await message.answer("Правильно!")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {current_question['correct']}")

    await state.update_data(current_question=q_index + 1, score=score)
    await send_question(message, state)


# Основные функции

@router.callback_query(F.data == 'info_more')
async def process(callback: CallbackQuery):
    await callback.message.answer(
                                  'Я - Soda, начинающий программист на языке Python.'
                                  'Сейчас я активно учусь библиотке \'aiogram\'. Это мой первый полноценный проект с использование данной библиотке. '
                                  'Надеюсь вам понравиться😘'
                                  )
    await callback.answer()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        'Привет😊! Это простая викторина по книгам серии <b>"Всё ради игры"</b>.\n\n'
        'В викторине будут представлены <i>10 вопросов</i> каждый с <i>4 вариантами ответа</i>. '
        'Правильный ответ только <u>один!</u>\n\n'
        'Нажми /help для вызова всех команд.\nЖелаю удачи❤️',
        parse_mode='HTML'
    )
    
    
@router.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Основные команды бота\n\n'
        '<i><b>/start</b></i> - начинает бота\n'
        '<i><b>/help</b></i> - вызывает команду помощи\n'
        '<i><b>/start_quiz</b></i> - начинает тест\n'
        '<i><b>/cancel</b></i> - выходит из теста\n'
        '<i><b>/author</b></i> - показывает кто автора этого шедевра😎\n',
        parse_mode = 'HTML'
        )

    
@router.message(Command('author'))
async def author(message: Message):
    await message.answer('Мои соц-сети и инфорация обо мне',
                         reply_markup = get_author_keyboard()
                         )

# Неизвестные команды

@router.message()
async def some(message: Message):
    await message.answer('Я не знаю эту команду😢')
