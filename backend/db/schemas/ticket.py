from pydantic import BaseModel,Field

class ticketModel(BaseModel):
  priority: int = Field(..., ge=0, le=2)
  subject: str
  description: str | None = None

