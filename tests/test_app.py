import email
import unittest
import os
from urllib import response

os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
    
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        self.client.post("/api/timeline_post", data=({'name':'A','email':'a@g.com','content':'test'}))
        response = self.client.get("/api/timeline_post")
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["content"] == "test"

        self.client.delete("/api/timeline_post", data=({'name':'A'}))
        response = self.client.get("/api/timeline_post")
        json = response.get_json()
        assert len(json["timeline_posts"]) == 0
    
    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data=({'email':'john@example','content':'Hello World'}))
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html
        
        
        response = self.client.post("/api/timeline_post", data=({'name':'John Doe','email':'john@example','content':''}))
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html
        
        response = self.client.post("/api/timeline_post", data=({'name':'John Doe','email':'not-an-email','content':'Hello World'}))
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
        
