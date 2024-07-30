
## Setup and Installation Instructions
    
### 1. Clone Repository

`https://github.com/ananyagopal2000/Daily-Expense-Sharing-Application.git`

`cd daily_expenses`

### 2. Install Dependencies
```pip install -r requirements.txt```

### 3. Setup the Database
```python -m manage.py migrate```

### 4. Run the development server
```python -m manage.py runserver```

## Requests and Responses

## 1. Create user
### Request

```
curl --location 'http://127.0.0.1:8000/api/create_user/ ' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "userm",
  "email": "userm@example.com",
  "mobile_number": "59134567810"
}'
```
### Response
```
{'message':'User has been created successfully!'}
```


## 2. Retrieve user
### Request
``` 
curl --location 'http://127.0.0.1:8000/api/retrieve_user/user2@example.com/' \
--data ''
```
### Responses
```
{
    "id": 2,
    "name": "Johnny Doe",
    "email": "user2@example.com",
    "mobile_number": "1234567891"
}
```


## 3. Add Expense
### Request
```
curl --location 'http://127.0.0.1:8000/api/add_expense/?user1%40example.com=null' \
--header 'Content-Type: application/json' \
--data-raw '{
  "created_by": "userg@example.com",
  "amount": "2000",
  "members_split": [
    {"userg":"userg@example.com"},
    {"usera":"usera@example.com"}, 
    {"useram":"useram@example.com"}],
  "split_method": "equal"
}'
```
### Responses
```
{
    "expense_id": "585b0eb4-bc60-4467-95b4-1a30e6ce8310"
}
```
## 4. Retrieve individual user Expense
### Request
```
curl --location --request GET 'http://127.0.0.1:8000/api/retrieve_individual_user_expense/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"userg@example.com"
}'
```
### Response
```
{
    "Expense-id and amount where paid user paid solely": [
        {
            "expense_id": "864121ff-9f70-4be8-ad84-76f4ed334e02",
            "amount": 2000.0
        },
        {
            "expense_id": "585b0eb4-bc60-4467-95b4-1a30e6ce8310",
            "amount": 2000.0
        }
    ],
    "Expense-id and actual amount paid by the user": [
        {
            "expense_id": 28,
            "amount_owed": 666.67
        }
    ],
    "Total amount user is owed by others": 3333.34,
    "Total amount user owes others": 0
}
```
## 5. Retrieve overall user Expense
### Request
```
curl --location --request GET 'http://127.0.0.1:8000/api/retrieve_overall_user_expense/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"userg@example.com"
}'
```
### Response
```
{
    "total_amount_user_is_owed": 3333.34,
    "total_amount_user_owes": 0
}
```
## 6. Download balance sheet
### Request
```
curl --location 'http://127.0.0.1:8000/api/download_balance_sheet/'
```
### Response
```
Name,Email id,Amount user is owed,Amount user owes,Balance
user1,user1@example.com,1916.72000000000,0,1916.72000000000
user2,user2@example.com,0,793.350000000000,-793.350000000000
user3,user3@example.com,0,723.350000000000,-723.350000000000
userA,usera@example.com,0,1666.67000000000,-1666.67000000000
userB,userb@example.com,0,0,0
userC,userc@example.com,0,0,0
userS,users@example.com,0,0,0
userAm,useram@example.com,0,1666.67000000000,-1666.67000000000
userG,userg@example.com,3333.34000000000,0,3333.34000000000

```
## 7. Input Validation
### Request
```
curl --location 'http://127.0.0.1:8000/api/input_validation/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "created_by": "userg@example.com",
  "amount": "100",
  "members_split": [
    {"email":"userg@example.com",
     "amount": 20},
    {"email":"usera@example.com",
    "amount":80}],
  "split_method": "percentage"
}'
```
### Response
```
{
    "message": "Valid users and percentages"
}
```



