from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

from Search.models import SearchItem, SearchPlugin
from Search.forms import SearchItemForm


admin.site.register(SearchItem)
admin.site.register(SearchPlugin)


class UserAdmin(AdminSite):
    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active

    def login(self, request, extra_context=None):
        defaults = {
            'extra_context': extra_context,
            'current_app': self.name,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'admin/login.html',
        }
        return super(UserAdmin, self).login(request, **defaults)


user_admin_site = UserAdmin(name='user_admin')


class SearchItemAdmin(GuardedModelAdmin):
    fields = ('title', 'snippet', 'owner_comment')
    form = SearchItemForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(SearchItemAdmin, self).get_form(request, obj, **kwargs)
        form.user = request.user

        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(SearchItemAdmin, self).queryset(request)
        return get_objects_for_user(user=request.user, perms=['owner'], klass=SearchItem)


user_admin_site.register(SearchItem, SearchItemAdmin)
