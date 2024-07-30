from rest_framework import serializers
from .models import User, Expense

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    # members = MemberSerializer(many=True)
    class Meta:
        model = Expense
        fields = '__all__'
        # ['created_by', 'amount', 'members', 'split_expense']