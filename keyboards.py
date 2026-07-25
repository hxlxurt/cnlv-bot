from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ℹ️ Informācija par botu', callback_data='botinfo')],
    [InlineKeyboardButton(text='📖 Piemērs', callback_data='botexample')],
    [InlineKeyboardButton(text='🚀 Sākt darbu!', callback_data='to_translate')]
])

help = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ℹ️ Informācija par botu', callback_data='botinfo')],
    [InlineKeyboardButton(text='📖 Piemērs', callback_data='botexample')],
    [InlineKeyboardButton(text='⬅️ Atpakaļ', callback_data='back')]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Atpakaļ', callback_data='back')]
])