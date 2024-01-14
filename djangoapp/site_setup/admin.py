from django.contrib import admin
from site_setup import models
# Register your models here.

# AGORA JA DA PAARA EDITAR DIRETAMENTE DO SITESETUP
# @admin.register(models.MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#    list_display = 'id', 'text', 'url_or_path'
#    list_display_links = 'id', 'text', 'url_or_path',
#    search_fields = 'id', 'text', 'url_or_path',


class MenuLinkInline(admin.TabularInline):  # to show MenuLink in siteSetup
    model = models.MenuLink
    extra = 1


@admin.register(models.SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description'
    inlines = MenuLinkInline,

    # True -> permission to add new SiteSetup (in admin area)
    def has_add_permission(self, request):
        return not models.SiteSetup.objects.exists()
