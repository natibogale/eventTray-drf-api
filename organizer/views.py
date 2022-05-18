from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from authentication.forms import organizerForm
from functools import wraps
from django.contrib import messages
from authentication.models import User, Organizer
from django.shortcuts import (
    HttpResponseRedirect,
    get_object_or_404,
    get_list_or_404,
    redirect,
    render,
)
from .forms import *
from .models import *

# Create your views here.


def organizerIsSetup(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            organizer = Organizer.objects.get(organizer=request.user.id)
            return function(request, *args, **kwargs)
        except Exception as e:
            return redirect("organizer-setup")

    return wrap




@login_required
@organizerIsSetup
def organizerHome(request):
    return render(request, "organizer/index.html")


def organizerSetup(request):

    if request.method == "POST":
        form = organizerForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)

            try:
                isThere = Organizer.objects.get(organizer=request.user.id)

                if isThere:
                    messages.info(
                        request, f"You have already filled this form.", extra_tags="info"
                    )
                    return redirect("organizer-home")  
            except Exception as e:
                pass

            organizer = Organizer.objects.create(
                organizer=user,
                displayName=request.POST["displayName"],
                organizerType=request.POST["organizerType"],
                twitter=request.POST["twitter"],
                telegram=request.POST["telegram"],
                facebook=request.POST["facebook"],
                instagram=request.POST["instagram"],
            )

            if organizer:
                messages.success(
                    request, f"Form submitted Successfully!", extra_tags="success"
                )
            else:
                messages.error(
                    request, f"Internal Error occured! Try again in a few.", extra_tags="danger"
                )
            return redirect("organizer-home")
        else:
            form = organizerForm(request.POST)
            context = {
                "form": form,
            }
            messages.error(request, "One or more fields is not valid!")
            return render(request, "organizer/organizer_setup.html", context)
    form = organizerForm()
    context = {"form": form}
    return render(request, "organizer/organizer_setup.html", context)




@login_required
# @organizerIsSetup
def organizerProfileView(request, username):
    obj = get_object_or_404(User, username=username)
    dire = User.objects.filter(username=request.user)
    org = get_object_or_404(Organizer, organizer=request.user.id)
    if obj in dire:
        form = profileUpdateForm(request.POST or None,request.FILES or None, instance=obj)
        form2 = organizerForm(request.POST or None, instance=org)
        if request.method=="POST" and request.POST.get('profile', None):
            if form.is_valid():
                ref = form.cleaned_data["username"]
                form.save()
                messages.success(
                    request, f'"{ ref }"   your profile has been updated!',extra_tags="success")
                url = request.get_full_path()
                # this = url.replace('update', '')
                return redirect('organizer-profile',request.user)

        # return render(request, "organizer/profile.html", context)
        if request.method=="POST" and request.POST.get('detail', None):
            if form2.is_valid():
                form2.save()
                messages.success(
                    request, f'Your details have been updated!',extra_tags="success")
                url = request.get_full_path()
                # this = url.replace('update', '')
                return redirect('organizer-profile',request.user)

        context = {
            'form2': form2,
            'name': obj,
            "form" : form,
        }
        return render(request, "organizer/profile.html", context)            

    else:
        messages.warning(
            request, f'You have no authorization to access or edit other users profiles!', extra_tags='warning')
        return redirect('organizer-profile',request.user)


    # return render(request, "organizer/profile.html")







@login_required
@organizerIsSetup
def organizerDetailView(request, username):
    obj = get_object_or_404(Organizer, organizer=username)
    dire = Organizer.objects.filter(organizer=request.user)
    if obj in dire:
        form = profileUpdateForm(request.POST or None,
                                 request.FILES or None, instance=obj)
        if form.is_valid():
            ref = form.cleaned_data["username"]
            form.save()
            messages.success(
                request, f'"{ ref }"   your profile has been updated!',extra_tags="success")
            url = request.get_full_path()
            # this = url.replace('update', '')
            return redirect('organizer-profile',request.user)

        context = {
            'form': form,
            'name': obj,
        }
        return render(request, "organizer/profile.html", context)
    else:
        messages.warning(
            request, f'You have no authorization to access or edit other users profiles!', extra_tags='warning')
        return redirect('organizer-profile',request.user)

