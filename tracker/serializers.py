from rest_framework import serializers
from.models import *


class IncomeCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeCategory
        fields = ['id', 'name']


class IncomeListSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category')

    class Meta:
        model = Income
        fields = ['id', 'category_name', 'title', 'amount', 'description', 'date_received']


class ExpenseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name']


class ExpenseListSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category')



    class Meta:
        model = Expense
        fields = ['id', 'category_name', 'title', 'amount', 'description', 'date_received']
