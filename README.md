# FinPay – Student Digital Wallet

A student wallet application with a React frontend and FastAPI backend.

## Features
- JWT login with Student, Merchant and Admin demo roles
- Student wallet with BASIC / PRIME / PREMIUM tiers
- Merchant directory and category-based payments
- Payment processing with wallet debit, merchant credit and transaction record
- Positive amount, sufficient-balance and duplicate-request checks
- Cashback calculation in integer paise; TOP_UP earns zero cashback
- Tier multipliers: BASIC 1.0x, PRIME 1.5x, PREMIUM 2.0x
- Monthly category cashback caps applied during payment processing
- Monthly reconciliation summary
- SQLite database and layered backend modules

The supplied documents' numeric cashback rates/caps are not fully specified in the available project notes. The included rates/caps are clearly marked as illustrative demo values and can be edited by the Admin screen.

## Requirements
- Python 3.10+
- Node.js 18+

## Run backend (PowerShell terminal 1)
```powershell
cd .\backend
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

If PowerShell activation is blocked, skip activation and run:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

## Run frontend (PowerShell terminal 2)
```powershell
cd .\frontend
npm.cmd install
npm.cmd run dev
```
Open http://localhost:5173. API docs: http://127.0.0.1:8000/docs

## Demo accounts
Password for all: `finpay123`
- Student: student@finpay.demo
- Merchant: merchant@finpay.demo
- Admin: admin@finpay.demo

Educational prototype only. Do not use for real financial transactions. Change the demo JWT secret, passwords and CORS configuration before deployment.
