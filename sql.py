import sqlalchemy as sa


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from common import app

db: SQLAlchemy = SQLAlchemy(app)


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False)
    password = sa.Column(sa.String(80), unique=True, nullable=False)
    blogs = db.relationship("Blog", backref="user")


class Blog(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(80), unique=True, nullable=False)
    desc = sa.Column(sa.Text)
    datetime = sa.Column(sa.DateTime)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"))


try:
    with app.app_context():
        db.create_all()

        # db.session.add(User(id=1, name="admin@admin.com", password="admin"))
        # db.session.commit()

except BaseException as e:
    print(e)

#########################################


def create_blog(title, desc, uid):
    obj = Blog(
        title=title,
        desc=desc,
        user_id=uid,
        datetime=datetime.now(),
    )
    db.session.add(obj)
    db.session.commit()


def get_blogs():
    return Blog.query.all()


def get_users():
    return User.query.all()


def get_blog_by_id(id):
    return Blog.query.filter_by(id=id).first()


def validate_user(email, password):
    users = User.query.filter_by(email=email, password=password).all()
    if len(users) == 1:
        return True, users[0].id
    else:
        return False, None
