from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import User, IOU
from api.serializers import UserSerializer, IOUSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from pprint import pprint


class UserList(APIView):
    """
    List all users, or create a new user.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_id = pk
        borrower_ious = self.get_borrower_iou(user_id)
        lender_ious = self.get_lender_iou(user_id)
        user = self.get_object(pk)
        
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    
    def delete_ious_per_user(self,user_id):
        borrower_ious = self.get_borrower_iou(user_id)
        lender_ious = self.get_lender_iou(user_id)
        for iou in borrower_ious:
            iou.delete()
        for iou in lender_ious:
            iou.delete()
        return None

    def delete(self, request, pk, format=None):
        user_id = pk
        user = self.get_object(user_id)
        self.delete_ious_per_user(user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IOUList(APIView):
    """
    List all IOUs, or create a new IOU
    """
    def get(self, request, format=None):
        ious = IOU.objects.all()
        serializer = IOUSerializer(ious, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = IOUSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IOUDetail(APIView):
    """
    Retrieve, update or delete an IOU record
    """
    def get_object(self, pk):
        try:
            return IOU.objects.get(pk=pk)
        except IOU.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        iou = self.get_object(pk)
        serializer = IOUSerializer(iou)
        return JsonResponse(serializer.data)

    def put(self, request, pk, format=None):
        iou = self.get_object(pk)
        serializer = IOUSerializer(iou, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        iou = self.get_object(pk)
        iou.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)