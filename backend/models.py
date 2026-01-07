from pydantic import BaseModel
from typing import List


class ProfileInput(BaseModel):
    role: str
    skills: List[str]
    location: List[str]
