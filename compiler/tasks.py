import os
import time
from subprocess import Popen, PIPE, STDOUT
from celery import shared_task
from compiler.models import CompileWorkflow, WorkflowStatus


@shared_task
def add(x, y):
    time.sleep(10)
    return x + y


working_source_code = '''
//this is a comment
#include <stdio.h>    //including header file in our program

int main()            //main() where the execution begins
{
    printf("Hello World");
    return 0;
} 
'''

not_working_source_code = '''
//this is a comment
#include <stdio.h>    //including header file in our program

int main()            //main() where the execution begins
{
    printf("Hello W
    return 0;
} 
'''


@shared_task
def gcc_compile(wf_id: int):
    # changement status
    CompileWorkflow.objects.filter(id=wf_id).update(status=WorkflowStatus.COMPILING)

    # get code source
    source_code = CompileWorkflow.objects.get(id=wf_id).source_code
    # definis l'emplacement des fichiers source et  cible
    source_code_file = f"/tmp/{wf_id}.c"
    compiled_binary = f"/tmp/{wf_id}_bin"

    # ecrire du code source dans file
    with open(f"/tmp/{wf_id}.c", mode="w") as stream:
        stream.write(source_code)

    # appel de gcc pour la compilation
    p = Popen(["gcc", "-o", f"{compiled_binary}", f"{source_code_file}"], stdout=PIPE, stderr=STDOUT)
    # attendez jusqu'à ce que vous ayez terminé et récupérez les journaux GCC
    gcc_logs, err = p.communicate()
    gcc_logs = gcc_logs.decode('utf-8')

    # sauvegarder le status dans la bd
    if p.returncode:
        # if erreur
        print("compile error")
        CompileWorkflow.objects.filter(id=wf_id).update(
            wf_log_compilation=gcc_logs,
            status=WorkflowStatus.COMPILING_ERROR,
            wf_compiled_binary=None
        )
    else:
        # if la compilation réussit, enregistrez également le contenu binaire
        print("compile success")
        with open(compiled_binary, mode="rb") as compiled_file:
            binary_contents = compiled_file.read()
        CompileWorkflow.objects.filter(id=wf_id).update(
            wf_log_compilation=gcc_logs,
            status=WorkflowStatus.COMPILED_SUCCESS,
            wf_compiled_binary=binary_contents
        )

    # netoyage fichier temporaire
    try:
        os.remove(source_code_file)
    except FileNotFoundError:
        pass
    try:
        os.remove(compiled_binary)
    except FileNotFoundError:
        pass


@shared_task
def run_binary(wf_id: int):
    # change status
    CompileWorkflow.objects.filter(id=wf_id).update(status=WorkflowStatus.EXECUTING)

    # get binaire
    binary_contents = CompileWorkflow.objects.get(id=wf_id).wf_compiled_binary
    compiled_binary_file = f"/tmp/{wf_id}_bin_from_db"
    # ecrire binaire dans le file
    with open(compiled_binary_file, mode="wb+") as stream:
        stream.write(binary_contents)
    p = Popen(["chmod", "+x", f"{compiled_binary_file}"], stdout=PIPE, stderr=STDOUT)
    p = Popen(
        [
            "/bin/sh",
            "-c",
            f"{compiled_binary_file}"
        ], stdout=PIPE, stderr=STDOUT)
    # wait until done and catch GCC logs
    exec_logs, err = p.communicate()
    exec_logs = exec_logs.decode('utf-8')

    # persist status on database
    if p.returncode:
        # if error
        print("exec error")
        CompileWorkflow.objects.filter(id=wf_id).update(
            wf_exec_logs=exec_logs,
            wf_exec_status_code=p.returncode,
            status=WorkflowStatus.EXECUTION_ERROR
        )
    else:
        print("exec success")
        CompileWorkflow.objects.filter(id=wf_id).update(
            wf_exec_logs=exec_logs,
            wf_exec_status_code=0,
            status=WorkflowStatus.EXECUTED
        )
