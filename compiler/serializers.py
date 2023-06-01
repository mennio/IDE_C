from rest_framework import serializers
from compiler.models import CompileWorkflow


class CompileWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompileWorkflow
        fields = "__all__"
        read_only_fields = [
            "created",
            "user",
            "code_source",
            "status",
            "wf_log_compilation",
            "wf_exec_stdout",
            "wf_exec_stderr",
            "wf_exec_status_code",
        ]

