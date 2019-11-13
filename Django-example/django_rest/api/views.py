from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, EventSerializer, GuestSerializer
from api.models import Event, Guest

# Create your views here.

#ViewsSets定义视图的展现形式
class UserViewSet(viewsets.ModelViewSet):

	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):

	queryset = Group.objects.all()
	serializer_class = GroupSerializer


class EventViewSet(viewsets.ModelViewSet):

	queryset = Event.objects.all()
	serializer_class = EventSerializer


class GuestViewSet(viewsets.ModelViewSet):

	queryset =  Guest.objects.all()
	serializer_class = GuestSerializer