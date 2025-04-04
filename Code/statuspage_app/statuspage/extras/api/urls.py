from statuspage.api.routers import StatusPageRouter
from . import views


router = StatusPageRouter()
router.APIRootView = views.ExtrasRootView

# Webhooks
router.register('webhooks', views.WebhookViewSet)

# Change logging
router.register('object-changes', views.ObjectChangeViewSet)

# ContentTypes
router.register('content-types', views.ContentTypeViewSet)

app_name = 'extras-api'
urlpatterns = router.urls
