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
from events.models import *
from authentication.models import *



from notifications.models import *

def sendSMS():
    # der = Messages.objects.create(phoneNumber="+919012345678", message=" to dssdfsdf")
    ms = Messages.objects.filter(isSent=False)
    print(ms)
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



    sendMessageTimer = Timer(30.0, sendSMS)
    sendMessageTimer.start()

sendMessageTimer = Timer(2.0, sendSMS)
sendMessageTimer.start()






def confirmPayment():
    url = ("https://sms.hahucloud.com/api/get/received?key="+settings.HAHU_API_KEY)
    fetch = requests.get(url)
    fetchedMessages = ""
    if fetch.status_code == 200:
        fetchedMessages = fetch.json()
    i =0
    for message in fetchedMessages:
        phoneNumber = fetchedMessages['data'][0]['phone']

        if phoneNumber == '127':
            message = fetchedMessages['data'][0]['message']
            if 'received' in message:
                ETBindex = message.find("ETB")
                fromIndex = message.find("from")
                amount=0
                amount = message[ETBindex+4:fromIndex]
                amount = int(float(amount))


                bracketIndex = message.find("(")
                sender = message[bracketIndex+5:bracketIndex+14]
                #add 0 to the first of the sender string
                if sender[0] != '0':
                    sender = '0'+sender

                #fetch the most recently saved message from the Messages model

                recentSentMessage = Messages.objects.filter(phoneNumber=sender).order_by('-id').first()
                if recentSentMessage:
                    message = recentSentMessage.message

                orderNo = message[message.find("is")+3:message.find(". Your tickets")]
                boughtTickets = TicketsBought.objects.filter(orderNo=orderNo,is_payed=False,is_scanned=False).first()

                
                if orderNo:
                    
                    boughtTickets = TicketsBought.objects.filter(orderNo=orderNo,is_payed=False,is_scanned=False)
                    uniqueTickets={}
                    l=[]
                    for bought in boughtTickets:
                        name = bought.ticket.id
                        allTickets = Tickets.objects.filter(id = name)
                        for each in allTickets:
                            if each.soldTickets:
                                each.soldTickets += 1
                            else:
                                each.soldTickets =1
                            each.save()





                    try:
                        totalPrice=0

                        for bought in boughtTickets:

                            totalPrice += int(float(bought.price))



                        price = int(float(boughtTickets[0].price))

                        quantity = int(float(boughtTickets[0].quantity))

                        # totalPrice = price * quantity

                        print('dddddddddddddddddddddddddddddddddddddddddd',totalPrice)
                        # if totalPrice:
                        #     totalPrice = totalPrice - 20

                        if amount >= totalPrice:

                            for ticket in boughtTickets:

                                try:
                                    eventId = ticket.event

                                    event = Events.objects.get(id=eventId.id)
                                    # print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwww',event)
                                    event.soldTickets = int(float(event.soldTickets)) + int(float(ticket.quantity))
                                    event.eventWallet = int(float(event.eventWallet)) + int(float(totalPrice))
                                    ownerId = event.organizer
                                    event.save()

                                    # owner = User.objects.get(id=ownerId.id)

                                    # print('ssssssssssssssssssss',owner.wallet)
                                    # if not owner.wallet:
                                    #     owner.wallet = 0
                                    # if not owner.sales:
                                    #     owner.sales = 0
                                    # owner.wallet = int(float(totalPrice))
                                    # owner.sales = int(float(totalPrice))
                                    # owner.save()
                                    # print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')


                                except:
                                    pass
                            print('gggggggggggggggggggggggggggggggggggg',ticket.phoneNumber)
                            createMessage = Messages.objects.create(
                                phoneNumber=ticket.phoneNumber,
                                message="Your ticket for "+event.eventName+" has been confirmed. Thank you for buying tickets with us.\n\n EventTray"
                            )
                                
                            yes = TicketsBought.objects.filter(phoneNumber=ticket.phoneNumber)

                            for y in yes:
                                y.is_payed = True
                                y.save()
                    except:
                        pass

            else:
                break

        i+=1
        
        
    
    fetchMessagesTimer = Timer(5.0, confirmPayment)
    fetchMessagesTimer.start()

fetchMessagesTimer = Timer(2.0, confirmPayment)
fetchMessagesTimer.start()

