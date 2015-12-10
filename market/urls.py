from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from store.views import CreateStoreView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='homepage'),
    url(r'^createshop', CreateStoreView.as_view(), name='shop_create'),
    url(r'^store', TemplateView.as_view(template_name="store.html"), name='store'),
    # Examples:
    # url(r'^$', 'market.views.home', name='home'),
    # url(r'^market/', include('market.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
