from pydantic import BaseModel
from typing import Optional, List

class Room(BaseModel):
    roomId: int
    roomName: str
    price: float
    currency: Optional[str] = None  # Make currency optional
    benefits: Optional[List[str]] = []  # Make benefits optional with a default empty list