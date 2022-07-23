import unittest
from playhouse.shortcuts import model_to_dict

from pymysql import Time
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(name='John Doe', email='jd@example.com', content='Hello World, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jd2@example.com', content='Hello World :3!')
        assert second_post.id ==2
        
        i = 1
        for p in TimelinePost.select().order_by(TimelinePost.created_at.asc()):
            assert p.id == i
            i += 1