from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.models import User
from .serializers import *
from icecream import ic
from django.contrib.auth import *
from collections import namedtuple
import json
from rest_framework.parsers import MultiPartParser, FormParser

# from rest_framework.serializers import *
# from rest_framework import serializers
from rest_framework.decorators import authentication_classes, permission_classes

from rest_framework import status, permissions, response
from rest_framework.permissions import AllowAny    

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.views import APIView
import base64
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework.generics import *
from django.conf import settings
import requests
from authentication.jwt import *
from authentication.permissions import IsEventOrganizer
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from notifications.models import *
from threading import Timer


from .forms import *

from django.shortcuts import (
    HttpResponseRedirect,
    get_object_or_404,
    get_list_or_404,
    redirect,
    render,
)

from datetime import timedelta, datetime
from rest_framework.parsers import JSONParser

from json import JSONEncoder
import threading


def sendSMS():
