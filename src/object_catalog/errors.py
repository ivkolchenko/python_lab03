class CatalogError(Exception):
    pass

class InvalidEntityError(CatalogError):
    pass

class IdDuplicateError(CatalogError):
    pass

class ObjectNotFoundError(CatalogError):
    pass

class UnsupportedVersionError(CatalogError):
    pass

class CorruptedFileError(CatalogError):
    pass
