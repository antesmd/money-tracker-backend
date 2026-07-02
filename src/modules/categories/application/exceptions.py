from __future__ import annotations


class CategoriesError(Exception):
    pass


class CategoryNotFoundError(CategoriesError):
    pass
