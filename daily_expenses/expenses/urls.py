from django.urls import path, include
from .views import CreateUser
from .views import (
    RetrieveUser, 
    AddExpense, 
    RetrieveIndividualExpense, 
    RetrieveOverallExpense, 
    GenerateBalanceSheet, 
    InputValidation
)


urlpatterns = [

    path('create_user/',CreateUser.as_view(), name='create_user'),
    path('retrieve_user/<str:email>/',RetrieveUser.as_view(), name='retrieve_user_details'),
    path('add_expense/',AddExpense.as_view(), name='add_expense'),
    path('retrieve_individual_user_expense/', RetrieveIndividualExpense.as_view(), name='retrieve_individual_user_expense'),
    path('retrieve_overall_user_expense/', RetrieveOverallExpense.as_view(), name='retrieve_overall_user_expense'),
    path('download_balance_sheet/', GenerateBalanceSheet.as_view(), name='download_balance_sheet'),
    path('input_validation/', InputValidation.as_view(), name='input_validation')

    
]
