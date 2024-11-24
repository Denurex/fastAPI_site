from datetime import date

from sqlalchemy import Row, and_, func, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels, Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def search_for_hotels(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:

            """
            WITH booking_count AS (
                SELECT 
                    b.room_id,
                    COUNT(*) AS count_bookings
                FROM bookings AS b
                WHERE 
                    (b.date_from <= '2023-06-30' AND b.date_to >= '2023-06-15')
                GROUP BY b.room_id
            	)
            """
            booking_count = (
                select(
                    Bookings.room_id,
                    func.count().label('count_bookings')
                )
                .where(
                    and_(
                        Bookings.date_from <= date_to,
                        Bookings.date_to >= date_from
                    )
                )
                .group_by(Bookings.room_id)
                .cte("booking_count")  # Создание CTE
            )

            """
            SELECT SUM(r.quantity) AS total_quantity,
               		SUM(r.quantity - COALESCE(bc.count_bookings, 0)) AS total_available_rooms,
                	h.location,
                	h.name AS hotel_name
            FROM rooms AS r
            LEFT JOIN booking_count AS bc ON r.id = bc.room_id
            JOIN hotels AS h ON h.id = r.hotel_id
            WHERE h.location LIKE '%Алтай%'
            GROUP BY h.location, h.name;
            """
            # Основной запрос
            query = (
                select(
                    func.sum(Rooms.quantity).label('total_quantity'),
                    func.sum(Rooms.quantity - func.coalesce(booking_count.c.count_bookings, 0)).label(
                        'total_available_rooms'),
                    Hotels.location,
                    Hotels.name.label('hotel_name'),
                    Hotels.id,
                    Hotels.image_id
                )
                .select_from(Rooms)
                .outerjoin(booking_count, Rooms.id == booking_count.c.room_id)  # Используем outer join для CTE
                .join(Hotels, Rooms.hotel_id == Hotels.id)
                .where(Hotels.location.like(f'%{location}%'))
                .group_by(Hotels.location, Hotels.name, Hotels.id)
            )

            result = await session.execute(query)
            hotels_as_dicts = [dict(row._mapping) if isinstance(row, Row) else row for row in result.all()]
            return hotels_as_dicts
            # return result.all()


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def search_for_rooms(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:

            """
            WITH booking_count AS (
                SELECT 
                    b.room_id,
                    COUNT(*) AS count_bookings
                FROM bookings AS b
                WHERE (b.date_from <= '2023-06-30' AND b.date_to >= '2023-06-15')
                GROUP BY b.room_id)
            """
            booking_count = (
                select(
                    Bookings.room_id,
                    func.count().label('count_bookings')
                )
                .where(
                    and_(
                        Bookings.date_from <= date_to,
                        Bookings.date_to >= date_from
                    )
                )
                .group_by(Bookings.room_id)
                .cte("booking_count")  # Создание CTE
            )

            """
            SELECT r.quantity, r.name,
                   r.quantity - COALESCE(bc.count_bookings, 0) AS available_rooms,
                   h.location,
                   r.name,
                   r.price,
                   r.services,
                   r.description
            FROM rooms AS r
            LEFT JOIN booking_count AS bc ON r.id = bc.room_id
            JOIN hotels AS h ON h.id = r.hotel_id
            WHERE h.id =1;
            """

            # Основной запрос
            query = (
                select(
                    Rooms.quantity,
                    (Rooms.quantity - func.coalesce(booking_count.c.count_bookings, 0)).label('available_rooms'),
                    Rooms.name,
                    Rooms.price,
                    Rooms.services,
                    Rooms.description
                )
                .select_from(Rooms)
                .outerjoin(booking_count, Rooms.id == booking_count.c.room_id)  # Используем outer join для CTE
                .join(Hotels, Rooms.hotel_id == Hotels.id)
                .where(Hotels.id == hotel_id)
            )

            result = await session.execute(query)

            # for hotel in hotels_data:
            #     print(hotel)
            return result.all()