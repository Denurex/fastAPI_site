from datetime import date

from sqlalchemy import Boolean, Column, Identity, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    # seq = Sequence('user_id_seq', metadata = Base.metadata, start=1)
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    booking = relationship('Bookings', back_populates='user')

    def __str__(self):
        return f'User: {self.email}'