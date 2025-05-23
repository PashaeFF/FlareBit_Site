from django.contrib import admin
from .models import Slider, SliderSettings

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        if Slider.objects.count() >= 3:
            return False
        return True

@admin.register(SliderSettings)
class SliderSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Eğer hiç kayıt yoksa, eklemeye izin ver
        return not SliderSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Silme işlemini engelle
        return False

    def changelist_view(self, request, extra_context=None):
        # Eğer hiç kayıt yoksa otomatik olarak bir tane oluştur
        if not SliderSettings.objects.exists():
            SliderSettings.objects.create()
        return super().changelist_view(request, extra_context)
