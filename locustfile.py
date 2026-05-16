import random
from locust import HttpUser, task, between
from locust.exception import StopUser

class TelemetryUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        username = f"load_user_{random.randint(1000000, 9999999)}"
        
        response_user = self.client.post("/api/v1/users/register", json={"username": username})
        
        if response_user.status_code == 201:
            self.user_id = response_user.json()["id"]
            
            self.device_id = f"sensor-{random.randint(10000, 99999)}"
            
            response_device = self.client.post("/api/v1/devices/register", json={
                "id": self.device_id,
                "name": "Тестовый датчик",
                "user_id": self.user_id
            })
            
            if response_device.status_code != 201:
                raise StopUser()
        else:
            raise StopUser()

    @task(10)
    def send_telemetry(self):
        if hasattr(self, 'device_id'):
            payload = {
                "x": random.uniform(-10.0, 10.0),
                "y": random.uniform(-10.0, 10.0),
                "z": random.uniform(-10.0, 10.0)
            }
            self.client.post(f"/api/v1/stats/{self.device_id}", json=payload, name="/api/v1/stats/{device_id}")

    @task(1)
    def request_analytics(self):
        if hasattr(self, 'user_id'):
            self.client.post(f"/api/v1/analytics/users/{self.user_id}", name="/api/v1/analytics/users/{user_id}")