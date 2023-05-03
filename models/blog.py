import datetime as dt
import uuid


class Blog:
    def __init__(self, title, desc, datetime, uid, id=None):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.desc = desc

        if isinstance(datetime, list):
            datetime = dt.datetime(*datetime)

        self.datetime = datetime
        self.uid = uid

    def __str__(self) -> str:
        return f"<Blog {self.id} ({self.title})>"

    def __repr__(self) -> str:
        return str(self)

    def to_dict(self):
        d = self.datetime
        return {
            "id": self.id,
            "title": self.title,
            "desc": self.desc,
            "datetime": [d.year, d.month, d.day, d.hour, d.minute, d.second],
            "uid": self.uid,
        }
