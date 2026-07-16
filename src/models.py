from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserProfile(BaseModel):
    id: str
    name: str
    cpf: str
    birth_date: datetime
    is_minor: bool = False

    @property
    def age(self) -> int:
        today = datetime.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class AccessRequest(BaseModel):
    user_id: str
    app_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class AccessResponse(BaseModel):
    allowed: bool
    reason: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
