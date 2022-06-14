from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .organizer_api_views import *
from .user_api_views import *

urlpatterns = [
    path("create-ticket/", createTicketView, name="create-ticket"),
    




    #For user api views
    path("list/", ListEventTicketView.as_view(), name="list-tickets-api"),

    path("buy/", BuyEventTicketView.as_view(), name="buy-tickets-api"),





    # Api URL paths for ticket app
    path("", OrganizerEventTicketsView.as_view(), name="create-ticket-api-merch"),
    path("new/", OrganizerEventsTicketsView.as_view(), name="create-ticket-api"),

    path("scan/", ScanEventTicketView.as_view(), name="scan-tickets-api"),

]



