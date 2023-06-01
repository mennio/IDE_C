from django.urls import include, path
from rest_framework import routers
from compiler.views import CompileWorkflowView

#definis un router et tous ce qui tape sur compile on l'envoi sur le models et gère tous type de requete get etc...
router = routers.DefaultRouter()
router.register("compile", CompileWorkflowView)

urlpatterns = [
    path("api/", include(router.urls)),
]
