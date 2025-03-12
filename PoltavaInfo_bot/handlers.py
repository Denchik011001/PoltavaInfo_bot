from aiogram import   Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from humanfriendly.terminal import message
from numpy.ma.core import repeat

import keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import requests
import pandas as pd
import asyncio
from g4f.client import Client

from keyboards import  nazadrist, naza000, zapovidn, naza111

router = Router()

open_token = "e6f1ade4df17660117e41a680bd070fe"
router = Router()

class WeatherStates(StatesGroup):
    waiting_for_city = State()

class ReserveState(StatesGroup):
    waiting_for_reserve_name = State()

class ReserveStatePam(StatesGroup):
    waiting_for_reserve_name_pam = State()

class CityState(StatesGroup):
    waiting_for_city_name = State()

class RadioState(StatesGroup):
    waiting_for_info_rad = State()

class VtoreEnergo(StatesGroup):
    waiting_for_info_energo = State()
city_translations = {
    "гоголеве": "Gogoleve",
    "зіньків": "Zinkiv",
    "миргород": "Myrhorod",
    "полтава": "Poltava",
    "чорнухи": "Chornukhy"
}
city_translations_ost = {
    "андріївка": "Andriivka",
    "байрак": "Bairak",
    "балясне": "Baliasne",
    "батьки": "Batky",
    "велика рудка": "Velyka Rudka",
    "великі будища": "Velyki Budyshcha",
    "водяна балка": "Vodiana Balka",
    "гадяч": "Hadiach",
    "горішні плавні": "Horishni Plavni",
    "диканька": "Dykanka",
    "кременчук": "Kremenchuk",
    "лубни": "Lubny",
    "малі будища": "Mali Budyshcha",
    "михайлівка": "Mykhailivka",
    "надежда": "Nadezhda",
    "нові санжари": "Novi Sanzhary",
    "опішня": "Opishnia",
    "орданівка": "Ordanivka",
    "попівка": "Popivka",
    "решетилівка": "Reshetylivka",
    "стасі": "Stasi",
    "супрунівка": "Suprunivka",
    "христанівка": "Khrystanivka",
    "човно-федорівка": "Chovno-Fedorivka"
}

city_rad = {
    "полтава": {
        "description": "Радіаційний фон у Полтаві",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.12 мкЗв/год",
                "details": "Рівень безпечний, відповідає нормам радіаційної безпеки."
            }
        }
    },
    "кременчук": {
        "description": "Радіаційний фон у Кременчуці",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.14 мкЗв/год",
                "details": "Стабільний радіаційний фон, нижче допустимих норм."
            }
        }
    },
    "горішні плавні": {
        "description": "Радіаційний фон у Горишніх Плавнях",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.13 мкЗв/год",
                "details": "Фон в межах норми, безпечний для здоров'я."
            }
        }
    },
    "лубни": {
        "description": "Радіаційний фон у Лубнах",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.11 мкЗв/год",
                "details": "Низький радіаційний фон, стабільний."
            }
        }
    },
    "миргород": {
        "description": "Радіаційний фон у Миргороді",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.10 мкЗв/год",
                "details": "Чистий регіон, низький рівень радіації."
            }
        }
    },
    "гадяч": {
        "description": "Радіаційний фон у Гадячі",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.15 мкЗв/год",
                "details": "Рівень фону трохи вищий за середній, але в межах безпечного."
            }
        }
    },
    "зеньків": {
        "description": "Радіаційний фон у Зенькові",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.13 мкЗв/год",
                "details": "Стабільний радіаційний фон у межах норми."
            }
        }
    },
    "карлівка": {
        "description": "Радіаційний фон у Карлівці",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.12 мкЗв/год",
                "details": "Радіаційний фон низький і стабільний."
            }
        }
    },
    "пирятин": {
        "description": "Радіаційний фон у Пирятині",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.11 мкЗв/год",
                "details": "Чисте середовище, радіація в межах норми."
            }
        }
    },
    "хорол": {
        "description": "Радіаційний фон у Хоролі",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.10 мкЗв/год",
                "details": "Низький рівень радіації, комфортно для проживання."
            }
        }
    },
    "лохвиця": {
        "description": "Радіаційний фон у Лохвиці",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.14 мкЗв/год",
                "details": "Радіаційний фон стабільний, в межах безпеки."
            }
        }
    },
    "решетилівка": {
        "description": "Радіаційний фон у Решетилівці",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.13 мкЗв/год",
                "details": "Безпечний рівень, відповідає нормам."
            }
        }
    },
    "нові санжари": {
        "description": "Радіаційний фон у Нових Санжарах",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.12 мкЗв/год",
                "details": "Радіаційний фон стабільний і безпечний."
            }
        }
    },
    "котельва": {
        "description": "Радіаційний фон у Котельві",
        "factories": {
            0: {
                "name": "Радіаційний фон",
                "value": "0.11 мкЗв/год",
                "details": "Стабільний рівень, сприятливий для проживання."
            }
        }
    }
}

city_data = {
    "андріївка": {
        "description": "Стан повітря у Андріївці",
        "factories": {
            0: {
                "name": "Air Quality Index: 15 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "байрак": {
        "description": "Стан повітря у Байраку",
        "factories": {
            0: {
                "name": "Air Quality Index: 20 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "балясне": {
        "description": "Стан повітря у Балясному",
        "factories": {
            0: {
                "name": "Air Quality Index: 18 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "батьки": {
        "description": "Стан повітря у Батьках",
        "factories": {
            0: {
                "name": "Air Quality Index: 14 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "велика рудка": {
        "description": "Стан повітря у Великій Рудці",
        "factories": {
            0: {
                "name": "Air Quality Index: 16 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "великі будища": {
        "description": "Стан повітря у Великих Будищах",
        "factories": {
            0: {
                "name": "Air Quality Index: 19 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "водяна балка": {
        "description": "Стан повітря у Водяній Балці",
        "factories": {
            0: {
                "name": "Air Quality Index: 22 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "гадяч": {
        "description": "Стан повітря у Гадячі",
        "factories": {
            0: {
                "name": "Air Quality Index: 21 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "горішні плавні": {
        "description": "Стан повітря у Горішніх Плавнях",
        "factories": {
            0: {
                "name": "Air Quality Index: 24 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "диканька": {
        "description": "Стан повітря у Диканьці",
        "factories": {
            0: {
                "name": "Air Quality Index: 23 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "човно-федорівка": {
        "description": "Стан повітря у Човно-Федорівці",
        "factories": {
            0: {
                "name": "Air Quality Index: 12 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "кременчук": {
        "description": "Стан повітря у Кременчуці",
        "factories": {
            0: {
                "name": "Air Quality Index: 25 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "лубни": {
        "description": "Стан повітря у Лубнах",
        "factories": {
            0: {
                "name": "Air Quality Index: 28 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "малі будища": {
        "description": "Стан повітря у Малих Будищах",
        "factories": {
            0: {
                "name": "Air Quality Index: 20 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "михайлівка": {
        "description": "Стан повітря у Михайлівці",
        "factories": {
            0: {
                "name": "Air Quality Index: 22 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "надежда": {
        "description": "Стан повітря у Надежді",
        "factories": {
            0: {
                "name": "Air Quality Index: 18 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "нові санжари": {
        "description": "Стан повітря у Нових Санжарах",
        "factories": {
            0: {
                "name": "Air Quality Index: 24 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "опішня": {
        "description": "Стан повітря у Опішні",
        "factories": {
            0: {
                "name": "Air Quality Index: 26 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "орданівка": {
        "description": "Стан повітря у Орданівці",
        "factories": {
            0: {
                "name": "Air Quality Index: 19 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "попівка": {
        "description": "Стан повітря у Попівці",
        "factories": {
            0: {
                "name": "Air Quality Index: 23 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "решетилівка": {
        "description": "Стан повітря у Решетилівці",
        "factories": {
            0: {
                "name": "Air Quality Index: 21 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "стасі": {
        "description": "Стан повітря у Стасах",
        "factories": {
            0: {
                "name": "Air Quality Index: 27 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "супрунівка": {
        "description": "Стан повітря у Супрунівці",
        "factories": {
            0: {
                "name": "Air Quality Index: 25 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    },
    "христанівка": {
        "description": "Стан повітря у Христанівці",
        "factories": {
            0: {
                "name": "Air Quality Index: 20 aqi",
                "description": "Дані щодо якості повітря застарілі.\nОстанній розрахунок проводився 21:00, 14 січня 2025 року."
            }
        }
    }
}



allowed_cities = {"Полтава", "Кременчук", "Горішні Плавні", "Лубни", "Миргород", "Гадяч", "Глобине", "Гребінка", "Заводське", "Зіньків", "Карлівка", "Кобеляки", "Лохвиця", "Пирятин", "Решетилівка", "Хорол"}

file_path = "Книга4d232340000.xlsx"
data = pd.read_excel(file_path)


file_pathpam = "Памяткипомістамфінал.xlsx"
datapam = pd.read_excel(file_pathpam)

file_energo = "Легккапром1.xlsx"
dataener = pd.read_excel(file_energo)

file_perv = "Первинний сектор економікиперероб.xlsx"
dataperv = pd.read_excel(file_perv)

file_tec = "Тецперероб.xlsx"
datatec = pd.read_excel(file_tec)

file_tret = "Третиннийсекторекономікиперероб1.xlsx"
datatret = pd.read_excel(file_tret)


@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.reply('Привіт. Вибери, що ти хочеш дізнатися про Полтавську область?',
    reply_markup = kb.main)

@router.callback_query(F.data == 'sect')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.sector)


@router.callback_query(F.data == 'nazad')
async def nazado(callback: CallbackQuery, state: FSMContext):
    datagon = await state.get_data()
    cloud = datagon.get("cloud", [])
    for message_id in cloud:
        try:
            await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=message_id)
        except Exception as e:
            print(f"Не вдалося видалити повідомлення {message_id}: {e}")
    await state.update_data(cloud=[])
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не вдалося видалити повідомлення з кнопкою: {e}")


    await callback.message.answer('Привіт. Вибери, що ти хочеш дізнатися про Полтавську область?',
    reply_markup = kb.main)








@router.callback_query(F.data == "pogoda")
async def start_weather(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Привіт! Введіть назву міста:")
    await state.set_state(WeatherStates.waiting_for_city)

@router.callback_query(F.data == "povit")
async def start_weather(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Привіт! Введіть назву міста, про яке хочете дізнатися якість повітря:")
    await state.set_state(CityState.waiting_for_city_name)


@router.message(WeatherStates.waiting_for_city)
async def get_weather(message: Message, state: FSMContext):
    city = message.text.strip().title()

    if city not in allowed_cities:
        await message.reply("Не вдалося знайти місто. Спробуйте одне з наступних: Полтава, Кременчук, Горішні Плавні.",
                            reply_markup=kb.nazad1)
        return

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_token}&units=metric"
        )
        data = r.json()

        city_name = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]


        await message.reply(
            f"***{datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f"Погода в місті: {city_name}\nТемпература: {cur_weather}°C\n"
            f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\nВітер: {wind} м/с\n"
            f"Гарного дня!",
            reply_markup=kb.nazad1
        )
    except Exception as e:
        await message.reply("Сталася помилка під час отримання погоди. Спробуйте ще раз.")
        print(e)


    await state.set_state(WeatherStates.waiting_for_city)


@router.message(RadioState.waiting_for_info_rad)
async def get_pov(message: Message, state: FSMContext):
    city_name_ua = message.text.strip().lower()
    data = await state.get_data()
    message_ids = data.get("message_ids", [])

    if city_name_ua.isdigit():
        msg = await message.reply("Введіть текст, а не цифру.", reply_markup=kb.nazad1)
        message_ids.append(msg.message_id)
        await state.update_data(message_ids=message_ids)
        return
    else:
        if city_name_ua not in city_rad:
            msg = await message.reply(
                "Не вдалося знайти місто у переліку. Введіть місто Полтавської області.",
                reply_markup=kb.nazad1
            )

            message_ids.append(msg.message_id)
            await state.update_data(message_ids=message_ids)
            return
        else:
            city_data = city_rad[city_name_ua]
            response = f"Місто <b>{city_name_ua.capitalize()}</b> - {city_data['description']}\n\n"
            for i, v in city_data["factories"].items():
                response += f"<b>{i + 1}.</b> {v['name']}\n{v.get('value', '')}\n{v.get('details', '')}\n\n"

            msg = await message.answer(response.strip(), parse_mode="HTML", reply_markup=kb.nazad1)
            message_ids.append(msg.message_id)
            await state.update_data(message_ids=message_ids)


@router.message(CityState.waiting_for_city_name)
async def get_pov(message: Message, state: FSMContext):
    city_name_ua = message.text.strip().lower()
    city_name_en = city_translations.get(city_name_ua)
    city_name_english = city_translations_ost.get(city_name_ua)
    if city_name_ua.isdigit():
        await message.reply(f"Введіть текст."
                            ,reply_markup=kb.nazad1)
        return
    else:
        if not city_name_en:
             if not city_name_english:
                 await message.reply(f"Не вдалося знайти місто у переліку. Введіть місто Полтавської області")
                 return
             else:
                 response = f"Місто <b>{city_name_ua.capitalize()}</b> - {city_data[city_name_ua]['description']}\n"
                 for i, v in city_data[city_name_ua]["factories"].items():
                     response += f"<b>{i + 1}</b>.{v['name']}\n{v['description']}\n"
                 await message.answer(response,parse_mode="HTML", reply_markup=kb.gaz)
                 return


        try:
            r = requests.get("https://api.saveecobot.com/output.json")
            data = r.json()

            for item in data:
                if item.get('cityName', '').strip().lower() == city_name_en.lower():
                    station_name = item.get('stationName', 'Станція не вказана')
                    pollutants_text = "Параметри якості повітря:\n"

                    pollutants = item.get('pollutants', [])
                    if not pollutants:
                        pollutants_text += "Дані про забруднювачі відсутні."
                    else:
                        for pollutant in pollutants:
                            if pollutant['pol'].lower() not in ['temperature', 'температура'] and pollutant['pol'].lower() not in ['humidity'] and pollutant['pol'].lower() not in ['pressure']:
                                pol = pollutant.get('pol', 'Невідомо')
                                value = pollutant.get('value', 'Невідомо')
                                unit = pollutant.get('unit', '')
                                emoji = ""
                                if pol ==  'Air Quality Index':
                                    pol = "Індекс якості повітря"
                                    value = pollutant.get('value', 'Невідомо')
                                    unit = pollutant.get('unit', '')

                                    pollutants_text += f"  - 🌬️<b>{pol}</b>: {value} {unit}\n"
                                else:
                                    if pol ==  "PM2.5":
                                        emoji = "💨"
                                    else:
                                        emoji ="🌪️"
                                    pollutants_text += f"  - {emoji}<b>{pol}</b>: {value} {unit}\n"


                    await message.reply(
                        f"Знайдено місто: {item['cityName']}\nСтанція: {station_name}\n\n{pollutants_text}",parse_mode="HTML",
                        reply_markup=kb.gaz
                    )
                    break
            else:
                await message.reply("Місто не знайдено у даних API!")
        except Exception as e:
            await message.reply("Сталася помилка під час отримання стану повітря. Спробуйте ще раз.")
            print(e)

        await state.set_state(CityState.waiting_for_city_name)




#Заповідники




@router.callback_query(F.data == 'zapov')
async def catalog(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Виберіть, про що саме хочете дізнатися', reply_markup=zapovidn)


@router.callback_query(F.data == 'park')
async def get_reserve_info(callback: CallbackQuery, state: FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_energ = " Національні природні парки"

    start_index = data[data.iloc[:, 0].astype(str).str.contains(district_energ, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        # await callback.message.answer(f"📍 Информация о районе: <b>{district_energ}</b>\n\n", parse_mode="HTML")
        cloud = []

        for i in range(start_index + 1, len(data)):
            row = data.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Назва об`єкту:</b> {row.get('Назва об`єкту', 'Не указано')}\n"
                    f"🔖 <b>Категорія:</b> {row.get('Категорія', 'Не указано')}\n"
                    f"📊 <b>Площа, га:</b> {row.get('Площа, га', 'Не указано')}\n"
                    f"📍 <b>Місцезнаходження заповідного об`єкту:</b> {row.get('Місцезнаходження заповідного об`єкту', 'Не указано')}\n"
                    f"📜 <b>Постанова створено даний об`єкт:</b> {row.get('Постанова, рішення, згідно якої створено даний об`єкт', 'Не указано')}\n\n"
                )
                # msg = await callback.message.answer(info, parse_mode="HTML")
                # cloud.append(msg.message_id)

                # Якщо це останнє повідомлення або наступне не є числовим, надсилаємо додаткове повідомлення
                if i == len(data) - 1 or not isinstance(data.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")

@router.callback_query(F.data == 'nazad9')
async def secto_eco(callback: CallbackQuery, state: FSMContext):
    datagon = await state.get_data()
    cloud = datagon.get("cloud", [])
    for message_id in cloud:
        try:
            await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=message_id)
        except Exception as e:
            print(f"Не вдалося видалити повідомлення {message_id}: {e}")
    await state.update_data(cloud=[])
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не вдалося видалити повідомлення з кнопкою: {e}")

@router.callback_query(F.data == 'botan')
async def get_reserve_info(callback: CallbackQuery, state: FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_energ = "Пам'ятки природи,ботанічні сади та парки загальнодержавного значення"


    start_index = data[data.iloc[:, 0].astype(str).str.contains(district_energ, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(data)):
            row = data.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Назва об`єкту:</b> {row.get('Назва об`єкту', 'Не указано')}\n"
                    f"🔖 <b>Категорія:</b> {row.get('Категорія', 'Не указано')}\n"
                    f"📊 <b>Площа, га:</b> {row.get('Площа, га', 'Не указано')}\n"
                    f"📍 <b>Місцезнаходження заповідного об`єкту:</b> {row.get('Місцезнаходження заповідного об`єкту', 'Не указано')}\n"
                    f"📜 <b>Постанова створено даний об`єкт:</b> {row.get('Постанова, рішення, згідно якої створено даний об`єкт', 'Не указано')}\n\n"
                )
                if i == len(data) - 1 or not isinstance(data.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")

@router.callback_query(F.data == 'zakaz')
async def get_reserve_info(callback: CallbackQuery,  state: FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_energ = "Заказники загальнодержавного значення"


    start_index = data[data.iloc[:, 0].astype(str).str.contains(district_energ, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(data)):
            row = data.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Назва об`єкту:</b> {row.get('Назва об`єкту', 'Не указано')}\n"
                    f"🔖 <b>Категорія:</b> {row.get('Категорія', 'Не указано')}\n"
                    f"📊 <b>Площа, га:</b> {row.get('Площа, га', 'Не указано')}\n"
                    f"📍 <b>Місцезнаходження заповідного об`єкту:</b> {row.get('Місцезнаходження заповідного об`єкту', 'Не указано')}\n"
                    f"📜 <b>Постанова створено даний об`єкт:</b> {row.get('Постанова, рішення, згідно якої створено даний об`єкт', 'Не указано')}\n\n"
                )
                if i == len(data) - 1 or not isinstance(data.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")




@router.callback_query(F.data == 'pamat')
async def catalog(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Напишіть назву міста, про пам`ятки якого хочете дізнатися.')

    await state.set_state(ReserveStatePam.waiting_for_reserve_name_pam)

@router.message(ReserveStatePam.waiting_for_reserve_name_pam)
async def get_reserve_info(message: Message, state: FSMContext):
    if data is None or data.empty:
        await message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_name = message.text.strip()


    start_index = datapam[datapam.iloc[:, 0].astype(str).str.contains(district_name, case=False, na=False)].index

    if start_index.empty:
        await message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(datapam)):
            row = datapam.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                                    f"🌳 <b>Назва об`єкту:</b> {row.get('Назва об`єкту', 'Не указано')}\n"
                                    f"🔖 <b>Категорія:</b> {row.get('Категорія', 'Не указано')}\n"
                                    f"📊 <b>Площа:</b> {row.get('Площа, га', 'Не указано')} га\n"
                                    f"📍 <b>Місцезнаходження:</b> {row.get('Місцезнаходження заповідного об`єкту', 'Не указано')}\n"
                                    f"📜 <b>Правова підстава:</b> {row.get('Постанова, рішення, згідно якої створено даний об`єкт', 'Не указано')}\n\n"
                                )
                if i == len(datapam) - 1 or not isinstance(datapam.iloc[i + 1, 0], (int, float)):
                    msg = await message.answer(info, parse_mode="HTML", reply_markup=naza000)
                    cloud.append(msg.message_id)
                else:
                    msg = await message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)


@router.callback_query(lambda callback_query: callback_query.data == "pm2")
async def handle_callback(callback_query: types.CallbackQuery):
    await callback_query.answer("PM2.5 — це дрібнодисперсні частинки діаметром 2.5 мікрометра або менше, які знаходяться у повітрі.", show_alert=True)

@router.callback_query(lambda callback_query: callback_query.data == "pm10")
async def handle_callback(callback_query: types.CallbackQuery):
    await callback_query.answer("PM10 — це тверді частинки та краплі рідини в повітрі діаметром 10 мікрометрів або менше.", show_alert=True)

@router.callback_query(F.data == "radioc")
async def ask_gpt(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введіть назву міста полтавської області')
    await state.set_state(RadioState.waiting_for_info_rad)

@router.message(RadioState.waiting_for_info_rad)
async def answer_gpt(message: Message, state: FSMContext):
    city = message.text.strip()
    client = Client()
    content = (f"Привет, я ищу данные о радиационном фоне в городе {city}. Пожалуйста, предоставь  информацию в формате: (Город: {city}, радиационный фон: [значение в мкЗв/ч], дата замера: [дата].) Напиши последние данные которые у тебя есть. "
               )
    response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": {content}}],
    )
    await message.reply(response.choices[0].message.content)


@router.callback_query(F.data == 'vtor')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.vtorp)

@router.callback_query(F.data == 'prom')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.promi)

@router.callback_query(F.data == 'energ')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.energo)

@router.callback_query(F.data == 'nazad2')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.vtorp)

@router.callback_query(F.data == 'nazad1')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.sector)

@router.callback_query(F.data == 'nazad3')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.vtorp)

@router.callback_query(F.data == 'nazad4')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.pervin)

@router.callback_query(F.data == 'nazad5')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.energo)

@router.callback_query(F.data == 'nazad6')
async def secto_eco(callback: CallbackQuery, state = FSMContext):
    datagon = await state.get_data()
    cloud = datagon.get("cloud", [])
    for message_id in cloud:
        try:
            await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=message_id)
        except Exception as e:
            print(f"Не вдалося видалити повідомлення {message_id}: {e}")
    await state.update_data(cloud=[])
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не вдалося видалити повідомлення з кнопкою: {e}")

@router.callback_query(F.data == 'nazad7')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.sector)

@router.callback_query(F.data == 'nazad8')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.tretun)

@router.callback_query(F.data == 'nazad10')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть, що хочете дізнатися',
                         reply_markup=kb.main)





@router.callback_query(F.data == 'mash')
async def get_reserve_info(callback: CallbackQuery, state= FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_energ = "Машинободування"


    start_index = dataener[dataener.iloc[:, 0].astype(str).str.contains(district_energ, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(dataener)):
            row = dataener.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                                    f"🌳 <b>Місто:</b> {row.get('Місто', 'Не указано')}\n"
                                    f"🔖 <b>Дата заснування заводу:</b> {row.get('Дата заснування заводу', 'Не указано')}\n"
                                    f"📊 <b>Основна продукція :</b> {row.get('Основна', 'Не указано')}\n"
                                    f"📍 <b>Приблизна кількість продукції за весь час :</b> {row.get('Приблизна кількість продукції за весь час ', 'Не указано')}\n"
                                )
                if i == len(dataener) - 1 or not isinstance(dataener.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=nazadrist)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")






@router.callback_query(F.data == 'harch')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_energ = "Харчова промисловість"


    start_index = dataener[dataener.iloc[:, 0].astype(str).str.contains(district_energ, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(dataener)):
            row = dataener.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Місто:</b> {row.get('Місто', 'Не указано')}\n"
                    f"🔖 <b>Дата заснування заводу:</b> {row.get('Дата заснування заводу', 'Не указано')}\n"
                    f"📊 <b>Основна продукція :</b> {row.get('Основна', 'Не указано')}\n"
                    f"📍 <b>Приблизна кількість продукції за весь час :</b> {row.get('Приблизна кількість продукції за весь час ', 'Не указано')}\n"
                )
                if i == len(dataener) - 1 or not isinstance(dataener.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=nazadrist)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")




@router.callback_query(F.data == 'legk')
async def get_reserve_info(callback: CallbackQuery,state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_energ = "Легка промисловість"


    start_index = dataener[dataener.iloc[:, 0].astype(str).str.contains(district_energ, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(dataener)):
            row = dataener.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Місто:</b> {row.get('Місто', 'Не указано')}\n"
                    f"🔖 <b>Дата заснування заводу:</b> {row.get('Дата заснування заводу', 'Не указано')}\n"
                    f"📊 <b>Основна продукція :</b> {row.get('Основна', 'Не указано')}\n"
                    f"📍 <b>Приблизна кількість продукції за весь час :</b> {row.get('Приблизна кількість продукції за весь час ', 'Не указано')}\n"
                )
                if i == len(dataener) - 1 or not isinstance(dataener.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=nazadrist)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")



@router.callback_query(F.data == 'derev')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_energ = "Деревообробна промисл."


    start_index = dataener[dataener.iloc[:, 0].astype(str).str.contains(district_energ, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(dataener)):
            row = dataener.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Місто:</b> {row.get('Місто', 'Не указано')}\n"
                    f"🔖 <b>Дата заснування заводу:</b> {row.get('Дата заснування заводу', 'Не указано')}\n"
                    f"📊 <b>Основна продукція :</b> {row.get('Основна', 'Не указано')}\n"
                    f"📍 <b>Приблизна кількість продукції за весь час :</b> {row.get('Приблизна кількість продукції за весь час ', 'Не указано')}\n"
                )
                if i == len(dataener) - 1 or not isinstance(dataener.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=nazadrist)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")



@router.callback_query(F.data == 'budiv')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_energ = "Будівельні матеріали"

    start_index = dataener[dataener.iloc[:, 0].astype(str).str.contains(district_energ, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(dataener)):
            row = dataener.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Місто:</b> {row.get('Місто', 'Не указано')}\n"
                    f"🔖 <b>Дата заснування заводу:</b> {row.get('Дата заснування заводу', 'Не указано')}\n"
                    f"📊 <b>Основна продукція :</b> {row.get('Основна', 'Не указано')}\n"
                    f"📍 <b>Приблизна кількість продукції за весь час :</b> {row.get('Приблизна кількість продукції за весь час ', 'Не указано')}\n"
                )
                if i == len(dataener) - 1 or not isinstance(dataener.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=nazadrist)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break


        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")







@router.callback_query(F.data == 'perv')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.pervin)

@router.callback_query(F.data == 'polyv')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Полювання"


    start_index = dataperv[dataperv.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        # await callback.message.answer(f"📍 Информация о районе: <b>{district_energ}</b>\n\n", parse_mode="HTML")


        cloud = []

        for i in range(start_index + 1, len(dataperv)):
            row = dataperv.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Показник:</b> {row.get('Показник', 'Не указано')}\n"
                    f"🔖 <b>Дані/Опис:</b> {row.get('Дані/Опис', 'Не указано')}\n"
                )


                # msg = await callback.message.answer(info, parse_mode="HTML")
                # cloud.append(msg.message_id)


                if i == len(dataperv) - 1 or not isinstance(dataperv.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break


        await state.update_data(cloud=cloud)


        await callback.answer("Дані відправлені.")



@router.callback_query(F.data == 'riba')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Риболовство"


    start_index = dataperv[dataperv.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]

        cloud = []

        for i in range(start_index + 1, len(dataperv)):
            row = dataperv.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Показник:</b> {row.get('Показник', 'Не указано')}\n"
                    f"🔖 <b>Дані/Опис:</b> {row.get('Дані/Опис', 'Не указано')}\n"
                )

                if i == len(dataperv) - 1 or not isinstance(dataperv.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break


        await state.update_data(cloud=cloud)


        await callback.answer("Дані відправлені.")

@router.callback_query(F.data == 'silsik')
async def get_reserve_info(callback: CallbackQuery,state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Сільське господарство"


    start_index = dataperv[dataperv.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]

        cloud = []

        for i in range(start_index + 1, len(dataperv)):
            row = dataperv.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Показник:</b> {row.get('Показник', 'Не указано')}\n"
                    f"🔖 <b>Дані/Опис:</b> {row.get('Дані/Опис', 'Не указано')}\n"
                )
                if i == len(dataperv) - 1 or not isinstance(dataperv.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)


        await callback.answer("Дані відправлені.")

@router.callback_query(F.data == 'vudob')
async def get_reserve_info(callback: CallbackQuery,state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Видобувна промислові."


    start_index = dataperv[dataperv.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(dataperv)):
            row = dataperv.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Показник:</b> {row.get('Показник', 'Не указано')}\n"
                    f"🔖 <b>Дані/Опис:</b> {row.get('Дані/Опис', 'Не указано')}\n"
                )
                if i == len(dataperv) - 1 or not isinstance(dataperv.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")

@router.callback_query(F.data == 'lis')
async def get_reserve_info(callback: CallbackQuery,state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Лісове господарство"


    start_index = dataperv[dataperv.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(dataperv)):
            row = dataperv.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Показник:</b> {row.get('Показник', 'Не указано')}\n"
                    f"🔖 <b>Дані/Опис:</b> {row.get('Дані/Опис', 'Не указано')}\n"
                )
                if i == len(dataperv) - 1 or not isinstance(dataperv.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")




@router.callback_query(F.data == 'tec')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Тец"


    start_index = datatec[datatec.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(datatec)):
            row = datatec.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                                    f"🌳 <b>Назва:</b> {row.get('Назва ', 'Не указано')}\n"
                                    f"🔖 <b>Місцезнаходження:</b> {row.get('Місцузнаходження', 'Не указано')}\n"
                                )
                if i == len(datatec) - 1 or not isinstance(datatec.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")


# info = (
#                     f"🌳 <b>Назва:</b> {row.get('Назва ', 'Не указано')}\n"
#                     f"🔖 <b>Місцезнаходження:</b> {row.get('Місцузнаходження', 'Не указано')}\n"
#                 )

@router.callback_query(F.data == 'gazd')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Газові родовища"


    start_index = datatec[datatec.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(datatec)):
            row = datatec.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Назва:</b> {row.get('Назва ', 'Не указано')}\n"
                    f"🔖 <b>Місцезнаходження:</b> {row.get('Місцузнаходження', 'Не указано')}\n"
                )
                if i == len(datatec) - 1 or not isinstance(datatec.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")



@router.callback_query(F.data == 'tret')
async def secto_eco(callback: CallbackQuery):
      await callback.message.edit_text('Виберіть різновид сектору економіки',
                         reply_markup=kb.tretun)



@router.callback_query(F.data == 'torg')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Торгівля"


    start_index = datatret[datatret.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(datatret)):
            row = datatret.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Категорія:</b> {row.get('Категорія', 'Не указано')}\n"
                    f"🔖 <b>Показники:</b> {row.get('Показники', 'Не указано')}\n"
                )
                if i == len(datatret) - 1 or not isinstance(datatret.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)


        await callback.answer("Дані відправлені.")





@router.callback_query(F.data == 'log')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Логістика"


    start_index = datatret[datatret.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(datatret)):
            row = datatret.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Категорія:</b> {row.get('Категорія', 'Не указано')}\n"
                    f"🔖 <b>Показники:</b> {row.get('Показники', 'Не указано')}\n"
                )
                if i == len(datatret) - 1 or not isinstance(datatret.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")


@router.callback_query(F.data == 'osv')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Освіта"


    start_index = datatret[datatret.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(datatret)):
            row = datatret.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Категорія:</b> {row.get('Категорія', 'Не указано')}\n"
                    f"🔖 <b>Показники:</b> {row.get('Показники', 'Не указано')}\n"
                )
                if i == len(datatret) - 1 or not isinstance(datatret.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")


@router.callback_query(F.data == 'turz')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = " Розваги та туризм"


    start_index = datatret[datatret.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(datatret)):
            row = datatret.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Категорія:</b> {row.get('Категорія', 'Не указано')}\n"
                    f"🔖 <b>Показники:</b> {row.get('Показники', 'Не указано')}\n"
                )
                if i == len(datatret) - 1 or not isinstance(datatret.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")


@router.callback_query(F.data == 'zdor')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Охорона здоров'я"


    start_index = datatret[datatret.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]
        cloud = []

        for i in range(start_index + 1, len(datatret)):
            row = datatret.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Категорія:</b> {row.get('Категорія', 'Не указано')}\n"
                    f"🔖 <b>Показники:</b> {row.get('Показники', 'Не указано')}\n"
                )


                if i == len(datatret) - 1 or not isinstance(datatret.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break
        await state.update_data(cloud=cloud)
        await callback.answer("Дані відправлені.")


@router.callback_query(F.data == 'derg')
async def get_reserve_info(callback: CallbackQuery, state = FSMContext):
    if data is None or data.empty:
        await callback.message.reply("Ошибка: Файл с данными не загружен или пуст.")
        return

    district_perv = "Державне управління "


    start_index = datatret[datatret.iloc[:, 0].astype(str).str.contains(district_perv, case=False, na=False)].index

    if start_index.empty:
        await callback.message.answer("Район не найден.")
    else:
        start_index = start_index[0]

        cloud = []

        for i in range(start_index + 1, len(datatret)):
            row = datatret.iloc[i]

            if isinstance(row[0], (int, float)):

                info = (
                    f"🌳 <b>Категорія:</b> {row.get('Категорія', 'Не указано')}\n"
                    f"🔖 <b>Показники:</b> {row.get('Показники', 'Не указано')}\n"
                )


                if i == len(datatret) - 1 or not isinstance(datatret.iloc[i + 1, 0], (int, float)):
                    msg = await callback.message.answer(info, parse_mode="HTML", reply_markup=naza111)
                    cloud.append(msg.message_id)
                else:
                    msg = await callback.message.answer(info, parse_mode="HTML")
                    cloud.append(msg.message_id)

            else:
                break


        await state.update_data(cloud=cloud)

        await callback.answer("Дані відправлені.")