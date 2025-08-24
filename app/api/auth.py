from fastapi import APIRouter, HTTPException
from app.schemas.auth import RegisterRequest, VerifyOTPRequest
from app.services import otp_service, user_service

router = APIRouter()

@router.post("/register")
def register_user(data: RegisterRequest):
    otp_service.generate_and_send_otp(data)
    return {"message": "OTP sent"}

@router.post("/verify-otp")
def verify_user(data: VerifyOTPRequest):
    user = otp_service.verify_otp_and_create_user(data)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return {"message": "User created & logged in", "user": user}
