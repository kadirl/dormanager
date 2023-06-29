from database.user import User, UserCollection


id = UserCollection.create_user(User(
    tg_id='testtest',
    name='Кадир Кадир',
    room=33
))

print(id)

print(UserCollection.get_user_by_id(id))