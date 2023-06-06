from rest_framework import serializers
from compiler.models import CompileWorkflow


class CompileWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompileWorkflow
        exclude = ["wf_compiled_binary"]
        read_only_fields = [
            "created",
            "user",
            "status",
            "wf_log_compilation",
            "wf_exec_logs",
            "wf_exec_status_code",
        ]

