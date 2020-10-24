from locust import HttpLocust, TaskSet, task, between
from random import randint
from datetime import datetime


class TestBehaviour(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    user_payload = {"name": "user{number}".format(number=randint(1, 100000000000))}
    item_payload = {
        "name": "item{number}".format(number=randint(1, 100)),
        "init_bid": 1,
        "currency": "EUR",
        "created_date": "2020-04-22T18:25:59.056Z",
        "bidding_enddate": "2020-04-22T18:25:59.056Z",
    }

    @task(1)
    def create_user(self):
        user = self.client.post("users", json=self.user_payload)

    @task(2)
    def create_item(self):
        item = self.client.post("items", json=self.item_payload)

    @task(3)
    def create_event(self):
        event_payload = {
            "item_id": "UUID",
            "user_id": "UUID",
            "value": 30,
            "bid_date": "2020-04-22T18:37:57.930Z",
            "created_date": "2020-04-22T18:37:57.930Z",
            "client": "web",
        }
        event = self.client.post("events", json=event_payload)

    @task(4)
    def create_user_items_events(self):
        # Create user
        user = self.client.post("users", json=self.user_payload)
        user_id = user.json()["id"]
        # Create item
        item_ids = []
        for item_idx in range(1, 3):
            item_payload = {
                "name": "item{number}".format(number=randint(1, 100)),
                "init_bid": 13,
                "currency": "EUR",
                "created_date": "2020-04-22T18:25:59.056Z",
                "bidding_enddate": "2020-04-22T18:25:59.056Z",
            }
            item = self.client.post("items", json=item_payload)
            item_ids.append(item.json()["id"])

        # Create events
        for item_id in item_ids:
            event_payload = {
                "item_id": item_id,
                "user_id": user_id,
                "value": randint(50, 10000),
                "bid_date": "2020-04-22T18:37:57.930Z",
                "created_date": "2020-04-22T18:37:57.930Z",
                "client": "web",
            }
            event = self.client.post("events", json=event_payload)

        # Get user items
        self.client.get("users/items/{user_id}".format(user_id=user_id))

    @task(5)
    def get_item_bids(self):
        item = self.client.post("items", json=self.item_payload)
        print(item.json()["id"])
        for user_number in range(0, 100):
            user = self.client.post("users", json=self.user_payload)
            event_payload = {
                "item_id": item.json()["id"],
                "user_id": user.json()["id"],
                "value": randint(50, 10000),
                "bid_date": "2020-04-22T18:37:57.930Z",
                "created_date": "2020-04-22T18:37:57.930Z",
                "client": "web",
            }
            event = self.client.post("events", json=event_payload)

        # Get bids for this item
        bids = self.client.get("item/bids/{item_id}".format(item_id=item.json()["id"]))


class UserBahavior_1(HttpLocust):
    task_set = TestBehaviour
    min_wait = 5000
    max_wait = 9000
