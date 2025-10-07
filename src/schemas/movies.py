from __future__ import annotations

import datetime as dt
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class CountrySchema(BaseModel):
    id: int
    code: str
    name: Optional[str] = None


class NamedEntitySchema(BaseModel):
    id: int
    name: str


class MovieBriefSchema(BaseModel):
    id: int
    name: Optional[str] = None
    date: Optional[dt.date] = None
    score: Optional[float] = None
    overview: Optional[str] = None


class MovieFullSchema(BaseModel):
    id: int
    name: Optional[str] = None
    date: Optional[dt.date] = None
    score: Optional[float] = None
    overview: Optional[str] = None
    status: Optional[str] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None
    country: Optional[CountrySchema] = None
    genres: List[NamedEntitySchema] = []
    actors: List[NamedEntitySchema] = []
    languages: List[NamedEntitySchema] = []


class MoviesListResponse(BaseModel):
    movies: List[MovieBriefSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int


_ALLOWED_STATUSES = {"Released", "Post Production", "In Production"}


class MovieCreateSchema(BaseModel):
    name: str = Field(..., max_length=255)
    date: dt.date
    score: float = Field(..., ge=0, le=100)
    overview: Optional[str] = None
    status: Optional[str] = None
    budget: Optional[float] = Field(default=None, ge=0)
    revenue: Optional[float] = Field(default=None, ge=0)
    country: Optional[str] = None
    genres: List[str] = []
    actors: List[str] = []
    languages: List[str] = []

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: dt.date) -> dt.date:
        if v > (dt.date.today() + dt.timedelta(days=365)):
            raise ValueError("date must not be more than one year in the future")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v not in _ALLOWED_STATUSES:
            raise ValueError("status must be one of: Released | Post Production | In Production")
        return v


class MovieUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    date: Optional[dt.date] = None
    score: Optional[float] = Field(default=None, ge=0, le=100)
    overview: Optional[str] = None
    status: Optional[str] = None
    budget: Optional[float] = Field(default=None, ge=0)
    revenue: Optional[float] = Field(default=None, ge=0)

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: Optional[dt.date]) -> Optional[dt.date]:
        if v and v > (dt.date.today() + dt.timedelta(days=365)):
            raise ValueError("date must not be more than one year in the future")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v not in _ALLOWED_STATUSES:
            raise ValueError("status must be one of: Released | Post Production | In Production")
        return v
