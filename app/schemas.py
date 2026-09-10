from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

class WidgetPreferenceCreate(BaseModel):
    widget_name: str
    config: dict

class WidgetPreferenceUpdate(BaseModel):
    config: dict