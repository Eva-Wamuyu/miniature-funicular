from fastapi import FastAPI,HTTPException
import sqlite3
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from schemas import Account,Card, Customer
from db import create_tables

create_tables()
conn = sqlite3.connect('restful.db', check_same_thread=False)
cursor = conn.cursor()

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(
    middleware=middleware,
    title="simple restful microservice"
)


@app.post("/customers/")        
async def create_customer(customer: Customer):
    cursor.execute("SELECT * FROM customers WHERE customer_id=?", (customer.customer_id,))
    existing_customer = cursor.fetchone()
    if existing_customer is not None:
        #print(f"Error: Customer with id {customer.customer_id} already exists.")
        raise HTTPException(status_code=400, detail="Customer with that id already exists")
    try:
        cursor.execute("INSERT INTO customers (customer_id, name, email) VALUES (?, ?, ?)", (customer.customer_id, customer.name, customer.email))
        conn.commit()
        #print(f"Customer with id {customer.customer_id} was added successfully.")
        return {"message": "Customer added"}
    except sqlite3.IntegrityError as e:
        print("Error:", e)
        conn.rollback()         



@app.post("/accounts/")
async def create_account(account: Account):
    cursor.execute(f"SELECT * FROM customers WHERE customer_id = {account.customer_id}")
    customer = cursor.fetchone()
    if not customer:
        raise HTTPException(status_code=404, detail="The customer ID does not exist.")
    cursor.execute(f"INSERT INTO accounts (customer_id, account_number, balance) VALUES ('{account.customer_id}', '{account.account_number}', '{account.balance}')")
    conn.commit()
    return {"message": "Account created"}


@app.post("/cards/")
async def create_card(card: Card):
    cursor.execute(f"SELECT balance FROM accounts WHERE id = {card.account_id}")
    account = cursor.fetchone()
    print(account)
    
    if not account:
        raise HTTPException(status_code=404, detail="The account ID does not exist.")
    cursor.execute(f"INSERT INTO cards (account_id, card_number, card_type) VALUES ('{card.account_id}', '{card.card_number}', '{card.card_type}')")
    conn.commit()
    return {"message": "Card created"}


@app.post("/accounts/{account_id}/top-up")
async def top_up_account(account_id: int, amount: float):
    cursor.execute(f"SELECT balance FROM accounts WHERE id = {account_id}")
    result = cursor.fetchone()
    if result:
        new_balance = result[0] + amount
        cursor.execute(f"UPDATE accounts SET balance = {new_balance} WHERE id = {account_id}")
        conn.commit()
        return {"message": "Account topped up", "new_balance": new_balance}
    else:
        raise HTTPException(status_code=404, detail="Account not found")


@app.post("/accounts/{account_id}/withdraw")
async def withdraw_from_account(account_id: int, amount: float):
    cursor.execute(f"SELECT balance FROM accounts WHERE id = {account_id}")
    result = cursor.fetchone()
    if result:
        current_balance = result[0]
        if current_balance >= amount:
            new_balance = current_balance - amount
            cursor.execute(f"UPDATE accounts SET balance = {new_balance} WHERE id = {account_id}")
            conn.commit()
            return {"message": "Withdrawal successful", "new_balance": new_balance}
        else:
            raise HTTPException(status_code=400, detail="Insufficient funds")
    else:
        raise HTTPException(status_code=404, detail="Account not found")


@app.get("/")
def home():
    return {
        "restful up"
    }
