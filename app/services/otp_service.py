import random

# In-memory store (MVP only)
otp_store = {}

def generate_and_send_otp(data):
    otp = str(random.randint(1000, 9999))
    otp_store[data.contact] = otp
    # In production: send via SMS or email
    print(f"OTP for {data.contact} is {otp}")  # for testing

def verify_otp(data):
    if data.contact in otp_store and otp_store[data.contact] == data.otp:
        del otp_store[data.contact]  # remove after use
        return True
    return False
