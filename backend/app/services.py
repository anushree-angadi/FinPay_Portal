from datetime import datetime
from sqlalchemy import func
from fastapi import HTTPException
from .models import Transaction,Merchant
from .repositories import Repository

TIER_MULTIPLIERS={"BASIC":10000,"PRIME":15000,"PREMIUM":20000}
def calculate_cashback(amount_paise,category,tier,rule):
    if amount_paise<=0: raise ValueError("Payment amount must be greater than zero")
    if category=="TOP_UP": return 0
    if tier not in TIER_MULTIPLIERS: raise ValueError("Unsupported wallet tier")
    return (amount_paise*rule.base_rate_bps*TIER_MULTIPLIERS[tier])//100_000_000

def process_payment(db,student,merchant,amount,key):
    repo=Repository(db)
    if amount<=0: raise HTTPException(400,"Payment amount must be greater than zero")
    wallet=repo.wallet(student.id)
    if not wallet: raise HTTPException(404,"Wallet not found")
    if wallet.balance_paise<amount: raise HTTPException(400,"Insufficient wallet balance")
    if repo.duplicate(student.id,key): raise HTTPException(409,"Duplicate payment request")
    rule=repo.rule(merchant.category)
    if not rule: raise HTTPException(400,"No cashback rule configured")
    try:
        raw=calculate_cashback(amount,merchant.category,wallet.tier,rule)
        month_start=datetime.utcnow().replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        prior=db.query(Transaction).join(Merchant,Transaction.merchant_id==Merchant.id).filter(
            Transaction.student_id==student.id,Merchant.category==merchant.category,
            Transaction.created_at>=month_start,Transaction.status=="SUCCESS").all()
        used=sum(t.cashback_paise for t in prior)
        cashback=min(raw,max(0,rule.monthly_cap_paise-used))
        wallet.balance_paise-=amount
        merchant.balance_paise+=amount
        row=Transaction(student_id=student.id,wallet_id=wallet.id,merchant_id=merchant.id,
            amount_paise=amount,cashback_paise=cashback,status="SUCCESS",idempotency_key=key)
        db.add(row); db.flush(); db.commit(); db.refresh(row)
        return row
    except Exception:
        db.rollback()
        raise

def monthly_reconciliation(db,year,month):
    rows=db.query(Transaction).filter(func.strftime("%Y",Transaction.created_at)==str(year),
        func.strftime("%m",Transaction.created_at)==f"{month:02d}",Transaction.status=="SUCCESS").all()
    total=sum(t.amount_paise for t in rows)
    return {"year":year,"month":month,"transaction_count":len(rows),
        "total_payment_paise":total,"total_cashback_paise":sum(t.cashback_paise for t in rows),
        "merchant_credit_paise":total,"status":"RECONCILED"}
