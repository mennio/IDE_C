from django.db import models
from django.contrib.auth.models import User
from dataclasses import dataclass

#status
@dataclass
class WorkflowStatus:
    INITIALIZED = "INITIALIZED"
    COMPILING = "COMPILING"
    COMPILING_ERROR = "COMPILING_ERROR"
    EXECUTION_ERROR = "EXECUTION_ERROR"
    EXECUTED = "EXECUTED"

#création de 4 champs : created, user, code source et status
class CompileWorkflow(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code_source = models.TextField(blank=False, null=False)

    workflow_status = (
        (WorkflowStatus.INITIALIZED, "Initialized"),
        (WorkflowStatus.COMPILING, "Compiling"),
        (WorkflowStatus.COMPILING_ERROR, "Compiling Error"),
        (WorkflowStatus.EXECUTION_ERROR, "Execution Error"),
        (WorkflowStatus.EXECUTED, "Executed"),
    )

#status de départ
    status = models.CharField(max_length=300,
                              choices=workflow_status,
                              default=WorkflowStatus.INITIALIZED)
