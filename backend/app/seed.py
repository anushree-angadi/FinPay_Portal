from .models import Student,Wallet,Merchant,CashbackRule
from .security import hash_password
def seed(db):
    if db.query(Student).count(): return
    student=Student(name="Demo Student",email="student@finpay.demo",password_hash=hash_password("finpay123"),role="student")
    merchant_user=Student(name="Demo Merchant",email="merchant@finpay.demo",password_hash=hash_password("finpay123"),role="merchant")
    admin=Student(name="FinPay Admin",email="admin@finpay.demo",password_hash=hash_password("finpay123"),role="admin")
    db.add_all([student,merchant_user,admin]); db.flush()
    db.add(Wallet(student_id=student.id,tier="PRIME",balance_paise=2500000))
    db.add_all([Merchant(name="Campus Cafe",category="FOOD"),
        Merchant(name="Tech Store",category="ELECTRONICS"),
        Merchant(name="Book Corner",category="BOOKS"),
        Merchant(name="FinPay Top-up Ledger",category="TOP_UP")])
    # Illustrative values: edit these in Admin > Cashback Rules to match approved policy.
    db.add_all([CashbackRule(category="FOOD",base_rate_bps=200,monthly_cap_paise=50000),
        CashbackRule(category="ELECTRONICS",base_rate_bps=100,monthly_cap_paise=100000),
        CashbackRule(category="BOOKS",base_rate_bps=300,monthly_cap_paise=30000),
        CashbackRule(category="TOP_UP",base_rate_bps=0,monthly_cap_paise=0)])
    db.commit()
