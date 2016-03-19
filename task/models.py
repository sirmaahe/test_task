from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Superuser(User):
    class Meta:
        verbose_name = _('superuser')
        verbose_name_plural = _('superusers')

    def __str__(self):
        return self.username


class Partner(User):
    class Meta:
        verbose_name = _('partner')
        verbose_name_plural = _('partners')

    def __str__(self):
        return self.username


class CreditOrganization(User):
    class Meta:
        verbose_name = _('credit organization')
        verbose_name_plural = _('credit organizations')

    def __str__(self):
        return self.username


class CreditProposal(models.Model):
    class Meta:
        verbose_name = _('credit proposal')
        verbose_name_plural = _('credit proposals')

    CONSUMER = 'consumer'
    MORTGAGE = 'mortgage'
    CAR_LOAN = 'car-loan'
    BUSINESS = 'business'

    PROPOSAL_TYPES = (
        (CONSUMER, _('consumer')),
        (MORTGAGE, _('mortgage')),
        (CAR_LOAN, _('car loan')),
        (BUSINESS, _('business')),
    )

    creation_datetime = models.DateTimeField(_('creation datetime'),
                                             auto_now_add=True)

    modification_datetime = models.DateTimeField(_('modification datetime'),
                                                 auto_now=True)

    rotation_begin_datetime = models.DateTimeField(_('rotation begin datetime'),
                                                   blank=True, null=True)

    rotation_end_datetime = models.DateTimeField(_('rotation end datetime'),
                                                 blank=True, null=True)

    proposal_name = models.CharField(_('proposal name'), max_length=100)

    proposal_type = models.CharField(_('proposal type'), max_length=8,
                                     choices=PROPOSAL_TYPES, default=CONSUMER)

    min_scoring = models.PositiveSmallIntegerField(_('minimum scoring points'))

    max_scoring = models.PositiveSmallIntegerField(_('maximum scoring points'))

    credit_organization = models.ForeignKey(CreditOrganization,
                                            verbose_name=_('credit organization'),
                                            on_delete=models.CASCADE)

    def __str__(self):
        return self.proposal_name


class ClientProfile(models.Model):
    class Meta:
        verbose_name = _('client profile')
        verbose_name_plural = _('client profiles')

    creation_datetime = models.DateTimeField(_('creation datetime'),
                                             auto_now_add=True)

    modification_datetime = models.DateTimeField(_('modification datetime'),
                                                 auto_now=True)

    full_name = models.CharField(_('full name'), max_length=100)

    birthday = models.DateField(_('birthday'))

    phone = models.CharField(_('phone'), max_length=20)

    passport = models.CharField(_('passport'), max_length=20)

    scoring = models.PositiveSmallIntegerField(_('scoring points'))

    partner = models.ForeignKey(Partner,
                                verbose_name=_('partner'),
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class CreditApplication(models.Model):
    class Meta:
        verbose_name = _('credit application')
        verbose_name_plural = _('credit applications')

    NEW = 'new'
    SENT = 'sent'
    RECIEVED = 'recieved'

    STATUSES = (
        (NEW, _('new')),
        (SENT, _('sent')),
        (RECIEVED, _('recieved')),
    )

    creation_datetime = models.DateTimeField(_('creation datetime'),
                                             auto_now_add=True)

    sent_datetime = models.DateTimeField(_('sent datetime'),
                                         blank=True, null=True)

    client_profile = models.ForeignKey(ClientProfile,
                                       verbose_name=_('client profile'),
                                       on_delete=models.CASCADE)

    credit_proposal = models.ForeignKey(CreditProposal,
                                        verbose_name=_('credit proposal'),
                                        on_delete=models.CASCADE)

    status = models.CharField(_('status'), max_length=8,
                              choices=STATUSES, default=NEW)

    def __str__(self):
        return '{}: {}'.format(_('Credit application'), self.id)
