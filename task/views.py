from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Partner, CreditProposal, ClientProfile, CreditApplication
from .permissions import ClientProfilePermission, CreditApplicationPermission
from .serializers import ClientProfileSerializer, CreditApplicationSerializer
from .utils import is_partner, is_credit_organization


class ModelViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        # поле, по которому будет осуществляться сортировка (по умолчанию id)
        sort_field = request.query_params.get('sort_by', 'id')
        # поле, по которому будет осуществляться фильтрация
        filter_field = request.query_params.get('filter_by')
        # значение, по которому будет осуществляться фильтрация
        filter_value = request.query_params.get('filter_value')

        filter_params = ({filter_field: filter_value}
                         if filter_field and filter_value else {})

        self.queryset = self.queryset.filter(**filter_params).order_by(sort_field)

        return super().list(request, *args, **kwargs)


class ClientProfileViewSet(ModelViewSet):
    """
    API для работы с анкетами клиентов.

    На get возвращает список анкет; при указании id, возвращает анкету.
    При методе post принимает json с параметрами и создает объект модели.
    При post id/send отправляет заявку, тело запроса (json) должно содержать
    идентификатор заявки: credit_proposal_id.
    """

    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = (permissions.IsAuthenticated, ClientProfilePermission)

    def list(self, request, *args, **kwargs):
        if is_partner(request.user):
            self.queryset = self.queryset.filter(partner__id=request.user.id)
        return super().list(request, *args, **kwargs)

    @detail_route(methods=['post'], url_path='send')
    def send(self, request, *args, **kwargs):
        client_profile = self.get_object()

        # извлечение из тела запроса id кредитного предложения
        credit_proposal_id = request.data.get('credit_proposal_id', '')

        # получение кредитного предложения по id
        try:
            credit_proposal = CreditProposal.objects.get(id=credit_proposal_id)
        except ObjectDoesNotExist:
            response = {'detail': _('Credit proposal id is not exist.')}
            return Response(response)
        except:
            response = {'detail': _('Credit proposal id is absent or not correct.')}
            return Response(response)

        # создание новой заявки
        credit_application = CreditApplication.objects.create(
            client_profile=client_profile,
            credit_proposal=credit_proposal
        )
        credit_application.save()  # автоматически устанавливается время создания

        # отправка заявки
        credit_application.status = CreditApplication.SENT
        credit_application.sent_datetime = timezone.now()
        credit_application.save()

        response = {'detail': _('Credit application successfully sent.')}
        return Response(response)

    def perform_create(self, serializer):
        partner = Partner.objects.get(id=self.request.user.id)
        serializer.save(partner=partner)


class CreditApplicationViewSet(ModelViewSet):
    """
    API для работы с заявками на кредит.

    На get возвращает список заявок; при указании id, возвращает заявку.
    При просмотре кредитной организацией статус заявки изменяется на RECEIVED.
    """

    queryset = CreditApplication.objects.all()
    serializer_class = CreditApplicationSerializer
    permission_classes = (permissions.IsAuthenticated, CreditApplicationPermission)

    def list(self, request, *args, **kwargs):
        if is_credit_organization(request.user):
            self.queryset = self.queryset.filter(
                credit_proposal__credit_organization__id=request.user.id
            )
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if is_credit_organization(request.user):
            credit_application = self.get_object()
            if credit_application.status == CreditApplication.SENT:
                credit_application.status = CreditApplication.RECIEVED
                credit_application.save()
        return super().retrieve(request, *args, **kwargs)
