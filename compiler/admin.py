from django.contrib import admin
from compiler.models import CompileWorkflow


#permet de voir la liste des choses que je veut voir sur mon administration
class CompileWorkflowAdmin(admin.ModelAdmin):
    list_display = ["user", "created", "status"]
    list_filter = ["user", "created", "status"]
    search_fields = ["user", "created", "status"]


# Ajouter compiler dans notre administration
admin.site.register(CompileWorkflow, CompileWorkflowAdmin)
