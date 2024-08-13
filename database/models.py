from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base, str_uniq, int_pk, score_landmark

class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    password: Mapped[str] = mapped_column(nullable=False)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, username={self.username})")

    def __repr__(self):
        return str(self)

class Score(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    result: Mapped[score_landmark]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id})")

    def __repr__(self):
        return str(self)