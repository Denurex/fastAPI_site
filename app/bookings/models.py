from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Bookings(Base):
    __tablename__ = 'bookings'

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey('rooms.id'))
    user_id = Column(ForeignKey('users.id'))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer)
    tottal_cost = Column(Integer)
    tital_days = Column(Integer)

    user = relationship("Users", back_populates='booking')
    room = relationship("Rooms", back_populates='booking')

    def __str__(self):
        return f'Booking {self.id}'