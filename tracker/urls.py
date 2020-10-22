from django.urls import path
from .views import *

urlpatterns =[
    path('income-category', income_category, name='income-category'),
    path('income-category-detail/<int:id>', income_category_detail, name='income-category-detail'),
    path('income',incomeListView, name='income'),
    path('income-list-detail/<int:id>',income_list_detail , name='income-list-detail'),
    path('expense-category', expense_category, name='expense-category'),
    path('expense-category-detail/<int:id>', expense_category_detail, name='expense-category-detail'),
    path('expense', expense_list_view, name='expense'),
    path('expense-list-detail/<int:id>',expense_list_detail , name='expense-list-detail'),
    path('income-summary',income_summary, name='income-summary'),
    path('expense-summary', expense_summary,name='expense-summary'),

]