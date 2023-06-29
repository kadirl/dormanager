# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
#
#
# def get_cities(country: str):
#     builder = ReplyKeyboardBuilder()
#     cities = CountryCollection.get_cities_by_country(country)
#
#     for city in cities:
#         builder.add(KeyboardButton(text=city.name))
#     builder.adjust(2)
#
#     builder.row(
#         KeyboardButton(text='{NO CITY}')
#     )
#
#     return builder.as_markup(resize_keyboard=True)
#
# def get_position_form_link():
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(
#             text='{FORM LINK}',
#             url='https://www.google.com'
#         )]
#     ])
#
# def get_back_button():
#     return ReplyKeyboardMarkup(keyboard=[
#         [KeyboardButton(text='{BACK}')]
#     ])
#
# def get_gender():
#     return ReplyKeyboardMarkup(
#         resize_keyboard=True,
#         input_field_placeholder='What is your gender?',
#         keyboard=[
#             [KeyboardButton(text='male')],
#             [KeyboardButton(text='female')]
#         ]
#     )
