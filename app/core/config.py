import os


class Settings():
    SECRET_KEY: str =os.getenv("SECRET_KEY",default="your-secret-key-here")  # Replace with a strong secret
    ALGORITHM: str = "HS256"  # JWT algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Access token expiration time
    NO_REPLY_FROM_EMAIL=os.getenv("NO_REPLY_FROM_EMAIL",default="")
    SUPPORT_FROM_EMAIL=os.getenv("SUPPORT_FROM_EMAIL",default="")
    PASSWORD_RECOVER_EMAIL_EXPIRE_HOURS=3
    RESEND_API_KEY=os.environ["RESEND_API_KEY"]
    
    
    
