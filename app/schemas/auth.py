from pydantic import BaseModel, EmailStr, constr

class RegisterRequest(BaseModel):
    contact: str  # could be email or phone

class VerifyOTPRequest(BaseModel):
    contact: str
    otp: constr(min_length=4, max_length=6)  # 4–6 digit OTP
