import sqlite3
from datetime import datetime

from common import app


def get_conn():
    return sqlite3.connect("instance/data2.sqlite")


try:
    conn = get_conn()
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS user(
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        VARCHAR(80),
            email       VARCHAR(120),
            password    VARCHAR(80)
        );
    """
    )

    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS blog(
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            title           VARCHAR(80),
            desc            TEXT,
            datetime        TEXT,
            user_id         INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id)
        );
    """
    )

    conn.commit()
except BaseException as e:
    print(e)


#########################################
class User:
    def __init__(self, e) -> None:
        id, name, email, password = e
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    # @property
    # def blogs(self):
    #     conn = get_conn()
    #     objs = conn.execute(
    #         "SELECT * FROM blog WHERE user_id=?",
    #         (self.id,),
    #     )
    #     objs = list(map(lambda e: Blog(*e), objs))
    #     return objs


class Blog:
    def __init__(self, e) -> None:
        (
            id,
            title,
            desc,
            datetime,
            user_id,
        ) = e
        self.id = id
        self.title = title
        self.desc = desc
        self.datetime = datetime
        self.user_id = user_id

    @property
    def user(self):
        print(self.user_id, flush=True)
        conn = get_conn()
        objs = conn.execute(
            "SELECT * FROM user WHERE id=?",
            (self.user_id,),
        )
        objs = list(map(lambda e: User(e), objs))
        print(objs)
        return objs[0]


#########################################


def create_user(name, email, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        f"""
    INSERT INTO user(name, email, password)
    VALUES (?, ?, ?)
    """,
        (name, email, password),
    )
    cur.close()
    conn.commit()


def create_blog(title, desc, uid, dt=None):
    conn = get_conn()
    cur = conn.cursor()
    if dt is None:
        dt = datetime.now()
    cur.execute(
        f"""
    INSERT INTO blog(title, desc, datetime, user_id)
    VALUES (?, ?, ?, ?)
    """,
        (title, desc, dt.isoformat(), uid),
    )
    cur.close()
    conn.commit()


def get_blogs():
    conn = get_conn()
    objs = conn.execute(
        "SELECT * FROM blog",
    )
    objs = list(map(lambda e: Blog(e), objs))
    return objs


def get_users():
    conn = get_conn()
    objs = conn.execute(
        "SELECT * FROM user",
    )
    objs = list(map(lambda e: User(e), objs))
    return objs


def get_blog_by_id(id):
    conn = get_conn()
    obj = conn.execute(f"SELECT * FROM blog WHERE id=?", (id,))
    return Blog(obj.fetchall()[0])


def validate_user(email, password):
    conn = get_conn()
    objs = conn.execute(
        """
        SELECT * FROM user
        WHERE email=? AND password=?
        """,
        (email, password),
    )
    if objs.arraysize == 1:
        return True, User(objs.fetchall()[0])
    else:
        return False, None
