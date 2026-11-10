from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Student(Base):
    __tablename__="students"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String(100))
    email:Mapped[str]=mapped_column(String(160),unique=True,index=True)
    password_hash:Mapped[str]=mapped_column(String(255))
    role:Mapped[str]=mapped_column(String(20),default="student")

class Wallet(Base):
    __tablename__="wallets"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    student_id:Mapped[int]=mapped_column(ForeignKey("students.id"),unique=True)
    tier:Mapped[str]=mapped_column(String(20),default="BASIC")
    balance_paise:Mapped[int]=mapped_column(Integer,default=0)

class Merchant(Base):
    __tablename__="merchants"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String(120))
    category:Mapped[str]=mapped_column(String(40),index=True)
    balance_paise:Mapped[int]=mapped_column(Integer,default=0)

class CashbackRule(Base):
    __tablename__="cashback_rules"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    category:Mapped[str]=mapped_column(String(40),unique=True,index=True)
    base_rate_bps:Mapped[int]=mapped_column(Integer,default=0)
    monthly_cap_paise:Mapped[int]=mapped_column(Integer,default=0)

class Transaction(Base):
    __tablename__="transactions"
    __table_args__=(UniqueConstraint("student_id","idempotency_key",name="uq_student_idempotency"),)
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    student_id:Mapped[int]=mapped_column(ForeignKey("students.id"),index=True)
    wallet_id:Mapped[int]=mapped_column(ForeignKey("wallets.id"))
    merchant_id:Mapped[int]=mapped_column(ForeignKey("merchants.id"))
    amount_paise:Mapped[int]=mapped_column(Integer)
    cashback_paise:Mapped[int]=mapped_column(Integer,default=0)
    status:Mapped[str]=mapped_column(String(20),default="SUCCESS")
    idempotency_key:Mapped[str]=mapped_column(String(100))
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
