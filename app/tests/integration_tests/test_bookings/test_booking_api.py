import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,booked_rooms,status_code",
    [
        *[(4, "2030-05-01", "2030-05-15", i, 201) for i in range(3, 11)],
        *[(4, "2030-05-01", "2030-05-15", 10, 409)] * 2,
    ],
)
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == booked_rooms


async def test_get_and_delete_bookings(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) != 0

    for booking in response.json():
        url = "/bookings/" + str(booking["id"])
        response = await authenticated_ac.delete(url)
    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == 0
    