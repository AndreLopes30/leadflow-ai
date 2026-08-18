from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=30)
    insurance_type: str | None = Field(default=None, max_length=80)
    message: str = Field(min_length=5, max_length=2_000)

    @field_validator("name", "phone", "insurance_type", "message", mode="before")
    @classmethod
    def strip_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("phone", "insurance_type")
    @classmethod
    def empty_optional_to_none(cls, value: str | None) -> str | None:
        return value or None


class LeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone: str | None
    insurance_type: str | None
    message: str
    category: str
    score: int
    priority: str
    summary: str
    created_at: datetime
