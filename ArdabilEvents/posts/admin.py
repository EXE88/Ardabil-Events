from django.contrib import admin
from .models import CreatePost
import jdatetime
import pytz

@admin.register(CreatePost)
class CreatePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'subject_display', 'short_description', 'created_at_jalali')
    list_filter = ('subject_choise', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def subject_display(self, obj):
        return obj.get_subject_choise_display()
    subject_display.short_description = 'موضوع'

    def short_description(self, obj):
        return obj.description[:30] + "..." if len(obj.description) > 30 else obj.description
    short_description.short_description = 'توضیح کوتاه'

    def created_at_jalali(self, obj):
        iran_tz = pytz.timezone('Asia/Tehran')
        created_at_iran = obj.created_at.astimezone(iran_tz)
        jalali_date = jdatetime.datetime.fromgregorian(datetime=created_at_iran)
        return jalali_date.strftime('%Y/%m/%d - %H:%M')
    created_at_jalali.short_description = 'تاریخ ایجاد'