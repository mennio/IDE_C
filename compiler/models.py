from django.db import models
from django.contrib.auth.models import User
from dataclasses import dataclass


# status
@dataclass
class WorkflowStatus:
    INITIALIZED = "INITIALIZED"
    COMPILING = "COMPILING"
    NO_CODE_SOURCE_ERROR = "NO_CODE_SOURCE_ERROR"
    COMPILED_SUCCESS = "COMPILED_SUCCESS"
    COMPILING_ERROR = "COMPILING_ERROR"
    EXECUTING = "EXECUTING"
    EXECUTION_ERROR = "EXECUTION_ERROR"
    EXECUTED = "EXECUTED"


# création de 4 champs : created, user, code source et status
class CompileWorkflow(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_code = models.TextField(blank=False, null=False)

    workflow_status = (
        (WorkflowStatus.INITIALIZED, "Initialized"),
        (WorkflowStatus.COMPILING, "Compiling"),
        (WorkflowStatus.NO_CODE_SOURCE_ERROR, "No code source error"),
        (WorkflowStatus.COMPILED_SUCCESS, "Compiled success"),
        (WorkflowStatus.COMPILING_ERROR, "Compiling error"),
        (WorkflowStatus.EXECUTING, "Executing"),
        (WorkflowStatus.EXECUTION_ERROR, "Execution error"),
        (WorkflowStatus.EXECUTED, "Executed"),
    )

    # status de départ
    status = models.CharField(max_length=300,
                              choices=workflow_status,
                              default=WorkflowStatus.INITIALIZED)

    #status
    wf_log_compilation = models.TextField(blank=True, null=True)
    wf_exec_logs = models.TextField(blank=True, null=True)
    wf_exec_status_code = models.IntegerField(blank=True, null=True)
    wf_compiled_binary = models.BinaryField(blank=True, null=True)
