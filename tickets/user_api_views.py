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
from authentication.serializers import *
# from rest_framework.serializers import *
# from rest_framework import serializers
from rest_framework.decorators import authentication_classes, permission_classes

from rest_framework import status, permissions, response

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


@permission_classes([permissions.AllowAny])

class ListEventTicketView(GenericAPIView):
    serializer_class = eventTicketSerializer

    def get(self, request):
        user = request.user
        try:
            eventId = request.GET.get('id')
            ticket = Tickets.objects.filter(event=eventId)
            for tk in ticket:
                evenet = Events.objects.get(id=tk.event.id)
                tk.eventName = evenet.eventName
                tk.save()
            serializer_class = eventTicketSerializer(ticket, many=True)

            return Response(
                {"status": "success","ticket":serializer_class.data}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"status": "success", "message": "No Tickets Available Yet!"}, status=status.HTTP_404_NOT_FOUND
            )



#a function that cancels all unpaid orders from TicketsBought model
def cancelUnpaidOrders(args, **kwargs):
    ticketsBought = TicketsBought.objects.filter(orderNo=args, is_payed=False) 
    phoneNumber = ""
    for ticketBuyer in ticketsBought:
        phoneNumber = ticketBuyer.phoneNumber
        break

    ticketsBought._raw_delete(ticketsBought.db)

    for key, value in kwargs.items():
        ticket = Tickets.objects.get(id=key)
        ticket.soldTickets = int(ticket.soldTickets) - int(value)
        ticket.save()

    message = "Dear User, \n\n Your order with the Order Number: "+ str(args) +" has been cancelled, because payment was not done within 10 minutes. Please purchase the ticket/s again.\n\n Thank you for using EventTray."

    createMessage = Messages.objects.create(
        phoneNumber=phoneNumber,
        message=message,
    )  

@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])

class BuyEventTicketView(GenericAPIView):
    serializer_class = BuyEventTicketsSerializer


    def post(self, request):
        user = request.user
        serializer_class = BuyEventTicketsSerializer(data=request.data, many=True)

        phoneNumber  = request.data[0]['phoneNumber']
        orderNo = request.data[0]['orderNo']
        ticketId = {}
        totalPriceOfTickets = 0.0
        for eachData in request.data:
            totalPriceOfTickets += float(eachData['price'])
            if eachData['ticket'] not in ticketId:
                ticketId[eachData['ticket']] = eachData['quantity']
        phoneNumberBeforeFormatting = phoneNumber
        phoneNumber = list(phoneNumber)
        phoneNumber[0] = "+251"
        phoneNumber = "".join(phoneNumber)

        if serializer_class.is_valid():
            serializer_class.save()
            for key, value in ticketId.items():
                ticket = Tickets.objects.get(id=key)
                ticket.soldTickets = int(ticket.soldTickets) + int(value)
                ticket.save()


            message = "Dear User, \n\n Your order has been placed successfully. Your order number is " + str(orderNo) + ". Your tickets will be automatically delivered to you after you complete a payment through Telebirr to the customer number 0932661739.\n\n Amount to be paid in total: "+str(totalPriceOfTickets)+" ETB.  \n\n Payments should be done within 10 minutes or your order will be cancelled. \n\n Thank you for using EventTray."

            createMessage = Messages.objects.create(
                phoneNumber=phoneNumberBeforeFormatting,
                message=message,
            )    

            t = Timer(300.0, cancelUnpaidOrders, (orderNo,),ticketId)
            t.start()

            return Response({"status": "success", "message":"Order Placed Successfully!","ticket":serializer_class.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"status": "error", "message": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST
            )



@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])

class ScanEventTicketView(GenericAPIView):
    serializer_class = ScanTicketsSerializer
    def get(self, request):
        user = request.user
        ticketId = Tickets.objects.get(id=request.GET.get('id'))
        buyerId = User.objects.get(id=request.GET.get('buyerId'))
        qrCode = request.GET.get('qrCode')
        ticketsBought = TicketsBought.objects.filter(buyer=buyerId, ticket=ticketId, qrCode=qrCode)
        buyer = User.objects.get(id=buyerId.id)
        serializer_class = UserProfileSerializer(buyer)
        buys = json.dumps(serializer_class.data)

        return Response(
            {"status": "success", "message":"confirmed","profile":serializer_class.data }, status=status.HTTP_202_ACCEPTED
        )
    def patch(self, request):
        user = request.user
        buyerId= request.data['buyerId']
        id = request.data['id']
        qrCode = request.data['qrCode']

        try:

            ticketsBought = TicketsBought.objects.filter( qrCode=qrCode, is_scanned=False).first()
            print('dddddddddddddddddddddddddddddd',ticketsBought)
            ticketsBought.is_scanned = True
            ticketsBought.save()
            
            return Response(
                {"status": "success", "message":"Scanned Ticket!" }, status=status.HTTP_202_ACCEPTED
            )

        except:
            pass
        
        return Response(
            {"status": "error", "message":"Ticket Not Found!" }, status=status.HTTP_404_NOT_FOUND       )
        # serializer_class = ScanTicketsSerializer(data=request.data)
 