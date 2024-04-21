# импортируем библиотеки
from flask import Flask, request, jsonify
import logging
import random


# Создаём приложение.
# Мы передаём __name__, в нём содержится информация,
# в каком модуле мы находимся.
# В данном случае там содержится '__main__',
# так как мы обращаемся к переменной из запущенного модуля.
# Если бы такое обращение, например, произошло внутри модуля logging,
# то мы бы получили 'logging'
app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Создадим словарь, чтобы для каждой сессии общения
# с навыком хранились подсказки, которые видел пользователь.
# Это поможет нам немного разнообразить подсказки ответов
# (buttons в JSON ответа).
sessionStorage = {}

# флаги режимов
mod_eng = False
mod_flags = False
mod_towns = False
mod_buildings = False
mod_wonders = False
mod_type = False

# переменная, где хранится тип игры
type_mod = None

# в переменной хранится название города/флага/постройки, которое было выбранно
new = True

# словари со странами и их столицами
countries = {

    # Америка
    'America':
        {
            'США': 'USA',
            'Канада': 'Canada',
            'Мексика': 'Mexico',
            'Куба': 'Cuba',
            'Бразилия': 'Brazil',
            'Аргентина': 'Argentina',
            'Чили': 'Chile',
            'Перу': 'Peru',
            'Колумбия': 'Colombia',
            'Венесуэла': 'Venezuela',
            'Эквадор': 'Ecuador',
            'Гватемала': 'Guatemala',
            'Боливия': 'Bolivia',
            'Уругвай': 'Uruguay',
            'Парагвай': 'Paraguay',
            'Хондурас': 'Honduras',
            'Никарагуа': 'Nicaragua',
            'Коста-Рика': 'Costa Rica',
            'Сальвадор': 'El Salvador',
            'Багамы': 'Bahamas',
            'Барбадос': 'Barbados',
            'Белиз': 'Belize',
            'Доминика': 'Dominica',
            'Доминиканская Республика': 'Dominican Republic',
            'Гренада': 'Grenada',
            'Гаити': 'Haiti',
            'Гондурас': 'Honduras',
            'Ямайка': 'Jamaica',
            'Панама': 'Panama',
            'Сент-Люсия': 'Saint Lucia',
            'Сент-Винсент и Гренадины': 'Saint Vincent and the Grenadines',
            'Суринам': 'Suriname',
            'Тринидад и Тобаго': 'Trinidad and Tobago',
        },

    # Азия
    'Asia':
        {
            'Афганистан': 'Afghanistan',
            'Армения': 'Armenia',
            'Азербайджан': 'Azerbaijan',
            'Бахрейн': 'Bahrain',
            'Бангладеш': 'Bangladesh',
            'Бутан': 'Bhutan',
            'Бруней': 'Brunei',
            'Камбоджа': 'Cambodia',
            'Китай': 'China',
            'Восточный Тимор': 'East Timor',
            'Египет': 'Egypt',
            'Индия': 'India',
            'Индонезия': 'Indonesia',
            'Иран': 'Iran',
            'Ирак': 'Iraq',
            'Израиль': 'Israel',
            'Япония': 'Japan',
            'Иордания': 'Jordan',
            'Казахстан': 'Kazakhstan',
            'Кувейт': 'Kuwait',
            'Киргизия': 'Kyrgyzstan',
            'Лаос': 'Laos',
            'Ливан': 'Lebanon',
            'Малайзия': 'Malaysia',
            'Мальдивы': 'Maldives',
            'Монголия': 'Mongolia',
            'Мьянма': 'Myanmar',
            'Непал': 'Nepal',
            'Северная Корея': 'North Korea',
            'Оман': 'Oman',
            'Пакистан': 'Pakistan',
            'Палестина': 'Palestine',
            'Филиппины': 'Philippines',
            'Катар': 'Qatar',
            'Россия': 'Russia',
            'Саудовская Аравия': 'Saudi Arabia',
            'Сингапур': 'Singapore',
            'Южная Корея': 'South Korea',
            'Шри-Ланка': 'Sri Lanka',
            'Сирия': 'Syria',
            'Тайвань': 'Taiwan',
            'Таджикистан': 'Tajikistan',
            'Таиланд': 'Thailand',
            'Турция': 'Turkey',
            'Туркменистан': 'Turkmenistan',
            'ОАЭ': 'UAE',
            'Узбекистан': 'Uzbekistan',
            'Вьетнам': 'Vietnam',
            'Йемен': 'Yemen'
        },

    # Европа
    'Europe':
        {
            'Австрия': 'Austria',
            'Азербайджан': 'Azerbaijan',
            'Албания': 'Albania',
            'Андорра': 'Andorra',
            'Армения': 'Armenia',
            'Беларусь': 'Belarus',
            'Бельгия': 'Belgium',
            'Болгария': 'Bulgaria',
            'Босния и Герцеговина': 'Bosnia and Herzegovina',
            'Хорватия': 'Croatia',
            'Кипр': 'Cyprus',
            'Чехия': 'Czech Republic',
            'Дания': 'Denmark',
            'Эстония': 'Estonia',
            'Финляндия': 'Finland',
            'Франция': 'France',
            'Грузия': 'Georgia',
            'Германия': 'Germany',
            'Греция': 'Greece',
            'Венгрия': 'Hungary',
            'Исландия': 'Iceland',
            'Ирландия': 'Ireland',
            'Италия': 'Italy',
            'Казахстан': 'Kazakhstan',
            'Косово': 'Kosovo',
            'Латвия': 'Latvia',
            'Лихтенштейн': 'Liechtenstein',
            'Литва': 'Lithuania',
            'Люксембург': 'Luxembourg',
            'Северная Македония': 'North Macedonia',
            'Мальта': 'Malta',
            'Молдова': 'Moldova',
            'Монако': 'Monaco',
            'Черногория': 'Montenegro',
            'Нидерланды': 'Netherlands',
            'Норвегия': 'Norway',
            'Польша': 'Poland',
            'Португалия': 'Portugal',
            'Румыния': 'Romania',
            'Россия': 'Russia',
            'Сан-Марино': 'San Marino',
            'Сербия': 'Serbia',
            'Словакия': 'Slovakia',
            'Словения': 'Slovenia',
            'Испания': 'Spain',
            'Швеция': 'Sweden',
            'Швейцария': 'Switzerland',
            'Турция': 'Turkey',
            'Украина': 'Ukraine',
            'Великобритания': 'United Kingdom',
            'Ватикан': 'Vatican City'
        },

    # Африка
    'Africa':
        {
            'Алжир': 'Algeria',
            'Ангола': 'Angola',
            'Бенин': 'Benin',
            'Ботсвана': 'Botswana',
            'Буркина-Фасо': 'Burkina Faso',
            'Бурунди': 'Burundi',
            'Камерун': 'Cameroon',
            'Кабо-Верде': 'Cape Verde',
            'ЦАР': 'Central African Republic',
            'Чад': 'Chad',
            'Коморы': 'Comoros',
            'ДР Конго': 'DR Congo',
            'Республика Конго': 'Republic of the Congo',
            'Кот-д’Ивуар': "Côte d'Ivoire",
            'Джибути': 'Djibouti',
            'Египет': 'Egypt',
            'Экваториальная Гвинея': 'Equatorial Guinea',
            'Эритрея': 'Eritrea',
            'Эфиопия': 'Ethiopia',
            'Габон': 'Gabon',
            'Гамбия': 'Gambia',
            'Гана': 'Ghana',
            'Гвинея': 'Guinea',
            'Гвинея-Бисау': 'Guinea-Bissau',
            'Кения': 'Kenya',
            'Лесото': 'Lesotho',
            'Либерия': 'Liberia',
            'Ливия': 'Libya',
            'Мадагаскар': 'Madagascar',
            'Малави': 'Malawi',
            'Мали': 'Mali',
            'Мавритания': 'Mauritania',
            'Маврикий': 'Mauritius',
            'Марокко': 'Morocco',
            'Мозамбик': 'Mozambique',
            'Намибия': 'Namibia',
            'Нигер': 'Niger',
            'Нигерия': 'Nigeria',
            'Руанда': 'Rwanda',
            'Сан-Томе и Принсипи': 'São Tomé and Príncipe',
            'Сенегал': 'Senegal',
            'Сейшельские острова': 'Seychelles',
            'Сьерра-Леоне': 'Sierra Leone',
            'Сомали': 'Somalia',
            'ЮАР': 'South Africa',
            'Южный Судан': 'South Sudan',
            'Судан': 'Sudan',
            'Свазиленд': 'Swaziland',
            'Танзания': 'Tanzania',
            'Того': 'Togo',
            'Тунис': 'Tunisia',
            'Уганда': 'Uganda',
            'Замбия': 'Zambia',
            'Зимбабве': 'Zimbabwe'
        },

    # Столицы
    'capitals':
        {
            # Америка
            'America':
                {
                    'Аргентина': 'Буэнос-Айрес',
                    'Багамы': 'Нассау',
                    'Барбадос': 'Бриджтаун',
                    'Белиз': 'Бельмопан',
                    'Боливия': 'Сукре',
                    'Бразилия': 'Бразилиа',
                    'Канада': 'Оттава',
                    'Чили': 'Сантьяго',
                    'Колумбия': 'Богота',
                    'Коста-Рика': 'Сан-Хосе',
                    'Куба': 'Гавана',
                    'Доминика': 'Розо',
                    'Доминиканская Республика': 'Санто-Доминго',
                    'Эквадор': 'Кито',
                    'Сальвадор': 'Сан-Сальвадор',
                    'Гренада': 'Сент-Джорджес',
                    'Гватемала': 'Гватемала',
                    'Гаити': 'Порт-о-Пренс',
                    'Гондурас': 'Тегусигальпа',
                    'Ямайка': 'Кингстон',
                    'Мексика': 'Мехико',
                    'Никарагуа': 'Манагуа',
                    'Панама': 'Панама',
                    'Парагвай': 'Асунсьон',
                    'Перу': 'Лима',
                    'Сент-Люсия': 'Кастри',
                    'Сент-Винсент и Гренадины': 'Кингстаун',
                    'Суринам': 'Парамарибо',
                    'Тринидад и Тобаго': 'Порт-оф-Спейн',
                    'США': 'Вашингтон',
                    'Уругвай': 'Монтевидео',
                    'Венесуэла': 'Каракас'
                },

            # Азия
            'Asia':
                {
                    'Корея': 'Сеул',
                    'Афганистан': 'Кабул',
                    'Армения': 'Ереван',
                    'Азербайджан': 'Баку',
                    'Бангладеш': 'Дакка',
                    'Бутан': 'Тхимпху',
                    'Бруней': 'Бандар-Сери-Бегаван',
                    'Камбоджа': 'Пномпень',
                    'Китай': 'Пекин',
                    'Восточный Тимор': 'Дили',
                    'Индия': 'Нью-Дели',
                    'Индонезия': 'Джакарта',
                    'Иран': 'Тегеран',
                    'Ирак': 'Багдад',
                    'Израиль': 'Иерусалим',
                    'Япония': 'Токио',
                    'Иордания': 'Амман',
                    'Казахстан': 'Нур-Султан',
                    'Кувейт': 'Эль-Кувейт',
                    'Кыргызстан': 'Бишкек',
                    'Лаос': 'Вьентьян',
                    'Ливан': 'Бейрут',
                    'Малайзия': 'Куала-Лумпур',
                    'Мальдивы': 'Мале',
                    'Монголия': 'Улан-Батор',
                    'Мьянма': 'Нейпьидо',
                    'Непал': 'Катманду',
                    'Северная Корея': 'Пхеньян',
                    'Оман': 'Маскат',
                    'Пакистан': 'Исламабад',
                    'Палестина': 'Рамалла',
                    'Филиппины': 'Манила',
                    'Катар': 'Доха',
                    'Россия': 'Москва',
                    'Саудовская Аравия': 'Эр-Рияд',
                    'Сингапур': 'Сингапур',
                    'Южная Корея': 'Сеул',
                    'Шри-Ланка': 'Шри-Джаяварденепура-Котте',
                    'Сирия': 'Дамаск',
                    'Тайвань': 'Тайбэй',
                    'Таджикистан': 'Душанбе',
                    'Таиланд': 'Бангкок',
                    'Турция': 'Анкара',
                    'Туркменистан': 'Ашхабад',
                    'ОАЭ': 'Абу-Даби',
                    'Узбекистан': 'Ташкент',
                    'Вьетнам': 'Ханой',
                    'Йемен': 'Сана'

                },

            # Европа
            'Europe':
                {
                    'Австрия': 'Вена',
                    'Албания': 'Тирана',
                    'Андорра': 'Андорра-ла-Велья',
                    'Беларусь': 'Минск',
                    'Бельгия': 'Брюссель',
                    'Болгария': 'София',
                    'Босния и Герцеговина': 'Сараево',
                    'Хорватия': 'Загреб',
                    'Кипр': 'Никосия',
                    'Чехия': 'Прага',
                    'Дания': 'Копенгаген',
                    'Эстония': 'Таллин',
                    'Финляндия': 'Хельсинки',
                    'Франция': 'Париж',
                    'Германия': 'Берлин',
                    'Греция': 'Афины',
                    'Венгрия': 'Будапешт',
                    'Исландия': 'Рейкьявик',
                    'Ирландия': 'Дублин',
                    'Италия': 'Рим',
                    'Косово': 'Приштина',
                    'Латвия': 'Рига',
                    'Лихтенштейн': 'Вадуц',
                    'Литва': 'Вильнюс',
                    'Люксембург': 'Люксембург',
                    'Северная Македония': 'Скопье',
                    'Мальта': 'Валлетта',
                    'Молдова': 'Кишинев',
                    'Монако': 'Монако',
                    'Черногория': 'Подгорица',
                    'Нидерланды': 'Амстердам',
                    'Норвегия': 'Осло',
                    'Польша': 'Варшава',
                    'Португалия': 'Лиссабон',
                    'Румыния': 'Бухарест',
                    'Россия': 'Москва',
                    'Сан-Марино': 'Сан-Марино',
                    'Сербия': 'Белград',
                    'Словакия': 'Братислава',
                    'Словения': 'Любляна',
                    'Испания': 'Мадрид',
                    'Швеция': 'Стокгольм',
                    'Швейцария': 'Берн',
                    'Украина': 'Киев',
                    'Великобритания': 'Лондон',
                    'Ватикан': 'Ватикан'
                },

            # Африка
            'Africa':
                {
                    'Алжир': 'Алжир',
                    'Ангола': 'Луанда',
                    'Бенин': 'Порто-Ново',
                    'Ботсвана': 'Габороне',
                    'Буркина-Фасо': 'Уагадугу',
                    'Бурунди': 'Бужумбура',
                    'Габон': 'Либревиль',
                    'Гамбия': 'Банжул',
                    'Гана': 'Аккра',
                    'Гвинея': 'Конакри',
                    'Гвинея-Бисау': 'Бисау',
                    'Джибути': 'Джибути',
                    'Египет': 'Каир',
                    'Замбия': 'Лусака',
                    'Зимбабве': 'Хараре',
                    'Камерун': 'Яунде',
                    'Кения': 'Найроби',
                    'Коморы': 'Морони',
                    'Конго': 'Браззавиль',
                    'ДР Конго': 'Киншаса',
                    'Кот-д’Ивуар': 'Ямусукро',
                    'Лесото': 'Масеру',
                    'Либерия': 'Монровия',
                    'Ливия': 'Триполи',
                    'Маврикий': 'Порт-Луи',
                    'Мавритания': 'Нуакшот',
                    'Мадагаскар': 'Антананариву',
                    'Малави': 'Лилонгве',
                    'Мали': 'Бамако',
                    'Марокко': 'Рабат',
                    'Мозамбик': 'Мапуту',
                    'Намибия': 'Виндхук',
                    'Нигер': 'Ниамей',
                    'Нигерия': 'Абуджа',
                    'Руанда': 'Кигали',
                    'Сан-Томе и Принсипи': 'Сан-Томе',
                    'Сенегал': 'Дакар',
                    'Сейшельские Острова': 'Виктория',
                    'Сьерра-Леоне': 'Фритаун',
                    'Сомали': 'Могадишо',
                    'Судан': 'Хартум',
                    'Свазиленд': 'Мбабане',
                    'Танзания': 'Додома',
                    'Того': 'Ломе',
                    'Тунис': 'Тунис',
                    'Уганда': 'Кампала',
                    'Центральноафриканская Республика': 'Банги',
                    'Чад': 'Нджамена',
                    'Экваториальная Гвинея': 'Малабо',
                    'Эритрея': 'Асмэра',
                    'Эфиопия': 'Аддис-Абеба',
                    'ЮАР': 'Претория',
                    'Южный Судан': 'Джуба'
                }

        }
}

# словари с флагами
Flags = {

    # Америка
    'America':
        {
            'США': '1030494/56d2ff2be9707e20bccc',
            'Канада': '997614/e19d665d4d5ea0855e75',
            'Мексика': '1030494/71d5aaad8ecc5e8dddbb',
            'Куба': '1533899/f5e4462bad3ef3098793',
            'Бразилия': '1030494/69fa60fac39a21efcc16',
            'Аргентина': '213044/de0f207d13333b4586c8',
            'Чили': '997614/18168ec4a3d0314ab0a1',
            'Перу': '1030494/de3cc441f95a39b11e71',
            'Колумбия': '997614/6c22a06b5dcd94d9aef9',
            'Эквадор': '997614/199761b698958a41bfaf',
            'Гватемала': '213044/2444d2c9e767904363f0',
            'Боливия': '213044/b1f10c6de1ababfb8b2a',
            'Уругвай': '997614/a747737914fa380c0523',
            'Парагвай': '997614/3b1198f4461d2b079c47',
            'Гондурас': '997614/2cb9a0472ced68768020',
            'Никарагуа': '997614/2b18c4936dafe0297358',
            'Коста-Рика': '1030494/92e7020c522725f83812',
            'Сальвадор': '1030494/844a84424cacda14fa55'
        },

    # Азия
    'Asia':
        {
            'Япония': '213044/c3150bb7180ba9eda195',
            'Китай': '1030494/4f7c2a22e98331ba53cf',
            'Индия': '1533899/8f154105a7748274959a',
            'Индонезия': '213044/9e0d6a46dc07c35f60c4',
            'Южная Корея': '1030494/c6f91c342f3e51524d6a',
            'ОАЭ': '1030494/327e955e95c49b1e98ce',
            'Турция': '997614/76b437b8ca1f29213014',
            'Израиль': '1030494/e2a22bdc1c441cdefd77',
            'Малайзия': '213044/fb49a534222b422eb5d8',
            'Афганистан': '213044/4031ad7be23e70573219',
            'Пакистан': '213044/c5e2070381195a0ffb7f',
            'Филиппины': '1030494/49194adbd5e453f89fe3',
            'Ирак': '1030494/a00fb4e9702535aad62f',
            'Иран': '997614/c69b6f53655c85ef47e0',
            'Вьетнам': '1030494/67fb64f5cbb6e43ccddc',
            'Таиланд': '1533899/34549776eeb71424e519',
            'Бангладеш': '1533899/37b5aec404afe3a526f0',
            'Сингапур': '965417/4edaad7e870b2d31e0e8',
            'Сирия': '1533899/64044a5f0e8eccbb0ae1'
        },

    # Европа
    'Europe':
        {
            'Россия': '213044/7c00bbcacfdae3245be9',
            'Германия': '1030494/7a56f73fe043874c4c48',
            'Италия': '1533899/74efc92afc89661d4dc9',
            'Казахстан': '997614/36eab559162b06587361',
            'Франция': '213044/26c02d6b5aab2574ac45',
            'Великобритания': '1030494/28dec72144a3c03e8f22',
            'Испания': '997614/5554f0c9c9dbbaef729b',
            'Польша': '1533899/6467bc8783de686a542b',
            'Украина': '1521359/d6aab610f9541b66b410',
            'Греция': '1030494/4b09b5005a3fac42f199',
            'Австрия': '997614/d88d5edf54e445f25567',
            'Швейцария': '1030494/269c42738840039577cb',
            'Швеция': '1533899/5aef95d570b3765c6daa',
            'Норвегия': '1533899/92a40958ba8a1f6fc710',
            'Финляндия': '1533899/f0a047878606d0c57c8f',
            'Дания': '997614/b20d33a2d7a13d6c8dc3',
            'Исландия': '1030494/b4daa64ddd3c09941293',
            'Ирландия': '213044/13ac8bf400f73b0b3b4b',
            'Нидерланды': '1533899/3ebaba242ef4af5fdccb'
        },

    # Африка
    'Africa':
        {
            'Алжир': '997614/020c23cc81621782cac5',
            'Ангола': '937455/12b73cfd5abcc10df583',
            'Бенин': '937455/cc36a03d18a3a49258e6',
            'Ботсвана': '937455/01d2d8f32f1d995458bb',
            'Буркина-Фасо': '1652229/f7266a3ac113180fb75e',
            'Бурунди': '1656841/47c08ac7ca1e14367451',
            'Габон': '997614/affc9658656d98c47516',
            'Гамбия': '1521359/fa449b5054c97bdc84e3',
            'Гана': '1533899/e7bfbdbab2703bc150b3',
            'Гвинея': '997614/5d1e9707fe4026d22cc4',
            'Гвинея-Бисау': '1521359/987fa5611f57abfd5c3c',
            'Джибути': '213044/25ed4c78e62f154c6457',
            'Египет': '997614/23c5be4d4e4676e39f25',
            'Замбия': '1656841/d4ae7c088304668996d7',
            'Зимбабве': '1652229/81814e4b67a55aa86aad',
            'Камерун': '1652229/cf980e3ccba4dd92d1e9',
            'Кения': '937455/beec7a4a62d637593af3',
            'Коморы': '1521359/eb0ba76f3bd67a624884',
            'Конго': '1656841/56c404b50939e125d5a2',
            'ДР Конго': '1652229/308fe198cfc3d021070b',
            'Кот-д’Ивуар': '1652229/b12fd4c25815a4fe6130',
            'Лесото': '1030494/8c61afa5b7db572130fc',
            'Либерия': '1652229/ee8451d290731170def4',
            'Ливия': '1656841/79af181fc77978b12157',
            'Мавритания': '1656841/cc80e95521378de7b1ef',
            'Мадагаскар': '997614/185a909f2582e087ea34',
            'Малави': '1533899/64d6ead4e641d8b8b51a',
            'Мали': '1656841/42c85ecdf822ae9b436c',
            'Марокко': '997614/1bb5cce5a6e2f6112286',
            'Мозамбик': '997614/75576b6b661aea9903d6',
            'Намибия': '1656841/429aa8c878100e57411f',
            'Нигер': '1030494/f1c5298b5b7107d4412b',
            'Нигерия': '1652229/090483ac88937f1d7235',
            'Руанда': '997614/b21257fc9708a66e13ed',
            'Сан-Томе и Принсипи': '213044/7ee93d1638b4f974dabf',
            'Сенегал': '1652229/228ebb822db23b7a11ac',
            'Сейшельские Острова': '1521359/67b3e2b09eb44ef067bb',
            'Сьерра-Леоне': '1656841/b4b4844da4a28e951557',
            'Сомали': '1533899/512a0ace68c87a9a2aff',
            'Маврикий': '1533899/58cca52b3f878ffc3b5a',
            'Судан': '1533899/56ad5fd7a46965b75db2',
            'Свазиленд': '1521359/db5053069de75c57cde7',
            'Танзания': '1533899/5d1d6a54df665837ff48',
            'Того': '1656841/af73f3289215da314a13',
            'Уганда': '1652229/94cbf6333b3a6bca6b98',
            'Тунис': '1030494/82c0c6cbfcd0b434738f',
            'Центральноафриканская Республика': '1521359/0b0102547f98523170f0',
            'Чад': '1521359/b91ec55fec5ed2870642',
            'Экваториальная Гвинея': '1030494/176c46c6451e8edd1017',
            'Эритрея': '937455/f1616b30f00cac4c82ec',
            'Эфиопия': '997614/3fa08cf99d1eb5362ff4',
            'ЮАР': '1521359/a399a21d6df9ee652052',
            'Южный Судан': '937455/9226c0c7541a70923cd1'
        }

    }

# Постройки
Buildings = {

    # Америка
    'America':
        {
            'Эмпайр-стейт-Билдинг': '1652229/710b426802cce6224dbe',
            'Мачу-Пикчу': '1533899/0cb9726d81c5c704ff0b',
            'Флэтайрон-Билдинг': '1030494/ad3c099cc345ce11293b',
            'Статуя Свободы': '1540737/6d0ae58a8fc4eacaf3ac',
            'Бродвей': '1656841/03c5ff79d61edad2b459',
            'Пентагон': '1533899/30d4f16670a56b3a28ee',
            'Мост "Золотые ворота"': '997614/ad4951af40bf47b6801d',
            'Чичен-Ица': '1533899/0f3d8c8ae346977839e6',
            'Алькатрас': '1030494/1887d7c407df75dbe2c6',
            'Нотр-Дам де Монреаль': '937455/d1e6f131f1d1684d23d5'
        },

    # Азия
    'Asia':
        {
            'Бурдж Халифа': '1652229/debf47f70b8607230adf',
            'Тадж-Махал': '1030494/501227e985f5e1685ad2',
            'Великая Китайская стена': '997614/875eee1e0c2dfac9156c',
            'Петра': '213044/d2aadd6f5871ec38883a',
            'Кааба': '1652229/50a35a3469dd21e54686',
            'Ангкор-Ват': '1521359/5d663e0a018c0cec7da7',
            'Запретный город': '1521359/8167659a28d5da219a5b',
            'Мохенджо-Даро': '965417/e01d3654f447567ac9cd',
            'Дворец Потала': '1030494/7e6ce2bf353642c9d97e',
            'Терракотовая армия': '997614/d744bc38ea2d07cbbcd9',
            'Замок Химэдзи': '937455/aea51387a366e1623873'
        },

    # Европа
    'Europe':
        {
            'Храм Василия Блаженного': '1652229/ce5ac4124df56372618a',
            'Колизей': '997614/d7e8866a6ee073405f00',
            'Эйфелева башня': '213044/2de4c9a2e201cc804b8d',
            'Лувр': '213044/7e2893704eb3f3d4556e',
            'Биг-Бен': '213044/19c61b3f31b8de261fe7',
            'Стоунхендж': '1533899/6acde22c3b011f2896db',
            'Пизанская башня': '1521359/5114e22e193d3d95e9d3',
            'Айя-София': '1533899/1935fd8b0dfceb2a31da',
            'Акрополь': '1540737/1a447a78958bbfe0745a',
            'Триумфальная арка': '1652229/b83322f1b0f52dafe77a',
            'Площадь Святого Петра': '213044/20640ff80f91aa211aa1'
        },

    # Африка
    'Africa':
        {
            'Мечеть Дженне': '1030494/3e7d25d1c5f84f6eccd7',
            'Томбукту': '1652229/bd929c2657c142dee2b0',
            'Сфинкс': '937455/0c6c0057bc828a2610ee',
            'Джебель-Баркал': '213044/88b1eedf58d5ea423a6f',
            'Монумент воссоединения в Яунде': '1656841/e2e7103ad584b60edf4a',
            'Башня Набемба': '1521359/0607a38eac622f536d9d',
            'Лептис-Магна': '1030494/7791ee5476861cf4c53c',
            'Национальный театр Нигерии': '1656841/32ca35b3a24a423283ee',
            'Храм Арул Миху Навасакти Винайягар': '997614/d03abab3292b0d9e948a',
            'Пирамиды Мероэ': '1521359/ab6e5fef6d58cfaa1a54',
            'Собор Нотр-Дам в Банги': '1030494/5a51c969f463f2a444ea'
        },

    # 7 чудес света
    'wonders':
        {
            'Пирамида Хеопса': '213044/8487268bcea26140ad5e',
            'Александрийский маяк': '937455/e0611ef8e555dcaab398',
            'Висячие сады Семирамиды': '213044/a848a79d0f78727fe6ee',
            'Колосс Родосский': '1533899/fa5c347584e4a685c0a3',
            'Мавзолей в Галикарнасе': '1521359/4be2da3b500396e47649',
            'Храм Артемиды Эфесской': '213044/e588b4b3c392c221c29f',
            'Статуя Зевса в Олимпии': '1533899/f046b7e6f5f5d5ca50a9'
        }
}


# Получить случайную страну на английском и русском
def get_random_country_eng(type):
    # получаем случайную страну на русском
    random_country_rus = random.choice(list(countries[type].keys()))

    # берём выбранную страну на английском
    random_country_eng = countries[type][random_country_rus]

    # берём ещё 3 страны на русском
    new_random_countries_rus = list(random.sample(
        list(countries['Europe'].keys()) + list(countries['Asia'].keys())
        + list(countries['America'].keys()) + list(countries['Africa'].keys()), k=4))

    # проверяем, есть ли наша выбранная в начале страна в этом списке
    while random_country_rus in new_random_countries_rus:
        # если есть, меняем список, так, чтобы выбранной страны в нём не было
        new_random_countries_rus = random.sample(
            list(countries['Europe'].keys()) + list(countries['Asia'].keys())
            + list(countries['America'].keys()) + list(countries['Africa'].keys()), k=4)

    # добавляем в список русских стран, нашу страну
    new_random_countries_rus.append(random_country_rus)

    # перемешиваем список
    random.shuffle(new_random_countries_rus)

    # отравляем страну на английском, на русском и список из 4-х стран на русском
    return random_country_eng, random_country_rus, new_random_countries_rus


# Получить случайный флаг страны
def get_random_flag(type):
    # получаем случайный флаг
    random_flag = random.choice(list(Flags[type].items()))

    # получаем случайно ещё 3 флага
    random_countries_flags = random.sample(
        list(Flags['Europe']) + list(Flags['America']) + list(Flags['Asia']) + list(Flags['Africa']), k=4)

    # проверяем, если наш выбранный флаг есть в списке из 3-х флагов
    while random_flag in random_countries_flags:
        # если есть, меняем список, пока нашего флага в нём не будет
        random_countries_flags = random.sample(
            list(Flags['Europe']) + list(Flags['America'])
            + list(Flags['Asia']) + list(Flags['Africa']), k=4)

    # добавляем в список флагов, наш флаг
    random_countries_flags.append(random_flag[0])
    # перемешиваем список
    random.shuffle(random_countries_flags)

    # отправляем наш флаг и список флагов
    return (list(random_flag),
            sorted(random_countries_flags, key=lambda x: random.random()))


# Получить случайно 1 из чудес света
def get_random_wonders():

    # получаем случайную картинку
    random_wonder = random.choice(list(Buildings['wonders'].items()))

    # получаем случайно ещё 3 случайных картинки
    random_wonders = random.sample(list(Buildings['wonders']), k=3)

    # проверяем, если наш выбранная картинка есть в списке из 3-х случайных картинок
    while random_wonder in random_wonders:
        # если есть, меняем список, пока нашей картинки в нём не будет
        random_wonders = random.sample(list(Buildings['wonders']), k=3)

    # добавляем в список случайных картинок, нашу картинку
    random_wonders.append(random_wonder[0])

    # перемешиваем список
    random.shuffle(random_wonders)

    # отправляем нашу картинку и список картинок
    return (list(random_wonder),
            sorted(random_wonders, key=lambda x: random.random()))


# Получить случайную постройку
def get_random_building(type):
    # получаем случайную картинку
    random_building = random.choice(list(Buildings[type].items()))

    # получаем случайно ещё 3 случайных картинки
    random_buildings = random.sample(
        list(Buildings['Europe']) + list(Buildings['America'])
        + list(Buildings['Asia']) + list(Buildings['Africa']), k=4)

    # проверяем, если наш выбранная картинка есть в списке из 3-х случайных картинок
    while random_building in random_buildings:
        # если есть, меняем список, пока нашей картинки в нём не будет
        random_buildings = random.sample(
            list(Buildings['Europe']) + list(Buildings['America'])
            + list(Buildings['Asia']) + list(Buildings['Africa']), k=4)

    # добавляем в список случайных картинок, нашу картинку
    random_buildings.append(random_building[0])

    # перемешиваем список
    random.shuffle(random_buildings)

    # отправляем нашу картинку и список картинок
    return (list(random_building),
            sorted(random_buildings, key=lambda x: random.random()))


# Получить случайный город страны
def get_random_town(type):
    # получаем случайный город
    random_town = random.choice(list(countries['capitals'][type].items()))
    # получаем случайно ещё 3 города
    random_towns = random.sample(list(countries['capitals']['Europe'].values())
                                 + list(countries['capitals']['America'].values())
                                 + list(countries['capitals']['Asia'].values())
                                 + list(countries['capitals']['Africa'].values()), k=4)

    # проверяем, если наш город есть в списке из 3-х случайных городов
    while random_town[1] in random_towns:
        # если есть, меняем список, пока наш город в нём не будет
        random_towns = random.sample(list(countries['capitals'][type].values()), k=4)

    # добавляем в список случайных городов, наш город
    random_towns.append(random_town[1])

    # перемешиваем список
    random.shuffle(random_towns)

    # отправляем наш город, столицу и список городов
    return random_town, random_towns


@app.route('/post', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON,
# который отправила нам Алиса в запросе POST
def main():

    logging.info(f'Request: {request.json!r}')

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    # Отправляем request.json и response в функцию handle_dialog.
    # Она сформирует оставшиеся поля JSON, которые отвечают
    # непосредственно за ведение диалога
    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return jsonify(response)


# игра
def handle_dialog(req, res):
    # наши флаги
    global mod_eng, mod_flags, mod_towns, mod_type, mod_buildings, mod_wonders, type_mod, new

    # айди пользователя
    user_id = req['session']['user_id']

    try:

        # Если это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        if req['session']['new']:

            # нашa подсказка
            sessionStorage[user_id] = {}

            # сразу включаем флаги режима
            mod_type = True

            # просим его выбрать тип игры
            res['response']['text'] = 'Привет! Выбери тип игры! (Europe, America, Asia, Africa)'

            # выводим подсказки
            sessionStorage[user_id]['suggests'] = ["Europe", "America", "Asia", "Africa"]
            res['response']['buttons'] = get_suggests(user_id)

            return

        # Проверка на выбор типа и соответствующей логики
        if mod_type:

            # проверяем ответ и записываем выбранный режим:
            # режим европа
            if ('европа' in req['request']['original_utterance'].lower() or
                    'europe' in req['request']['original_utterance'].lower()):

                # записываем выбранный режим на английском
                type_mod = 'Europe'

            # режим америка
            elif ('америка' in req['request']['original_utterance'].lower() or
                  'america' in req['request']['original_utterance'].lower()):

                # записываем выбранный режим на английском
                type_mod = 'America'

            # режим африка
            elif ('африка' in req['request']['original_utterance'].lower() or
                  'africa' in req['request']['original_utterance'].lower()):

                # записываем выбранный режим на английском
                type_mod = 'Africa'

            # режим азия
            elif ('азия' in req['request']['original_utterance'].lower() or
                  'asia' in req['request']['original_utterance'].lower()):

                # записываем выбранный режим на английском
                type_mod = 'Asia'

            # если что-то написано не верно, просим его написать всё правильно
            else:

                # выводим текст
                res['response']['text'] = 'Выбери тип игры! (Europe, America, Asia, Africa)'

                # выводим подсказки
                sessionStorage[user_id]['suggests'] = ["Europe", "America", "Asia", "Africa"]
                res['response']['buttons'] = get_suggests(user_id)

                return

            # выключаем выбор типа
            mod_type = False

            # создаём новые подсказки
            sessionStorage[user_id]['suggests'] = ["Английские названия", "Флаги", "Столицы",
                                                   "Постройки", 'Чудеса Света']
            res['response']['buttons'] = get_suggests(user_id)

            # выводим текст
            res['response']['text'] = 'Выбирай режим игры!'

            return

        # записываем переменные для разных режимов:
        # для режима английские названия
        random_country_eng, random_country_rus, random_countries_rus = get_random_country_eng(
            type_mod if type_mod else 'Europe')

        # для режима флаги
        random_flag, random_countries_flags = get_random_flag(type_mod if type_mod else 'Europe')

        # для режима постройки
        random_building, random_buildings = get_random_building(type_mod if type_mod else 'Europe')

        # для режима чудеса света
        random_wonder, random_wonders = get_random_wonders()

        # для режима столицы
        random_cap, random_caps = get_random_town(type_mod if type_mod else 'Europe')

        # если выбрали режим английские названия
        if 'английские названия' in req['request']['original_utterance'].lower():

            # выключаем все другие режимы
            mod_towns = False
            mod_flags = False
            mod_buildings = False
            mod_wonders = False

            # включаем наш режим
            mod_eng = True

            # записываем в переменную страну на русском
            new = random_country_rus

            # пишем текст с объяснениями
            res['response']['text'] = "Я буду писать страны на английском, а ты пиши на русском"

            # и добавляем страну на английском к нашему тексту
            res['response']['text'] += f"\n {random_country_eng}"

            # изменяем наши подсказки, на страны на русском
            sessionStorage[user_id]['suggests'] = random_countries_rus
            res['response']['buttons'] = get_suggests(user_id)

            return

        # сообщаем об ошибке
        res['response']['text'] = "Произошла ошибка! Перезагрузите страницу!"
        res['response']['buttons'] = get_suggests(user_id)

        # если выбрали режим флаги
        if 'флаги' in req['request']['original_utterance'].lower():

            # выключаем все другие режимы
            mod_eng = False
            mod_towns = False
            mod_buildings = False
            mod_wonders = False

            # включаем наш режим
            mod_flags = True

            # записываем в переменную флаг
            new = random_flag[0]

            # пишем текст с объяснениями и картинку
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = "Я буду отображать флаг страны, а ты напишешь её название."
            res['response']['card']['image_id'] = random_flag[1]

            # изменяем наши подсказки, на названия стран
            sessionStorage[user_id]['suggests'] = random_countries_rus
            res['response']['buttons'] = get_suggests(user_id)

            return

        # если выбрали режим столицы
        if 'столицы' in req['request']['original_utterance'].lower():

            # выключаем все другие режимы
            mod_flags = False
            mod_eng = False
            mod_buildings = False
            mod_wonders = False

            # включаем наш режим
            mod_towns = True

            # записываем столицу
            new = random_cap[1]

            # пишем текст с объяснениями и город
            res['response']['text'] = "Я буду писать название страны, а ты напишешь название столицы."
            res['response']['text'] += f"\n {random_cap[0]}"

            # изменяем наши подсказки, на названия столиц
            sessionStorage[user_id]['suggests'] = random_caps
            res['response']['buttons'] = get_suggests(user_id)

            return

        # если выбрали режим постройки
        if 'постройки' in req['request']['original_utterance'].lower():

            # выключаем все другие режимы
            mod_eng = False
            mod_towns = False
            mod_flags = False
            mod_wonders = False

            # включаем наш режим
            mod_buildings = True

            # записываем постройку
            new = random_building[0]

            # пишем текст с объяснениями и выводим картинку
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = "Я буду отображать постройку, а ты напишешь её название."
            res['response']['card']['image_id'] = random_building[1]

            # изменяем наши подсказки, на названия столиц
            sessionStorage[user_id]['suggests'] = random_buildings
            res['response']['buttons'] = get_suggests(user_id)

            return

        # если выбрали режим чудеса света
        if 'чудеса света' in req['request']['original_utterance'].lower():

            # выключаем все другие режимы
            mod_eng = False
            mod_towns = False
            mod_flags = False
            mod_buildings = False

            # включаем наш режим
            mod_wonders = True

            # записываем постройку
            new = random_wonder[0]

            # пишем текст с объяснениями и выводим картинку
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = "Я буду отображать чудеса света, а ты напишешь её название."
            res['response']['card']['image_id'] = random_wonder[1]

            # изменяем наши подсказки, на названия столиц
            sessionStorage[user_id]['suggests'] = random_wonders
            res['response']['buttons'] = get_suggests(user_id)

            return

        # если игра уже началась
        if mod_eng:

            # выключаем все другие режимы
            mod_towns = False
            mod_flags = False
            mod_buildings = False
            mod_wonders = False

            # проверяем ответ
            if new in req['request']['original_utterance']:
                res['response']['text'] = 'Правильно!'
            else:
                res['response']['text'] = 'Неправильно!'

            # продолжаем игру
            res['response']['text'] += f"\n {random_country_eng}"

            # обновляем словарь
            sessionStorage[user_id]['suggests'] = random_countries_rus
            res['response']['buttons'] = get_suggests(user_id)

            # обновляем переменную
            new = random_country_rus

            return

        # если игра уже началась
        if mod_flags:

            # выключаем все другие режимы
            mod_towns = False
            mod_eng = False
            mod_buildings = False
            mod_wonders = False

            # делаем заготовку для картинки
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'

            # проверяем ответ
            if new in req['request']['original_utterance']:
                res['response']['card']['title'] = 'Правильно!'
            else:
                res['response']['card']['title'] = 'Неправильно!'

            # добавляем картинку
            res['response']['card']['image_id'] = random_flag[1]

            # обновляем словарь
            sessionStorage[user_id]['suggests'] = random_countries_flags
            res['response']['buttons'] = get_suggests(user_id)

            # обновляем переменную
            new = random_flag[0]

            return

        # если игра уже началась
        if mod_towns:

            # выключаем все другие режимы
            mod_eng = False
            mod_flags = False
            mod_buildings = False
            mod_wonders = False

            # проверяем ответ
            if new in req['request']['original_utterance']:
                res['response']['text'] = 'Правильно!'
            else:
                res['response']['text'] = 'Неправильно!'

            # добавляем новую страну
            res['response']['text'] += f"\n {random_cap[0]}"

            # обновляем словарь
            sessionStorage[user_id]['suggests'] = random_caps
            res['response']['buttons'] = get_suggests(user_id)

            # обновляем переменную
            new = random_cap[1]

            return

        res['response']['text'] = "Произошла ошибка! Перезагрузите страницу!"
        res['response']['buttons'] = get_suggests(user_id)

        # если игра уже началась
        if mod_buildings:

            # выключаем все другие режимы
            mod_towns = False
            mod_flags = False
            mod_eng = False
            mod_wonders = False

            # делаем заготовку для картинки
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'

            # проверяем ответ
            if new in req['request']['original_utterance']:
                res['response']['card']['title'] = 'Правильно!'
            else:
                res['response']['card']['title'] = 'Неправильно!'

            # добавляем новую постройку
            res['response']['card']['image_id'] = random_building[1]

            # обновляем словарь
            sessionStorage[user_id]['suggests'] = random_buildings
            res['response']['buttons'] = get_suggests(user_id)

            # обновляем переменную
            new = random_building[0]

            return

        # если игра уже началась
        if mod_wonders:

            # выключаем все другие режимы
            mod_towns = False
            mod_flags = False
            mod_eng = False
            mod_buildings = False

            # делаем заготовку для картинки
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'

            # проверяем ответ
            if new in req['request']['original_utterance']:
                res['response']['card']['title'] = 'Правильно!'
            else:
                res['response']['card']['title'] = 'Неправильно!'

            # добавляем новую постройку
            res['response']['card']['image_id'] = random_wonder[1]

            # обновляем словарь
            sessionStorage[user_id]['suggests'] = random_wonders
            res['response']['buttons'] = get_suggests(user_id)

            # обновляем переменную
            new = random_wonder[0]

            return

        return

    # если выводит ошибку
    except ExceptionGroup as err:
        # то сообщаем о ней
        res['response']['text'] = f"Ошибка {err}! Попробуйте снова!"

        return


# Функция обновляет словарь
def get_suggests(user_id):

    # копируем в перменную словарь
    session = sessionStorage[user_id]

    # Выбираем подсказки из массива.
    suggests = [
        {
            'title': suggest,
            'hide': True
        }
        for suggest in session['suggests'][:]
    ]

    return suggests


# запускаем код
if __name__ == '__main__':
    app.run(host='0.0.0.0')
