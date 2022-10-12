from pydantic import BaseModel, validator


class UserModel(BaseModel):
    name: str
    last_name: str
    birth_date: str
    phone: str
    gender: str
    username: str
    password: str

    @validator("name")
    def name_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError("Name must be a string")
        return v.title()

    @validator("last_name")
    def last_name_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError("Last name must be a string")
        return v.title()

    @validator("birth_date")
    def birth_date_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError("Birth date must be a string")
        return v

    @validator("phone")
    def phone_must_contain_number(cls, v):
        if not v.isdigit():
            raise ValueError("Phone must be a number")
        return v.title()

    @validator("gender")
    def gender_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError("Gender must be a string")
        return v.title()

    @validator("username")
    def username_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.title()

    @validator("password")
    def password_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("Password must be alphanumeric")
        return v.title()
