from django.conf import settings
from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt

from .graphql.api import schema
from saleor.graphql.views import GraphQLView

non_translatable_urlpatterns = [
    url(r'^graphql/', csrf_exempt(GraphQLView.as_view(
        schema=schema)), name='api')]

urlpatterns = non_translatable_urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))]

