from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import get_db
from .models import Student

SECRET="CHANGE_THIS_DEMO_SECRET_BEFORE_DEPLOYMENT"
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
bearer=HTTPBearer(auto_error=False)
def hash_password(value): return pwd.hash(value)
def verify_password(value,hashed): return pwd.verify(value,hashed)
def token_for(user):
    return jwt.encode({"sub":str(user.id),"role":user.role,
        "exp":datetime.now(timezone.utc)+timedelta(hours=8)},SECRET,algorithm="HS256")
def current_user(credentials:HTTPAuthorizationCredentials=Depends(bearer),db:Session=Depends(get_db)):
    if not credentials: raise HTTPException(401,"Authentication required")
    try: uid=int(jwt.decode(credentials.credentials,SECRET,algorithms=["HS256"])["sub"])
    except (JWTError,ValueError,KeyError): raise HTTPException(401,"Invalid or expired token")
    user=db.get(Student,uid)
    if not user: raise HTTPException(401,"User not found")
    return user
def roles(*allowed):
    def check(user=Depends(current_user)):
        if user.role not in allowed: raise HTTPException(403,"Not authorized")
        return user
    return check
