from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum, Q, F
from django.db import models, connection
from .serializers import UserSerializer, ExpenseSerializer
from .models import User, Expense, SplitDetails
import json
import csv

class CreateUser(APIView):
    def post(self, requests):
        ''' Creating a user with details such as name, email id and mobile number'''
        serializer=UserSerializer(data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User has been created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveUser(generics.RetrieveAPIView):   
    def get_queryset(self):
        '''Filtering out the user using email id'''
        email = self.kwargs['email']
        return User.objects.filter(email=email)
    
    def get(self, request, *args,**kwargs): 
        '''Retrieving the details of the user'''
        try:         
            user = self.get_queryset().get()
        except user.DoesNotExist:
            return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

 
class AddExpense(APIView):

    def equal_split_method(self, created_by, members, expense):
        '''Splitting and saving the amount EQUALLY among the users '''
        amount_per_person = int(expense.amount)/(len(members))
        for member_email in members:
            if created_by==member_email:
                SplitDetails.objects.create(                    
                    expense_id=expense,
                    created_by=created_by,
                    member=member_email,
                    amount_paid=int(expense.amount),
                    amount_owed=amount_per_person                   
                )
            else:
                SplitDetails.objects.create(                    
                    expense_id=expense,
                    created_by=created_by,
                    member=member_email,
                    amount_owed=amount_per_person                   
                )
      
    def exact_split_method(self,created_by, members_split, expense):
        '''Splitting and saving the EXACT amount among the users '''
        for member_details in members_split:
            member_email=member_details.get('email')
            amount=member_details.get('amount')
            if created_by==member_email:
                SplitDetails.objects.create(
                    expense_id=expense,
                    created_by=created_by,
                    member=member_email,
                    amount_paid=amount,
                    amount_owed=amount
                )
            else:
                SplitDetails.objects.create(
                    expense_id=expense,
                    created_by=created_by,
                    member=member_email,
                    amount_owed=amount
                )

    def percentage_split_method(self, created_by, members_split, expense):
        '''Splitting  and saving the amount based on PERCENTAGES among the users'''
        for member_details in members_split:
            member_email=member_details.get('email')
            percentage=member_details.get('percentage')
            user_amount=float(expense.amount)*(percentage/100)
            if created_by==member_email:
                SplitDetails.objects.create(
                    expense_id=expense,
                    created_by=created_by,
                    member=member_email,
                    amount_paid=user_amount,
                    amount_owed=user_amount
                ) 
            else:
                SplitDetails.objects.create(
                    expense_id=expense,
                    created_by=created_by,
                    member=member_email,
                    amount_owed=user_amount
                )

    def post(self, requests):
        '''Saving the data to Expense table and SplitDetails table'''
        data=json.loads(requests.body)
        created_by_email = data.get('created_by')
        amount = data.get('amount')
        members_split = data.get('members_split')
        split_method = data.get('split_method')
        
        try:
            created_by = User.objects.get(email=created_by_email)        
        except User.DoesNotExist():
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)        
        
        expense=Expense.objects.create(
            created_by=created_by, 
            amount=amount,
            split_method=split_method
            )
        expense.save()

        if split_method=="Equal" or split_method=="equal":            
            members = [list(member.values())[0] for member in members_split]                
            self.equal_split_method(created_by, members, expense)
        
        if split_method=='Exact' or split_method=='exact':                        
            self.exact_split_method(created_by, members_split, expense)

        if split_method=='Percentage' or split_method=='percentage':
            self.percentage_split_method(created_by, members_split, expense)

        return Response({"expense_id":expense.expense_id}, status=status.HTTP_201_CREATED)
    
class RetrieveIndividualExpense(APIView):
    '''Retrieving the individual expense of a given user'''
    def get(self, requests):
        data = json.loads(requests.body)
        user_email=data.get('email')
        
        try:
            user = User.objects.get(email=user_email)        
        except User.DoesNotExist():
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        expenses = Expense.objects.filter(created_by=user).values('expense_id', 'amount') #amount paid solely
        user_expense = SplitDetails.objects.filter(member=user_email).values('expense_id','amount_owed')

        total_owed = SplitDetails.objects.filter(created_by=user).exclude(member=user_email).aggregate(total_amount_owes=Sum('amount_owed'))['total_amount_owes'] or 0  #amount others owe the user   
        total_owes = SplitDetails.objects.filter(member=user_email).exclude(created_by=user).aggregate(total_amount_owed=Sum('amount_owed'))['total_amount_owed'] or 0  #amount user owes others
        
        response={
            "Expense-id and amount where paid user paid solely": expenses,
            "Expense-id and actual amount paid by the user": user_expense,
            "Total amount user is owed by others": total_owed,
            "Total amount user owes others": total_owes
        }
        return Response(response, status=status.HTTP_200_OK)
    
class RetrieveOverallExpense(APIView):
    '''Retrieving the overall expense of a given user'''
    def get(self, requests):
        data = json.loads(requests.body)
        user_email=data.get('email')

        try:
            user = User.objects.get(email=user_email)        
        except User.DoesNotExist():
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        total_is_owed = SplitDetails.objects.filter(created_by=user, status="Unpaid").exclude(member=user_email).aggregate(total_amount_user_is_owed=Sum('amount_owed'))
        total_owes = SplitDetails.objects.filter(member=user_email, status="Unpaid").exclude(created_by=user).aggregate(total_amount_user_owes=Sum('amount_owed'))

        response= {
            'total_amount_user_is_owed': total_is_owed['total_amount_user_is_owed'] or 0,
            'total_amount_user_owes': total_owes['total_amount_user_owes'] or 0,
        }
        return Response(response,status=status.HTTP_200_OK)    

class GenerateBalanceSheet(APIView):
    '''Generating balance sheet'''
    def get(self,requests):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="balance_sheet.csv"'},
        )

        writer=csv.writer(response)
        writer.writerow(["Name", "Email id", "Amount user is owed", "Amount user owes", "Balance"])

        users = User.objects.all()

        for user in users:
            user_email = user.email
            user_name = user.name

            # Calculate total amount user owes
            total_owes = SplitDetails.objects.filter(member=user_email, status="Unpaid").exclude(created_by=user).aggregate(total_amount_owed=Sum('amount_owed'))['total_amount_owed'] or 0

            # Calculate total amount user is owed
            total_owed = SplitDetails.objects.filter(created_by=user, status="Unpaid").exclude(member=user_email).aggregate(total_amount_owes=Sum('amount_owed'))['total_amount_owes'] or 0

            # Calculate balance
            balance = total_owed - total_owes

            # Writing data to CSV
            writer.writerow([user_name, user_email, total_owed, total_owes, balance])

        return response
    
class InputValidation(APIView):
    '''Validating the users and percentage split if method of split is percentages'''
    def post(self, requests):
        data = json.loads(requests.body)
        user_id = data.get("created_by")
        member_split = data.get("members_split")
        split_method = data.get("split_method")

        def percentage_validation(percentages):
            '''Validating percentages and splits'''
            total = sum(percentages)
            if total == 100:
                return Response({"message": "Valid users and percentages"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid percentages. Recheck member percentages!"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if split_method == "percentage" or split_method == "Percentage":
            percentages = [member.get('amount') for member in member_split]
            return percentage_validation(percentages)
        
        # Validating users
        try:
            user = User.objects.get(email=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        members_mail = [list(member.values())[0] for member in member_split]

        for email_id in members_mail:
            try:
                member_user = User.objects.get(email=email_id)
            except User.DoesNotExist:
                return Response({"error": f"Member with email {email_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Valid users"}, status=status.HTTP_200_OK)

#controller, service, model\\
# main apis descrption\\
# #api endpoints - 1 line explain \\
# curl command in postmn= has request body and respons - 
# future improvements - authentication and token authentication, optimix=zation,
# way implementation - locally testedafter each checkpoint of code,  api endpoints were working 
# gitclone the code
# go to this directory
# #generate requirements.txt file    
        

