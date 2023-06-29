import random
from bson import ObjectId

from database.room import Room, RoomRating, RoomCollection
from database.user import User, UserCollection

rooms = []

print('creating rooms')

for i in range(10, 20):
    room = Room(
        number=i
    )

    rooms.append(room)

    print(RoomCollection.create_room(room))

print('gettings rooms by number')
print(RoomCollection.get_room_by_number(12))
print(RoomCollection.get_room_by_number(14))
print(RoomCollection.get_room_by_number(15))
print(RoomCollection.get_room_by_number(48))

print('getting all rooms')
print(RoomCollection.get_all_rooms())


for room in rooms:
    room_number = room.number

    for i in range(5):
        rating = random.randint(1, 5)
        rating_instance = RoomRating(
            rating=rating,
            text='test',
            sender_id=ObjectId('649da63f00962d23993e5d68')
        )
        RoomCollection.add_room_rating(room_number, rating_instance)

print('getting all rooms')
print(RoomCollection.get_all_rooms())

print('getting all rooms rated')
print(RoomCollection.get_all_rooms())


