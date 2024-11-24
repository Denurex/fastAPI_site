from datetime import date

from sqlalchemy import and_, func, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects import postgresql

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Rooms
from app.logger import logger


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        WITH booking_count AS (
            SELECT COUNT(*) AS count_bookings
            FROM bookings AS b
            WHERE b.room_id = 1
              AND (
                  -- Первый случай: бронирование начинается до или во время диапазона и заканчивается после диапазона
                  (b.date_from <= '2023-06-30' AND b.date_to >= '2023-06-15')
              )
        )
        """
        try:
            async with async_session_maker() as session:
                booking_count_subquery = (
                    select(func.count().label("count_bookings"))
                    .select_from(Bookings)
                    .where(
                        Bookings.room_id == room_id,
                        and_(
                            Bookings.date_from
                            <= date_to,  # Дата начала бронирования до конца диапазона
                            Bookings.date_to
                            >= date_from,  # Дата окончания бронирования после начала диапазона
                        ),
                    )
                    .scalar_subquery()  # Подзапрос для использования в основном запросе
                )

                # compiled_query = booking_count_subquery.compile(engine,
                #                                                 compile_kwargs={"literal_binds": True})
                # print(str(compiled_query))

                """
                SELECT r.quantity - bc.count_bookings
                FROM rooms AS r
                JOIN booking_count bc ON r.id = 1
                WHERE r.id = 1;
                """

                available_rooms_query = select(
                    Rooms.quantity - booking_count_subquery
                ).where(Rooms.id == room_id)

                # Выполнение запроса
                result = await session.execute(available_rooms_query)
                available_rooms: int = result.scalar()  # Получение одного значения

                print(available_rooms)

                if available_rooms <= 0:
                    return None

                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e,SQLAlchemyError):
                msg = 'DB Exc: Cannot add booking'
            else:
                msg = 'Unknow Exc: Cannot add booking'

            extra = {
                'user_id': user_id,
                'room_id': room_id,
                'date_from': date_from,
                'date_to': date_to
            }

            logger.error(msg,extra=extra,exc_info=True)