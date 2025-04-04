from statuspage.api.routers import StatusPageRouter
from . import views


router = StatusPageRouter()
router.APIRootView = views.MaintenancesRootView

router.register('maintenances', views.MaintenanceViewSet)
router.register('maintenance-updates', views.MaintenanceUpdateViewSet)
router.register('maintenance-templates', views.MaintenanceTemplateViewSet)

app_name = 'maintenances-api'
urlpatterns = router.urls
