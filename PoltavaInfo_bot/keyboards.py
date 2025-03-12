from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder




main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🌦 Погода', callback_data='pogoda'),
     InlineKeyboardButton(text='☢ Радіаційний фон', callback_data='radioc')],
    [InlineKeyboardButton(text='🌬 Стан повітря', callback_data='povit'),
     InlineKeyboardButton(text='🏭 Сектори економіки', callback_data='sect')],
    [InlineKeyboardButton(text='🌿 Заповідники', callback_data='zapov'),
     InlineKeyboardButton(text='🏛 Історичні пам`ятки', callback_data='pamat')]
])

sector = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🌾 Первинний', callback_data='perv'),
     InlineKeyboardButton(text='🏗 Вторинний', callback_data='vtor')],
    [InlineKeyboardButton(text='📊 Третинний', callback_data='tret'),
     InlineKeyboardButton(text='🔙 Назад', callback_data='nazad10')]
])

nazad1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад', callback_data='nazad')]
])

gaz = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💨 PM2.5', callback_data='pm2'),
     InlineKeyboardButton(text='🌫 PM10', callback_data='pm10')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='nazad')]
])

vtorp = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🏭 Промисловість', callback_data='prom'),
     InlineKeyboardButton(text='⚡️ Енергетика', callback_data='energ')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='nazad1')]
])

promi = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🛠 Машинобудування', callback_data='mash'),
     InlineKeyboardButton(text='🍞 Харчова', callback_data='harch')],
    [InlineKeyboardButton(text='👕 Легка', callback_data='legk'),
     InlineKeyboardButton(text='🪵 Деревообробна', callback_data='derev')],
    [InlineKeyboardButton(text='🏗 Будівельна', callback_data='budiv'),
     InlineKeyboardButton(text='🔙 Назад', callback_data='nazad2')]
])

energo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔥 ТЕЦ', callback_data='tec'),
     InlineKeyboardButton(text='🛢 Газові родовища', callback_data='gazd')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='nazad2')]
])

nazado2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад', callback_data='nazad3')]
])

pervin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🏹 Полювання', callback_data='polyv'),
     InlineKeyboardButton(text='🎣 Риболовство', callback_data='riba')],
    [InlineKeyboardButton(text='🌱 Сільське господарство', callback_data='silsik'),
     InlineKeyboardButton(text='⛏ Видобувна промисловість', callback_data='vudob')],
    [InlineKeyboardButton(text='🌲 Лісове господарство', callback_data='lis'),
     InlineKeyboardButton(text='🔙 Назад', callback_data='nazad7')]
])

tretun = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🛒 Торгівля', callback_data='torg'),
     InlineKeyboardButton(text='🚛 Логістика', callback_data='log')],
    [InlineKeyboardButton(text='🎓 Освіта', callback_data='osv'),
     InlineKeyboardButton(text='🎭 Розваги та туризм', callback_data='turz')],
    [InlineKeyboardButton(text='🏥 Охорона здоров`я', callback_data='zdor'),
     InlineKeyboardButton(text='🏛 Державне управління', callback_data='derg')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='nazad7')]
])

zapovidn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🏞 Національні природні парки', callback_data='park'),
     InlineKeyboardButton(text='🌺 Ботанічні сади', callback_data='botan')],
    [InlineKeyboardButton(text='🦅 Державні заказники', callback_data='zakaz'),
     InlineKeyboardButton(text='🔙 Назад', callback_data='nazad10')]
])

nazadik = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад',callback_data='nazad4')]
])

nazadron = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад',callback_data='nazad5')]
])

nazadrist= InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад',callback_data='nazad6')]
])

nazadndo= InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад',callback_data='nazad7')]
])

naza345= InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад',callback_data='nazad8')]
])

naza000= InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад',callback_data='nazad')]
])

naza111 =  InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад',callback_data='nazad9')]
])