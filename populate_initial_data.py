import random
from datetime import datetime, timedelta

from faker import Faker

from common import app
from sql import Blog, User, db

fake = Faker()

with app.app_context():
    for i in range(100):
        obj = User(
            name=fake.name(),
            email=fake.email(),
            password=fake.password(8),
        )
        db.session.add(obj)

    for i in range(100):
        obj = Blog(
            title=fake.name(),
            desc=fake.paragraph(),
            datetime=(datetime.now() - timedelta(days=int(random.random() * 1000))),
            user_id=int(random.random() * 100) + 1,
        )
        db.session.add(obj)

    db.session.commit()
