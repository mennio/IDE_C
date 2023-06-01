from rest_framework.viewsets import ModelViewSet
from compiler.serializers import CompileWorkflowSerializer
from compiler.models import CompileWorkflow


class CompileWorkflowView(ModelViewSet):
    queryset = CompileWorkflow.objects.all()
    serializer_class = CompileWorkflowSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
