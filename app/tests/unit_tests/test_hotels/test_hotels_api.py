

from datetime import date
from httpx import AsyncClient

import pytest

@pytest.mark.parametrize("location,date_from,date_to,status_code", [
    ("Алтай", "2020-05-05", "2020-05-05", 200),
    ("Алтай", "2020-05-05", "2020-05-04", 400),
    ("Алтай", "2020-05-05", "2020-07-05", 400),
    ("Алтай", "2020-05-05", "2020-05-25", 200),
])
async def test_get_hotels_by_location_and_time(
        location: str,
        date_from: str,
        date_to: str,
        status_code: int,
        ac: AsyncClient,
):
    response = await ac.get("/hotels", params={
        "location": location,
        "date_from": date_from,
        "date_to": date_to,
    })
    assert response.status_code == status_code
