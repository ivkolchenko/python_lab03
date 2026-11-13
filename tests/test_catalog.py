import pytest

from src.object_catalog import Catalog, Auditorium, ObjectNotFoundError, IdDuplicateError


def test_catalog_methods():
    """Тест методов Catalog get() и add()"""
    catalog = Catalog()
    auditorium = Auditorium(
        uid="1",
        name="Name",
        category="first",
        date="2026",
        number=101,
        size="medium"
    )

    catalog.add(auditorium)
    assert catalog.get("1").__dict__ == {
        "uid": "1",
        "name": "Name",
        "category": "first",
        "date": "2026",
        "number": 101,
        "size": "medium"
    }

    with pytest.raises(ObjectNotFoundError):
        catalog.get("2")


def test_catalog_duplicate_id():
    """Тест ошибки дубликата id сущности при добавлении в каталог"""
    auditorium1 = Auditorium(
        uid="1",
        name="1",
        category="first",
        date="2026",
        number=101,
        size="medium"
    )
    auditorium2 = Auditorium(
        uid="1",
        name="2",
        category="first",
        date="2026",
        number=101,
        size="medium"
    )
    catalog = Catalog()

    with pytest.raises(IdDuplicateError):
        catalog.add(auditorium1)
        catalog.add(auditorium2)


def test_catalog_find():
    """Тест поиска по имени и категории"""
    auditorium1 = Auditorium(
        uid="1",
        name="ABC",
        category="first",
        date="2026",
        number=101,
        size="medium"
    )
    auditorium2 = Auditorium(
        uid="2",
        name="abcd",
        category="first",
        date="2026",
        number=101,
        size="medium"
    )
    auditorium3 = Auditorium(
        uid="3",
        name="bCd",
        category="second",
        date="2026",
        number=101,
        size="medium"
    )

    catalog = Catalog()
    catalog.add(auditorium1)
    catalog.add(auditorium2)
    catalog.add(auditorium3)

    assert catalog.find_by_name("abc") == [auditorium1, auditorium2]
    assert catalog.find_by_name("bcd") == [auditorium2, auditorium3]
    assert catalog.find_by_name("name") == []

    assert catalog.find_by_category("first") == [auditorium1, auditorium2]
    assert catalog.find_by_category("second") == [auditorium3]
    assert catalog.find_by_category("third") == []


def test_catalog_iteration():
    """Тест итерации Catalog: она идет по лексикографическому возрастанию id"""
    auditorium1 = Auditorium(
        uid="1",
        name="Name",
        category="first",
        date="2026",
        number=101,
        size="medium"
    )
    auditorium2 = Auditorium(
        uid="2",
        name="Name",
        category="first",
        date="2026",
        number=101,
        size="medium"
    )
    auditorium3 = Auditorium(
        uid="3",
        name="Name",
        category="second",
        date="2026",
        number=101,
        size="medium"
    )

    catalog = Catalog()
    catalog.add(auditorium3)
    catalog.add(auditorium1)
    catalog.add(auditorium2)

    iteration = iter(catalog)

    assert next(iteration) == auditorium1
    assert next(iteration) == auditorium2
    assert next(iteration) == auditorium3
