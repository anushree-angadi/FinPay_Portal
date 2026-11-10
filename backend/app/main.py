from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from .database import Base,engine,SessionLocal,get_db
from .models import Student,Wallet,Merchant,Transaction,CashbackRule
from .security import verify_password,token_for,current_user,roles
from .repositories import Repository
from .services import process_payment,monthly_reconciliation
from .seed import seed

app=FastAPI(title="FinPay Student Digital Wallet API",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
Base.metadata.create_all(bind=engine)
with SessionLocal() as db: seed(db)

class Login(BaseModel): email:str; password:str
class Payment(BaseModel):
    merchant_id:int
    amount_paise:int=Field(gt=0)
    idempotency_key:str=Field(min_length=8,max_length=100)
class TopUp(BaseModel):
    amount_paise:int=Field(gt=0)
    idempotency_key:str=Field(min_length=8,max_length=100)
class RuleEdit(BaseModel):
    base_rate_bps:int=Field(ge=0,le=10000)
    monthly_cap_paise:int=Field(ge=0)

@app.get("/")
def home(): return {"app":"FinPay","architecture":"Layered","docs":"/docs"}

@app.post("/api/auth/login")
def login(data:Login,db:Session=Depends(get_db)):
    user=Repository(db).user(data.email)
    if not user or not verify_password(data.password,user.password_hash):
        raise HTTPException(401,"Invalid email or password")
    return {"access_token":token_for(user),"token_type":"bearer",
        "user":{"id":user.id,"name":user.name,"email":user.email,"role":user.role}}

@app.get("/api/auth/me")
def me(user=Depends(current_user)):
    return {"id":user.id,"name":user.name,"email":user.email,"role":user.role}

@app.get("/api/wallet")
def wallet(db:Session=Depends(get_db),user=Depends(roles("student"))):
    w=Repository(db).wallet(user.id)
    return {"id":w.id,"tier":w.tier,"balance_paise":w.balance_paise}

@app.get("/api/merchants")
def merchants(db:Session=Depends(get_db),user=Depends(current_user)):
    return [{"id":m.id,"name":m.name,"category":m.category} for m in Repository(db).merchants()]

@app.post("/api/payments")
def pay(data:Payment,db:Session=Depends(get_db),user=Depends(roles("student"))):
    merchant=Repository(db).merchant(data.merchant_id)
    if not merchant: raise HTTPException(404,"Merchant not found")
    row=process_payment(db,user,merchant,data.amount_paise,data.idempotency_key)
    return {"id":row.id,"amount_paise":row.amount_paise,"cashback_paise":row.cashback_paise,"status":row.status}

@app.post("/api/wallet/top-up")
def topup(data:TopUp,db:Session=Depends(get_db),user=Depends(roles("student"))):
    repo=Repository(db); wallet=repo.wallet(user.id)
    if repo.duplicate(user.id,data.idempotency_key): raise HTTPException(409,"Duplicate top-up request")
    ledger=db.query(Merchant).filter_by(category="TOP_UP").first()
    try:
        wallet.balance_paise+=data.amount_paise
        row=Transaction(student_id=user.id,wallet_id=wallet.id,merchant_id=ledger.id,
            amount_paise=data.amount_paise,cashback_paise=0,status="SUCCESS",idempotency_key=data.idempotency_key)
        db.add(row); db.commit()
        return {"status":"SUCCESS","cashback_paise":0}
    except Exception:
        db.rollback(); raise

@app.get("/api/transactions")
def transactions(db:Session=Depends(get_db),user=Depends(current_user)):
    rows=Repository(db).transactions(user.id if user.role=="student" else None)
    result=[]
    for t in rows:
        m=db.get(Merchant,t.merchant_id)
        result.append({"id":t.id,"merchant":m.name if m else "Unknown",
            "category":m.category if m else "","amount_paise":t.amount_paise,
            "cashback_paise":t.cashback_paise,"status":t.status,"created_at":t.created_at.isoformat()})
    return result

@app.get("/api/cashback/rules")
def rules(db:Session=Depends(get_db),user=Depends(current_user)):
    return [{"id":r.id,"category":r.category,"base_rate_bps":r.base_rate_bps,
        "base_rate_percent":r.base_rate_bps/100,"monthly_cap_paise":r.monthly_cap_paise} for r in Repository(db).rules()]

@app.patch("/api/cashback/rules/{rule_id}")
def edit_rule(rule_id:int,data:RuleEdit,db:Session=Depends(get_db),user=Depends(roles("admin"))):
    rule=db.get(CashbackRule,rule_id)
    if not rule: raise HTTPException(404,"Rule not found")
    rule.base_rate_bps=data.base_rate_bps; rule.monthly_cap_paise=data.monthly_cap_paise
    db.commit()
    return {"message":"Rule updated"}

@app.get("/api/reconciliation/monthly")
def reconcile(year:int,month:int,db:Session=Depends(get_db),user=Depends(roles("admin"))):
    if not 1<=month<=12: raise HTTPException(400,"Month must be 1–12")
    return monthly_reconciliation(db,year,month)
