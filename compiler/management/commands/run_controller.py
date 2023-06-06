import time
from django.core.management.base import BaseCommand, CommandError
from compiler.models import CompileWorkflow, WorkflowStatus
from compiler.tasks import gcc_compile, run_binary


class Command(BaseCommand):
    help = "Start compiler controller"

    def handle(self, *args, **kwargs):
        print("Compiler controller is running ...")
        while True:
            wf_list = CompileWorkflow.objects.filter(status=WorkflowStatus.INITIALIZED)
            print(f"\nFound {len(wf_list)} in SATUS={WorkflowStatus.INITIALIZED}")
            for wf in wf_list:
                print(f"Compiling workflow id={wf.id}")
                gcc_compile.delay(wf.id)

            wf_list = CompileWorkflow.objects.filter(status=WorkflowStatus.COMPILED_SUCCESS)
            print(f"\nFound {len(wf_list)} in SATUS={WorkflowStatus.COMPILED_SUCCESS}")
            for wf in wf_list:
                print(f"Executing workflow id={wf.id}")
                run_binary.delay(wf.id)

            time.sleep(10)
