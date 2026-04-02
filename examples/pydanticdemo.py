from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str = "Aditya Verma"
    signup_ts: datetime | None = None
    friends: list[int] = []


external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)  # use of kwargs
print(user)
# > User id=123 name='Aditya Verma' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123
#
# OUTPUT
# id=1 name='Aditya Verma' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3] 123
