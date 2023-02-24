from weakref import WeakSet
from functools import update_wrapper

from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib.admin.sites import site

from baykeshop.core.options import ModelAdmin


all_sites = WeakSet()



class AdminSite:
    
    final_catch_all_view = True
    
    def __init__(self, name="baykeadmin") -> None:
        self._registry = {}
        self.name = name
        all_sites.add(self)
        
    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"
    
    def check(self, app_configs):
        return site.check(app_configs)
    
    def register(self, model_or_iterable, admin_class=None, **options):
        return site.register(model_or_iterable, admin_class=ModelAdmin, **options)
    
    def unregister(self, model_or_iterable):
        return site.unregister(model_or_iterable)
    
    def is_registered(self, model):
        return site.is_registered(model)
    
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def admin_view(self, view, cacheable=False):
        """
        Decorator to create an admin view attached to this ``AdminSite``. This
        wraps the view and provides permission checking by calling
        ``self.has_permission``.

        You'll want to use this from within ``AdminSite.get_urls()``:

            class MyAdminSite(AdminSite):

                def get_urls(self):
                    from django.urls import path

                    urls = super().get_urls()
                    urls += [
                        path('my_view/', self.admin_view(some_view))
                    ]
                    return urls

        By default, admin_views are marked non-cacheable using the
        ``never_cache`` decorator. If the view can be safely cached, set
        cacheable=True.
        """

        def inner(request, *args, **kwargs):
            if not self.has_permission(request):
                if request.path == reverse(f"baykeadmin:logout", current_app=self.name):
                    index_path = reverse("baykeadmin:index", current_app=self.name)
                    return HttpResponseRedirect(index_path)
                # Inner import to prevent django.contrib.admin (app) from
                # importing django.contrib.auth.models.User (unrelated model).
                from django.contrib.auth.views import redirect_to_login

                return redirect_to_login(
                    request.get_full_path(),
                    reverse("baykeadmin:login", current_app=self.name),
                )
            return view(request, *args, **kwargs)

        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, "csrf_exempt", False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)
    
    def get_urls(self):
        from django.contrib.contenttypes import views as contenttype_views
        from django.urls import include, path, re_path

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)

            wrapper.admin_site = self
            return update_wrapper(wrapper, view)
        urlpatterns = [
            path("", wrap(self.index), name="index"),
            path("login/", self.login, name="login"),
            path("login/", self.logout, name="logout"),
        ]
        
        valid_app_labels = []
        for model, model_admin in self._registry.items():
            urlpatterns += [
                path(
                    "%s/%s/" % (model._meta.app_label, model._meta.model_name),
                    include(model_admin.urls),
                ),
            ]
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        if valid_app_labels:
            regex = r"^(?P<app_label>" + "|".join(valid_app_labels) + ")/$"
            urlpatterns += [
                re_path(regex, wrap(self.app_index), name="app_list"),
            ]

        if self.final_catch_all_view:
            urlpatterns.append(re_path(r"(?P<url>.*)$", wrap(self.catch_all_view)))

        return urlpatterns
    
    @property
    def urls(self):
        return self.get_urls(), "baykeadmin", self.name
    
    def index(self, request):  
        return HttpResponse("测试")
    
    def login(self, request):
        return HttpResponse("login")
    
    def logout(self, request):
        return HttpResponse("logout")
    
    def catch_all_view(self, request, url):
        return site.catch_all_view(request, url)
    

bayke_site = AdminSite(name="baykeadmin")


