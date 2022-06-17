from django.shortcuts import render
from .models import *
from .views import *
from .forms import *
# Create your views here.
from django.contrib import messages

from django.shortcuts import (
    HttpResponseRedirect,
    get_object_or_404,
    get_list_or_404,
    redirect,
    render,
)

def createTicketView(request):
    if request.method == "POST":
        form=createEventTicketForm(request.user,request.POST)
        if form.is_valid():
            owner = form.save(commit=False)
            eventId = request.POST["event"]
            event = Events.objects.get(id=eventId)
            owner.ticketOwner = request.user
            owner.eventName = event.eventName
            owner.save()
            messages.success(request, f'New Ticket has been added to your event', extra_tags="success")
            return redirect('create-ticket')
        
        context={
            "form":form,
        }
        messages.error(request, f'Error occured while creating the ticket!', extra_tags="danger")
        return render(request, 'tickets/create_ticket.html',context)

    form = createEventTicketForm(request.user)
    context={
        "form":form,
    }
    return render(request, 'tickets/create_ticket.html',context)

     


def TicketListView(request):
    tickets = Tickets.objects.filter(ticketOwner=request.user.id)
    context={
        "tickets":tickets,
    }
    return render(request, "tickets/tickets_list.html",context)
    
def TicketUpdateView(request, id):
    req = Tickets.objects.filter(id=id).first()
    if request.method == "POST":
        form=createEventTicketForm(request.user,request.POST or None, instance=req)
        if form.is_valid():
            owner = form.save(commit=False)
            eventId = request.POST["event"]
            event = Events.objects.get(id=eventId)
            owner.ticketOwner = request.user
            owner.eventName = event.eventName
            owner.save()
            messages.success(request, f'Ticket has been updated.', extra_tags="success")
            return redirect('ticket-details' ,id)
        
        context={
            "form":form,
        }
        messages.error(request, f'Error occured while updating the ticket!', extra_tags="danger")
        return render(request, 'tickets/tickets_detail.html',context)

    form = createEventTicketForm(request.user, instance=req)
    context={
        "form":form,
    }
    return render(request, 'tickets/tickets_detail.html',context)
