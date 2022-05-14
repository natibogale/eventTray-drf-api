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
