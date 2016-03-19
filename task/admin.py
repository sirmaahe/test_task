from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Superuser, Partner, CreditOrganization
from .models import CreditProposal, ClientProfile, CreditApplication


@admin.register(CreditProposal)
class CreditProposalAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_datetime'  # установка иерархии по дате
    search_fields = ['proposal_name', 'proposal_type']  # поля, по которым будет вестись поиск
    list_display = ('id', 'creation_datetime', 'modification_datetime',
                    'proposal_name', 'proposal_type', 'credit_organization',
                    'min_scoring', 'max_scoring',
                    'rotation_begin_datetime', 'rotation_end_datetime')
    list_display_links = list_display
    list_filter = ('proposal_type', 'creation_datetime', 'proposal_name')


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_datetime'  # установка иерархии по дате
    search_fields = ['full_name', 'passport']  # поля, по которым будет вестись поиск
    list_display = ('id', 'creation_datetime', 'modification_datetime',
                    'full_name', 'passport', 'birthday', 'phone', 'scoring',
                    'partner')
    list_display_links = list_display
    list_filter = ('full_name', 'creation_datetime', 'birthday')


@admin.register(CreditApplication)
class CreditApplicationAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_datetime'  # установка иерархии по дате
    search_fields = ['status']  # поля, по которым будет вестись поиск
    list_display = ('id', 'creation_datetime', 'sent_datetime', 'status',
                    'client_profile', 'credit_proposal')
    list_display_links = list_display
    list_filter = ('status', 'creation_datetime', 'sent_datetime')


class CustomUserAdmin(UserAdmin):
    # поля, которые выводятся в общем списке и при нажатии на которые выводится окно редактирования модели
    list_display = list_display_links = ('id', 'username')


admin.site.register(Superuser, CustomUserAdmin)
admin.site.register(Partner, CustomUserAdmin)
admin.site.register(CreditOrganization, CustomUserAdmin)
