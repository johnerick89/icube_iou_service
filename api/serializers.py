from rest_framework import serializers
from api.models import User, IOU
from django.http import Http404
from pprint import pprint
import json
from decimal import Decimal
import decimal


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    phone = serializers.CharField(required=True, max_length=100)
    owes = serializers.JSONField(required=False)
    owed_by = serializers.JSONField(required=False)
    balance = serializers.DecimalField(required=False,max_digits=10, decimal_places=2)


    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

class IOUSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    borrower = serializers.CharField(required=True, max_length=100)
    lender = serializers.CharField(required=True, max_length=100)
    amount = serializers.DecimalField(required=True,max_digits=10, decimal_places=2)

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404
    
    def get_borrower_iou(self,user_id):
        queryset = IOU.objects.all()
        if user_id is not None:
            queryset = queryset.filter(borrower=user_id)
        return queryset
    
    def get_lender_iou(self,user_id):
        queryset = IOU.objects.all()
        if user_id is not None:
            queryset = queryset.filter(lender=user_id)
        return queryset

    def convert_decimal_to_float(self,value):
        if isinstance(value, decimal.Decimal):
            return float(value)
        return value 
    
    def update_user_iou_data(self, user_id):
        lender_ious = self.get_lender_iou(user_id)
        borrower_ious = self.get_borrower_iou(user_id)

        userModel = self.get_user(user_id)

        owed_by = {}
        owes = {}

        total_owing = 0.0
        total_owed = 0.0
        for lender_iou in lender_ious:
            user = self.get_user(lender_iou.borrower)
            total_owed = decimal.Decimal(total_owed) + lender_iou.amount
            if user.name in owed_by:
                total_owed = lender_iou.amount+Decimal(owed_by.get(user.name ))
                owed_by[user.name ] = self.convert_decimal_to_float(total_owed)
            else:
                owed_by[user.name] = self.convert_decimal_to_float(lender_iou.amount)
        
        for borrower_iou in borrower_ious:
            user = self.get_user(borrower_iou.lender)
            total_owing = decimal.Decimal(total_owing) + borrower_iou.amount
            if user.name in owes:
                total_owed = borrower_iou.amount+Decimal(owes.get(user.name))
                owes[user.name] = self.convert_decimal_to_float(total_owed)
            else:
                owes[user.name] = self.convert_decimal_to_float(borrower_iou.amount)
        
        balance = total_owed-total_owing
        owed_by_json = json.loads(json.dumps(owed_by))
        owes_json = json.loads(json.dumps(owes))
        userModel.owed_by = json.dumps(owed_by_json)
        userModel.owes = json.dumps(owes_json)
        userModel.balance = balance

        userModel.save()

        print("total_owed=="+str(total_owed)+";total_owing=="+str(total_owing)+";balance=="+str(balance))
        return None

    
    def validate_borrower_and_lender(self, borrower, lender):
        if lender == borrower:
            message = 'Borrower cannot be the same as lender'
            raise serializers.ValidationError(message)
    
    def validate_iou(self,validated_data):
        borrower = validated_data["borrower"]
        lender = validated_data["lender"]
        amount = validated_data["amount"]
        self.validate_borrower_and_lender(borrower,lender)
        user_id = borrower
        self.update_user_iou_data(user_id)
        user_id = lender
        self.update_user_iou_data(user_id)

    def create(self, validated_data):
        """
        Create and return a new `IOU` instance, given the validated data.
        """
        self.validate_iou(validated_data)
        return IOU.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `IOU` instance, given the validated data.
        """
        self.validate_iou(validated_data)
        instance.borrower = validated_data.get('borrower', instance.borrower)
        instance.lender = validated_data.get('lender', instance.lender)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance