from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notifications.models import Notification
from main.permissions import IsOwner
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError


# Create your views here.
class NotificationsAPIView(APIView):
    queryset = Notification.objects.all()
    permission_classes = [IsOwner]

    def get(self, request, pk):
        try:
            notification = self.queryset.get(id=pk)
            self.check_object_permissions(request, notification)
            notification.viewed = True
            notification.save()
        except ObjectDoesNotExist:
            raise ValidationError("No notification exists with the given pk")

        return Response(status=status.HTTP_200_OK)
