from rest_framework import status,response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
import datetime
from .serializers import *
import json


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET','POST'])
def income_category(request):

    categories = IncomeCategory.objects.filter(category_owner=request.user)
    if request.method == "GET":
        serializer = IncomeCategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = IncomeCategorySerializer(data=request.data)
        payload = json.dumps(request.data)
        payload = json.loads(payload)

        if serializer.is_valid():
            try:
                if not IncomeCategory.objects.filter(category_owner=request.user,name=payload['name']).exists():
                    serializer.save(category_owner=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Already Category Name exists..!!'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET','PUT','DELETE'])
def income_category_detail(request,id):
    try:
        income = IncomeCategory.objects.filter(income_owner=request.user)
        obj = get_object_or_404(income, id=id)
    except:
        return Response({'error': 'Doesn\'t Exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = IncomeListSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


    elif request.method == "PUT":
        categories = IncomeCategory.objects.filter(category_owner=request.user)
        obj = get_object_or_404(categories, id=id)
        serializer_class = IncomeCategorySerializer
        data = serializer_class(instance=obj, data=request.data)
        if data.is_valid(raise_exception=True):
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        categories = IncomeCategory.objects.filter(category_owner=request.user)
        obj = get_object_or_404(categories, id=id)
        if obj:
            obj.delete()
            return Response({'message':'Deleted'},status=status.HTTP_200_OK)
    return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def incomeListView(request):

    if request.method == "GET":
        income = Income.objects.filter(income_owner=request.user)
        serializer = IncomeListSerializer(income,many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = IncomeListSerializer(data=request.data)
        payload = json.dumps(request.data)
        payload = json.loads(payload)
        if serializer.is_valid():
            serializer.save(income_owner=request.user,category=IncomeCategory.objects.get(name=payload['category_name'],category_owner=request.user))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET','PUT','DELETE'])
def income_list_detail(request, id):
    try:
        income = Income.objects.filter(income_owner=request.user)
        obj = get_object_or_404(income, id=id)
    except:
        return Response({'error':'Doesn\'t Exist'},status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = IncomeListSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = IncomeListSerializer(obj,request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        serializer = IncomeListSerializer(obj)
        if obj:
            obj.delete()
            return Response({'message':'Deleted'},status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET','POST'])
def expense_category(request):

    categories = ExpenseCategory.objects.filter(category_owner=request.user)
    if request.method == "GET":
        serializer = ExpenseCategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExpenseCategorySerializer(data=request.data)
        payload = json.dumps(request.data)
        payload = json.loads(payload)

        if serializer.is_valid():
            try:
                if not ExpenseCategory.objects.filter(category_owner=request.user,name=payload['name']).exists():
                    serializer.save(category_owner=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Already Category Name exists..!!'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET','PUT','DELETE'])
def expense_category_detail(request,id):
    try:
        expense = ExpenseCategory.objects.filter(expense_owner=request.user)
        obj = get_object_or_404(expense, id=id)
    except:
        return Response({'error':'Doesn\'t Exist'},status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ExpenseListSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        categories = ExpenseCategory.objects.filter(category_owner=request.user)
        obj = get_object_or_404(categories, id=id)
        serializer_class = ExpenseCategorySerializer
        data = serializer_class(instance=obj, data=request.data)
        if data.is_valid(raise_exception=True):
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        categories = ExpenseCategory.objects.filter(category_owner=request.user)
        obj = get_object_or_404(categories, id=id)
        if obj:
            obj.delete()
            return Response({'message':'Deleted'},status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET','POST'])
def expense_list_view(request):

    if request.method == "GET":
        expense = Expense.objects.filter(expense_owner=request.user)
        serializer = ExpenseListSerializer(expense,many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ExpenseListSerializer(data=request.data)
        payload = json.dumps(request.data)
        payload = json.loads(payload)
        if serializer.is_valid():
            serializer.save(expense_owner=request.user,category=ExpenseCategory.objects.get(name=payload['category_name'],category_owner=request.user))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET','PUT','DELETE'])
def expense_list_detail(request,id):
    try:
        expense = Expense.objects.filter(expense_owner=request.user)
        obj = get_object_or_404(expense, id=id)
    except:
        return Response({'error':'Doesn\'t Exist'},status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ExpenseListSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        expense = Expense.objects.filter(expense_owner=request.user)
        obj = get_object_or_404(expense, id=id)
        serializer_class = ExpenseListSerializer
        data = serializer_class(instance=obj, data=request.data)
        if data.is_valid(raise_exception=True):
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        expense = Expense.objects.filter(expense_owner=request.user)
        obj = get_object_or_404(expense, id=id)
        if obj:
            obj.delete()
            return Response({'message':'Deleted'},status=status.HTTP_200_OK)


def get_amount_for_income_category(Income,category):
    incomes = Income.filter(category=category)
    amount = 0
    for income in incomes:
        amount += income.amount
    return {'amount': str(amount)}


def get_income_category(incomes):
    return incomes.category


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def income_summary(request):

    if request.method == "GET":
        todays_date = datetime.date.today()
        ayear_ago = todays_date - datetime.timedelta(days=30 * 12)
        incomes = Income.objects.filter(income_owner=request.user, date_received__gte=ayear_ago,
                                        date_received__lte=todays_date)

        final = {}
        categories = list(set(map(get_income_category, incomes)))

        for income in incomes:
            for category in categories:
                final[str(category)] = get_amount_for_income_category(incomes, category)

        return response.Response({'income_category_data': final}, status=status.HTTP_200_OK)


def get_amount_for_expense_category(Expense, category):
    expenses = Expense.filter(category=category)
    amount = 0
    for expense in expenses:
        amount += expense.amount
    return {'amount': str(amount)}


def get_expense_category(expenses):
    return expenses.category


@api_view(['GET'])
def expense_summary(request):

    if request.method=="GET":
        todays_date = datetime.date.today()
        ayear_ago = todays_date - datetime.timedelta(days=30 * 12)
        expenses = Expense.objects.filter(expense_owner=request.user, date_received__gte=ayear_ago,
                                          date_received__lte=todays_date)

        final = {}
        categories = list(set(map(get_expense_category, expenses)))

        for expense in expenses:
            for category in categories:
                final[str(category)] = get_amount_for_expense_category(expenses, category)

        return response.Response({'expense_category_data': final}, status=status.HTTP_200_OK)




