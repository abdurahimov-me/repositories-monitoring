from django.db import models


class Positions(models.TextChoices):
    BOSS = 'boss', 'Boss'
    DISPATCHER = 'dispatcher', 'Dispatcher'
    MANGER = 'manager', 'Manager'
    OTHER = 'other', 'Other'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Employee(BaseModel):
    first_name = models.CharField(
        verbose_name='First Name',
        max_length=100
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Last Name'
    )
    father_name = models.CharField(
        verbose_name='Father Name',
        max_length=100
    )
    phone = models.CharField(
        verbose_name='Phone',
        max_length=20,
    )
    position = models.CharField(
        verbose_name='Position',
        max_length=100,
        choices=Positions.choices
    )
    age = models.PositiveSmallIntegerField(
        verbose_name='Age',
    )
    photo = models.ImageField(
        verbose_name='Photo',
        upload_to='photos/',
    )

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        db_table = 'employees'
