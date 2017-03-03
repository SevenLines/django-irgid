from random import random, randint

from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    @task(2)
    def index(self):
        self.client.get("/")

    @task(10)
    def excursion(self):
        self.client.get("/excursions/{}/".format(randint(10,100)))


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
