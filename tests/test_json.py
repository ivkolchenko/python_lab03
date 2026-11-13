import pytest

from src.object_catalog import (Auditorium, Catalog, catalog_save, catalog_load,
                                CorruptedFileError, UnsupportedVersionError)


def test_round_trip_json(tmp_path):
    """Тест полного цикла JSON: загрузка каталога, его выгрузка и сравнение эквивалентности"""
    path = tmp_path / "test.json"

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
    catalog.add(auditorium1)
    catalog.add(auditorium2)
    catalog.add(auditorium3)

    catalog_save(catalog, path)

    assert catalog_load(path).__dict__ == catalog.__dict__


def test_broken_json(tmp_path):
    """Тест сломанных JSON, и JSON с неподдерживаемым форматом"""
    input_path_01 = tmp_path / "test01.json"
    input_path_02 = tmp_path / "test02.json"

    input_path_01.write_text(
        "... --- ...",
        encoding="utf-8"
    )

    input_path_02.write_text(
        "{\"format_version\": 1, \"container\": "
        "{\"1\": {\"uid\": \"1\", \"name\": \"Name\"}}}",
        encoding="utf-8"
    )

    with pytest.raises(CorruptedFileError):
        catalog_load(input_path_01)

    with pytest.raises(UnsupportedVersionError):
        catalog_load(input_path_02)


def test_load_catalog(tmp_path):
    """Тест загрузки сломанного каталога. Существующий каталог не должен измениться"""
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
    catalog.add(auditorium1)
    catalog.add(auditorium2)
    catalog.add(auditorium3)

    input_path = tmp_path / "test.json"
    input_path.write_text(
        "{\"format_version\": 1, \"container\": "
        "{\"1\": {\"uid\": \"1\", \"name\": \"Name\"}}}",
        encoding="utf-8"
    )

    try:
        catalog = catalog_load(input_path)
    except UnsupportedVersionError:
        pass

    auditorium_list = [auditorium1, auditorium2, auditorium3]
    for n, auditorium in enumerate(catalog):
        assert auditorium == auditorium_list[n]
