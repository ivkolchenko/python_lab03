import pytest

from src.object_catalog import Auditorium, InvalidEntityError


def test_creating_valid_entity():
    auditorium = Auditorium(
        uid="1",
        name="Name",
        category="first",
        date="2026",
        number=101,
        size="medium"
    )

    assert auditorium.__dict__ == {
        "uid": "1",
        "name": "Name",
        "category": "first",
        "date": "2026",
        "number": 101,
        "size": "medium"
    }

def test_creating_invalid_entity():
    with pytest.raises(InvalidEntityError):
        Auditorium(uid="1")

    with pytest.raises(InvalidEntityError):
        Auditorium(
            uid="1",
            name="Name",
            category="first",
            date="2026",
            number=-1,
            size="medium"
        )

    with pytest.raises(InvalidEntityError):
        Auditorium(
            uid="",
            name="Name",
            category="first",
            date="2026",
            number=101,
            size="medium",
        )

    with pytest.raises(InvalidEntityError):
        Auditorium(
            uid="1",
            name="Name",
            category="first",
            date="1-1-2026",
            number=101,
            size="medium"
        )
