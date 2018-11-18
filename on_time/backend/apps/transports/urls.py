from itertools import chain

from rest_framework.routers import SimpleRouter

from . import views

app_name = 'transports'

router = SimpleRouter()
router.register('events', views.TransportEventsViewSet, 'events')

urlpatterns = list()
urlpatterns = list(chain(urlpatterns, router.urls))
