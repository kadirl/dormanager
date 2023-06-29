from database import database
from database.countries import CountryCollection, Country, City


# country = Country(
#     name='Kazakhstan',
#     cities=[
#         City(
#             name='Shymkent',
#             telegram_chat_id='-1001887851233'
#         )
#     ]
# )
#
# id = CountryCollection.create_country(country)
# print(id)
#
# cities = CountryCollection.get_cities_by_country('kazakhstan')
# print(cities)

for i in range(5):
    result = CountryCollection.insert_city('kazakhstan', City(
        name='new shymkent '+str(i),
        telegram_chat_id='-1001887851233'
    ))

    print(i, result)