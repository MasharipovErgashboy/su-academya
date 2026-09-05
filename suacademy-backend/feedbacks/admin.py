from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__full_name', 'user__email', 'suggestions')
    readonly_fields = ('user', 'rating', 'benefits', 'useful_sections', 'suggestions', 'created_at')
    
    def has_add_permission(self, request):
        return False
