from collections.abc import Iterator
from typing import Literal

from pydantic import ValidationError, dataclasses, fields, model_validator

from src.object_catalog.errors import (InvalidEntityError, IdDuplicateError,
                                       ObjectNotFoundError)


@dataclasses.dataclass(kw_only=True)
class Auditorium:
    uid: str = fields.Field(min_length=1)
    name: str = fields.Field(min_length=1)
    category: str = fields.Field(min_length=1)
    date: str = fields.Field(pattern=r"^(?:\d{4}|\d{2}.\d{2}.\d{4})$")
    number: int = fields.Field(gt=0)
    size: Literal["small", "medium", "large"]

    @model_validator(mode="wrap")
    @classmethod
    def validate_entity(cls, data, handler):
        """Перехват ошибки pydantic и вызов InvalidEntityError"""
        try:
            return handler(data)
        except ValidationError:
            raise InvalidEntityError("Некорректные данные сущности")


class Catalog:
    def __init__(self):
        self.container: dict[str, Auditorium] = {}

    def __len__(self) -> int:
        return len(self.container)

    def __iter__(self) -> Iterator[Auditorium]:
        for uid in sorted(self.container):
            yield self.container[uid]

    def __contains__(self, item_id: str) -> bool:
        return item_id in self.container

    def add(self, item: Auditorium) -> None:
        """Добавление элемента в каталог"""
        if item.uid not in self.container:
            self.container[item.uid] = item
        else:
            raise IdDuplicateError("Объект с таким ID уже существует")

    def get(self, item_id: str) -> Auditorium:
        """Получение элемента из каталога"""
        try:
            return self.container[item_id]
        except KeyError:
            raise ObjectNotFoundError("Объект не найден в контейнере")


    def remove(self, item_id: str) -> None:
        """Удаление элемента из каталога"""
        try:
            self.container.pop(item_id)
        except KeyError:
            raise ObjectNotFoundError("Объект не найден в контейнере")

    def find_by_category(self, category: str) -> list[Auditorium]:
        return [entity for entity in self if entity.category == category]

    def find_by_name(self, name: str) -> list[Auditorium]:
        return [entity for entity in self if name.lower() in entity.name.lower()]
