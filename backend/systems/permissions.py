from rest_framework import permissions
from systems.models import *


class WahahPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if str(request.user) == 'admin':
            return True

        if verification_perm_curl(request.path, request.user, request.method):
            return True


def verification_perm_curl(path, user, method):
    uri_list = path.split('/')[1:-1]

    url = '/{}/{}/'.format(uri_list[0], uri_list[1])

    user_obj = User.objects.filter(username=user)
    user_role_list = user_obj.values('roles')
    user_apiperm_list = Role.objects.filter(id__in=user_role_list).values('apiperms')

    for item in user_apiperm_list:
        menu_info = ApiPerm.objects.get(id=item['apiperms'])
        if url == menu_info.curl and method == menu_info.method:
            return True
