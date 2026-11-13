from src.object_catalog.models import Catalog, Auditorium
from src.object_catalog.errors import *

import json

def catalog_save(catalog: Catalog, path: str) -> None:
    """Сохранение каталога в json"""
    try:
        with (open(path, mode="r+") as file):
            legacy = json.load(file)
            result: dict[str, int | dict[str, dict[str, str | int]]] = {
                "format_version": legacy["format_version"],
                "container": {}
            }

            if len(legacy["container"]) != 0 and len(catalog.container) != 0 and \
                    next(iter(legacy["container"].values())).keys() != \
                    next(iter(catalog.container.values())).__dict__.keys():
                result["format_version"] += 1

            for auditorium in catalog:
                result["container"][auditorium.uid] = auditorium.__dict__

            file.seek(0)
            json.dump(result, file)
            file.truncate()

    except (FileNotFoundError, json.JSONDecodeError):
        with open(path, mode="w") as file:
            result: dict[str, int | dict[str, dict[str, str | int]]] = {"format_version": 1, "container": {}}
            for auditorium in catalog:
                result["container"][auditorium.uid] = auditorium.__dict__

            json.dump(result, file)


def catalog_load(path: str) -> Catalog:
    """Загрузка каталога из json"""
    try:
        with open(path, mode="r") as file:
            data = json.load(file)
            result = Catalog()

            try:
                for uid in data["container"]:
                    result.add(Auditorium(**data["container"][uid]))
            except CatalogError:
                raise UnsupportedVersionError("Неподдерживаемый формат сущности")

            return result

    except FileNotFoundError:
        raise CorruptedFileError("Файл не найден")

    except (json.JSONDecodeError, KeyError):
        raise CorruptedFileError("Не удалось расшифровать файл")