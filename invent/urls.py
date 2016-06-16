from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
    # Examples:
    url(r'^signup/$', 'invent.views.signup', name='sign'),
    url(r'^logout/$', 'invent.views.Logout', name='out'),
    url(r'^start/$', 'invent.views.FirstUser', name='start'),
    url(r'^$', 'invent.views.logins', name='home'),
    url(r'^history/$', 'invent.views.UserHistory', name='hist'),
    url(r'^(?P<state>\w+)/$', 'invent.views.SuperState', name='stat'),
)