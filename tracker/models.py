from django.db import models

# Create your models here.
try:
    from ..authentication.models import User
except:
    from authentication.models import User


class IncomeCategory(models.Model):
    objects = None
    name = models.CharField(max_length=255,unique=True)
    category_owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Income categories'

    def __str__(self):
        return self.name


class Income(models.Model):
    objects = None
    category = models.ForeignKey(IncomeCategory,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True,unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date_received = models.DateField(null=False, blank=False)
    income_owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True)


    class Meta:
        ordering = ['-date_received']

    def __str__(self):
        return self.description + '|' + str(self.category)


class ExpenseCategory(models.Model):
    objects = None
    name = models.CharField(max_length=255,unique=True)
    category_owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Expense categories'

    def __str__(self):
        return self.name


class Expense(models.Model):
    objects = None
    category = models.ForeignKey(ExpenseCategory,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True,unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date_received = models.DateField(null=False, blank=False)
    expense_owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True)


    class Meta:
        ordering = ['-date_received']

    def __str__(self):
        return self.description + '|' + str(self.category)
