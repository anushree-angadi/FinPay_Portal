from .models import Student,Wallet,Merchant,Transaction,CashbackRule
class Repository:
    def __init__(self,db): self.db=db
    def user(self,email): return self.db.query(Student).filter_by(email=email).first()
    def wallet(self,sid): return self.db.query(Wallet).filter_by(student_id=sid).first()
    def merchants(self): return self.db.query(Merchant).order_by(Merchant.name).all()
    def merchant(self,mid): return self.db.get(Merchant,mid)
    def rules(self): return self.db.query(CashbackRule).order_by(CashbackRule.category).all()
    def rule(self,category): return self.db.query(CashbackRule).filter_by(category=category).first()
    def duplicate(self,sid,key): return self.db.query(Transaction).filter_by(student_id=sid,idempotency_key=key).first()
    def transactions(self,sid=None):
        q=self.db.query(Transaction)
        if sid is not None: q=q.filter_by(student_id=sid)
        return q.order_by(Transaction.created_at.desc()).all()
