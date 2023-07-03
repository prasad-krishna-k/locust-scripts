import json

from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 5)  # Time between consecutive requests in seconds

    @task
    def my_task(self):
        with open("sds3.solution.prevalent.ai_Archive [23-07-03 16-28-14].har",
                  "r") as har_file:  # Replace with the path to your HAR file
            har_data = json.load(har_file)
        entries = har_data["log"]["entries"]
        for entry in entries:
            request = entry["request"]
            url = request["url"]
            method = request["method"]
            headers = {}
            for header in request["headers"]:
                headers[header["name"]] = header["value"]
            payload = None
            if "postData" in request:
                payload = request["postData"]["text"]
            self.client.request(method, url, headers=headers, data=payload)
