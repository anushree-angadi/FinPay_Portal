# FinPay – Student Digital Wallet

## About the Project

FinPay is a Student Digital Wallet application designed to make digital payments easier, faster, and more convenient for students. It allows students to manage their wallet balance, make payments, view transactions, and earn cashback.

## Features

- **Student Login:** Secure authentication using email and password.
- **Wallet Management:** View wallet balance.
- **Digital Payments:** Make payments to registered merchants.
- **Wallet Top-Up:** Add money to the wallet.
- **Transaction History:** View previous transactions.
- **Cashback System:** Earn cashback based on payment rules.
- **Cashback Management:** Manage cashback rules.
- **Monthly Reconciliation:** View monthly payment reconciliation.

## Technology Stack

### Frontend
- HTML
- CSS
- JavaScript
- React / Vite (if applicable)

### Backend
- Python
- FastAPI
- SQLAlchemy
- JWT Authentication

### Database
- SQLite

## Project Structure

```text
FinPay_Application/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── security.py
│   │   ├── seed.py
│   │   └── ...
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── index.html
│   └── package.json
│
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FinPay_Application
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

**Windows PowerShell:**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend URL: http://127.0.0.1:8000

API Documentation: http://127.0.0.1:8000/docs

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the frontend URL displayed in the terminal.

## Demo Login

- **Email:** student@finpay.demo
- **Password:** finpay123

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/auth/login | Student login |
| GET | /api/auth/me | Get user details |
| GET | /api/wallet | View wallet |
| GET | /api/merchants | View merchants |
| POST | /api/payments | Make payment |
| POST | /api/wallet/top-up | Add money |
| GET | /api/transactions | View transactions |
| GET | /api/cashback/rules | View cashback rules |
| PATCH | /api/cashback/rules/{rule_id} | Update cashback rules |
| GET | /api/reconciliation/monthly | Monthly reconciliation |

## Project Objective

The main objective of FinPay is to provide students with a simple and convenient digital wallet platform that supports cashless transactions, wallet management, and cashback rewards.

## Future Enhancements

- QR code-based payments.
- Payment notifications.
- Enhanced fraud detection.
- Integration with real payment gateways.
- Mobile application support.

## Author

Anushree Angadi

---

