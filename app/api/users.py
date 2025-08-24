from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import random
import string
import time

router = APIRouter()

# ---- In-memory stores ----
otp_store = {}   # { "email_or_phone": {"otp": "1234", "expires": 123456789} }
users = {}       # { "email_or_phone": {"created_at": 123456789} }


# ---- Models ----
class RegisterRequest(BaseModel):
    phone: str | None = None
    email: EmailStr | None = None

class VerifyRequest(BaseModel):
    phone: str | None = None
    email: EmailStr | None = None
    otp: str


# ---- Helpers ----
def generate_otp(length: int = 4) -> str:
    """Generate a numeric OTP of given length."""
    return ''.join(random.choices(string.digits, k=length))


# ---- Endpoints ----
@router.post("/register")
def register_user(request: RegisterRequest):
    """Step 1: User provides phone/email, system sends OTP"""
    identifier = request.email or request.phone
    if not identifier:
        raise HTTPException(status_code=400, detail="Phone or email required")

    # Generate OTP
    otp = generate_otp()
    expires_at = int(time.time()) + 300  # 5 min expiry
    otp_store[identifier] = {"otp": otp, "expires": expires_at}

    # Simulate sending OTP (print to console)
    print(f"📨 OTP for {identifier}: {otp}")

    return {"message": f"OTP sent to {identifier}"}


@router.post("/verify")
def verify_user(request: VerifyRequest):
    """Step 2: User verifies OTP, system creates account"""
    identifier = request.email or request.phone
    if not identifier:
        raise HTTPException(status_code=400, detail="Phone or email required")

    otp_record = otp_store.get(identifier)
    if not otp_record:
        raise HTTPException(status_code=400, detail="No OTP request found")

    if int(time.time()) > otp_record["expires"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    if request.otp != otp_record["otp"]:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # OTP correct → create account
    users[identifier] = {"created_at": int(time.time())}

    # Remove OTP after success
    otp_store.pop(identifier, None)

    return {
        "message": "Account created and logged in",
        "user": identifier,
        "token": "fake-jwt-token"
    }
