from database.user import User, UserCollection


print(UserCollection.get_all_users())
print(UserCollection.get_regular_notification_allowed_users())
print(UserCollection.get_events_notification_allowed_users())
print(UserCollection.get_offers_notification_allowed_users())
