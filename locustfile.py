"""
Simple load testing file for Locust.
Tests the FastAPI prediction endpoint.
"""
from locust import HttpUser, task, between
import random

class RPSUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def predict_image(self):
        """Test prediction endpoint"""
        # Simulate sending an image
        files = {
            'file': ('test.jpg', b'fake_image_data', 'image/jpeg')
        }
        with self.client.post("/predict", files=files, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(1)
    def check_uptime(self):
        """Test uptime endpoint"""
        self.client.get("/uptime")
    
    @task(1)
    def check_health(self):
        """Test health check"""
        self.client.get("/")
