from django.contrib import admin

from .models import Block, Document

class BlockAdmin(admin.ModelAdmin):
    pass

class DocAdmin(admin.ModelAdmin):
    pass


admin.site.register(Block, BlockAdmin)
admin.site.register(Document, DocAdmin)
