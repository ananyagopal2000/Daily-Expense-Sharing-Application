
# Daily Expense Sharing Application

The Daily Expense Sharing Application is designed to facilitate the management and sharing of expenses among groups of users. This application helps users keep track of who owes what to whom, ensuring a fair distribution of shared costs and accountablity.

## Key features
### 1. User Management
- **Create User** : Creates a and stores user details such as name, email id and pone number

- **Retrieve User** : Enables users to view their personal account information.

### 2. Expense Management
- **Add Expense** : Users can add new expenses by specifying the amount, split method (equal, exact, or percentage), and involved members using their email addresses.

- **Retrieve Individual User expenses** : Allows users to view their personal expenses, including the total amount paid solely, the actual amount after the split, total amount they owe and the total amount they are owed.

- **Retrieve Overall expense** : Provides the user a comprehensive amount that includes the total amount they owe and the total amount they are owed.

- **Download Balance sheet** : Users can download a balance sheet that summarizes individual, showing the balance for each user

### 3. Input Validation
- Validates user inputs to ensure they are accurate and consistent.

- Ensures that percentages in the percentage split method add up to 100%, guaranteeing an equitable distribution of expenses.

## Implementation details

- **Models** : The application uses Django models for managing users (**User**), expenses (**Expense**), and split details (**SplitDetails**).
    - **`User`**: model contains user details like name, email id and phone number
    - **`Expense`**: model includes fields for the creator, expense ID, amount, split method, and date.
    - **`SplitDetails`** : model contains fields for the expense, creator, member, amount paid, amount owed, status, and date.

- **API Endpoints** :
    - **User Endpoints** :
        - **`Create User`** : API to create new user
        - **`Retrieve User Details`** : API to retrieve details of existing user
    - **Expense Endpoints** :
        - **`Add Expense`** : API to create new user
        - **`Retrieve Individual User Expense`** : API to retrieve details of all expense a particular user is involved in
        - **`Retrieve Overall Expenses`** : API to retrieve overall expense details of a particular user
        - **`Download Balance Sheet`** : API to download the balance sheet that summarizes expenses
    - **Validation Endpoints** :
        - **`Input Validaition`**: API to validate the users and percentages if present

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

## Future Enhancements
If I were to be given more time to execute this project, I would:
- Implement Authorization and Authentication services for the user using tokens. This would enhance the overall security and trustworthiness of the application.
- Implements unit test cases. Although the code was locally tested after each checkpoint and verified the working conditions of the API endpoints before moving to implement the logical chunk of code, I would implement unit test cases using unittestcase in python for clarity during integration tests
- develop an end -to-end mobile application that would have features like logging in and logging out of users, create rooms and add-split expenses within the room, add a payment inerface to make payments quick and hassle free.




