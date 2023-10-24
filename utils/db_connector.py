import time
import uuid
import logging
from typing import Union, Type
from pymongo import MongoClient


class MongodbAPI:
    def __init__(self, database_uri, database_name):
        self.database_name = database_name
        self.client = MongoClient(database_uri)

    def check_user(self, user_id) -> Union[bool]:
        table = self.client[self.database_name]['users']
        try:
            if table.find_one({"id": user_id}) is None:
                return False
            return True
        except Exception as e:
            logging.error(f'[check_user] error text: {e}')

    def get_user(self, user_id) -> Union[dict]:
        table = self.client[self.database_name]['users']
        try:
            return table.find_one({"id": user_id})
        except Exception as e:
            logging.error(f'[get_user] error text: {e}')

    def create_user(self, email: str, user_id: str = None, limits: int = 100):
        table = self.client[self.database_name]['users']
        timestamp = int(time.time())
        user_id = self.generate_short_uuid() if user_id is None else user_id
        try:
            item = {
                "id": user_id,
                "email": email,
                "notifications": {
                    "limits": limits,
                    "notifications_data": []
                },
                "created_at": timestamp
            }
            table.insert_one(item)
        except Exception as e:
            logging.error(f'[create_user] error text: {e}')

    def new_notification(self, user_id, new_data):
        table = self.client[self.database_name]['users']
        try:
            user = self.get_user(user_id)

            if user:
                notification_id = self.generate_short_uuid()
                timestamp = int(time.time())
                new_data.update({"id": notification_id, 'timestamp': timestamp, "is_new": True})
                current_data = user["notifications"]["notifications_data"]
                limits = user["notifications"]["limits"]
                current_data.insert(0, new_data)
                if len(current_data) > limits:
                    current_data = current_data[:limits]
                table.update_one({"id": user_id}, {"$set": {"notifications.notifications_data": current_data}})
        except Exception as e:
            logging.error(f'[new_notification] error text: {e}')

    def get_slice_user_notifications(self, user_id, skip, limit):
        try:
            user = self.get_user(user_id)
            if user:
                notifications = user["notifications"]["notifications_data"]
                data = {
                    "elements": len(notifications),
                    "new": len(self._get_new_notifications_in_data(notifications)),
                    "request": {
                        "user_id": user_id,
                        "skip": skip,
                        "limit": limit
                    },
                    "list": notifications[skip:limit]
                }
                return data
            else:
                return None
        except Exception as e:
            logging.error(f'[get_slice_user_notifications] error text: {e}')

    def read_notification(self, user_id, notification_id) -> Union[bool, None]:
        table = self.client[self.database_name]['users']
        try:
            user = self.get_user(user_id)
            if user:
                data = user["notifications"]["notifications_data"]
                current_data = self._read_notifications_by_id(data, notification_id)
                if current_data is None:
                    return None
                table.update_one({"id": user_id}, {"$set": {"notifications.notifications_data": current_data}})
                return True
            else:
                return False
        except Exception as e:
            logging.error(f'[read_notification] error text: {e}')


    @staticmethod
    def _read_notifications_by_id(data: list, notification_id) -> Union[list, None]:
        for notification in data:
            if notification.get('id') == notification_id:
                notification['is_new'] = False
                return data
        return None

    @staticmethod
    def _get_new_notifications_in_data(data: list) -> Union[list]:
        temp = list()
        for notification in data:
            if notification.get('is_new') is True:
                temp.append(notification)
        return temp

    @staticmethod
    def generate_short_uuid() -> Union[str]:
        new_uuid = uuid.uuid4()
        short_uuid = str(new_uuid).replace("-", "")
        return short_uuid[:24]
