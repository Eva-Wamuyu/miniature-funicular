## miniature-funicular


### Setup
```
git clone https://github.com/Eva-Wamuyu/miniature-funicular.git

cd miniature-funicular

python3 -m venv venv 

. venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

### Schema

Customer table
customer_id is the primary key
Customer has a one to many relation with Account
Account has a one to many relation with Card

