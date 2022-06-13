"""
WSGI config for eventTray project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventTray.settings')

application = get_wsgi_application()

from threading import Timer


from django.conf import settings
import requests
from tickets.models import *




from notifications.models import *

def sendSMS():
    # der = Messages.objects.create(phoneNumber="+919012345678", message=" to dssdfsdf")
    ms = Messages.objects.filter(isSent=False)
    for m in ms:
        phoneNumber = m.phoneNumber
        phoneNumber = list(phoneNumber)
        phoneNumber[0] = "+251"
        phoneNumber = "".join(phoneNumber)
        message = m.message
        url = (
                    "https://sms.hahucloud.com/api/send?key="
                    + settings.HAHU_API_KEY
                    + "&phone="
                    + phoneNumber
                    + "&message="
                    + message
                    + "&priority=10"
                )
        r = requests.get(url)
        if r.status_code == 200:
            m.isSent = True
            m.save()



    sendMessageTimer = Timer(3.0, sendSMS)
    sendMessageTimer.start()

sendMessageTimer = Timer(2.0, sendSMS)
sendMessageTimer.start()






def confirmPayment():
    url = ("https://sms.hahucloud.com/api/get/received?key="+settings.HAHU_API_KEY)
    fetch = requests.get(url)
    fetchedMessages = fetch.json()
    i =0
    for message in fetchedMessages:
        phoneNumber = fetchedMessages['data'][i]['phone']
        if phoneNumber == '127':
            message = fetchedMessages['data'][i]['message']
            if 'received' in message:
                ETBindex = message.find("ETB")
                fromIndex = message.find("from")
                amount = message[ETBindex+4:fromIndex]
                bracketIndex = message.find("(")
                sender = message[bracketIndex+5:bracketIndex+14]
                #add 0 to the first of the sender string
                if sender[0] != '0':
                    sender = '0'+sender
                #fetch the most recently saved message from the Messages model
                recentSentMessage = Messages.objects.filter(phoneNumber=sender).order_by('-id')[0]
                message = recentSentMessage.message
                orderNo = message[message.find("is")+3:message.find(". Your tickets")]
                if orderNo:
                    boughtTickets = TicketsBought.objects.filter(orderNo=orderNo,is_payed=False,is_scanned=False)
                    try:
                        totalPrice = int(boughtTickets[0].price) * int(boughtTickets[0].quantity)
                        print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',int(amount), int(totalPrice))

                        if int(amount) == int(totalPrice):
                            
                            for ticket in boughtTickets:
                                ticket.is_payed = True
                                ticket.save()
                    except:
                        pass

            else:
                break

        i+=1
        
        
    
    fetchMessagesTimer = Timer(30.0, confirmPayment)
    fetchMessagesTimer.start()

fetchMessagesTimer = Timer(2.0, confirmPayment)
fetchMessagesTimer.start()

