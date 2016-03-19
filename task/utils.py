from .models import Superuser, Partner, CreditOrganization


def is_superuser(user):
    return Superuser.objects.filter(id=user.id).exists()


def is_partner(user):
    return Partner.objects.filter(id=user.id).exists()


def is_credit_organization(user):
    return CreditOrganization.objects.filter(id=user.id).exists()
