import random
from datetime import datetime, timedelta
from tqdm import tqdm
from faker import Faker

from common import app
from sql_raw import create_user, create_blog

fake = Faker()

with app.app_context():
    # for i in tqdm(range(100)):
    #     obj = create_user(
    #         name=fake.name(),
    #         email=fake.email(),
    #         password=fake.password(8),
    #     )

    for i in tqdm(range(100)):
        obj = create_blog(
            title=fake.name(),
            desc=fake.paragraph(),
            dt=(datetime.now() - timedelta(days=int(random.random() * 1000))),
            uid=int(random.random() * 100) + 1,
        )
