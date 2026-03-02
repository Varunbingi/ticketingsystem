from pydantic import BaseModel

class UpdatePreferenceRequest(BaseModel):
    email_enabled: bool | None = None
    sms_enabled: bool | None = None
    inapp_enabled: bool | None = None