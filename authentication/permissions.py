from rest_framework import permissions


class IsEventOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "Organizer":
            return True
        return False


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "User":
            return True
        return False


class IsChecker(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "Ticket Checker":
            return True
        return False
