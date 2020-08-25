from django.db import models
import jsonfield


class User(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    phone = models.CharField(max_length=100, blank=False)
    owes = jsonfield.JSONField(blank=False, default={})
    owed_by = jsonfield.JSONField(blank=False, default={})
    balance = models.DecimalField(decimal_places=4,max_digits=25,default=0.0)

    class Meta:
        ordering = ['name']



class IOU(models.Model):
    borrower = models.CharField(max_length=100, blank=False)
    lender = models.CharField(max_length=100, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=4,max_digits=25,blank=False)
