from rest_framework import serializers

from .models import ClientProfile, CreditApplication


class ClientProfileSerializer(serializers.HyperlinkedModelSerializer):
    partner = serializers.ReadOnlyField(source='partner.username')

    class Meta:
        model = ClientProfile
        fields = ('id', 'creation_datetime', 'modification_datetime',
                  'full_name', 'birthday', 'phone', 'passport', 'scoring',
                  'partner')


class CreditApplicationSerializer(serializers.HyperlinkedModelSerializer):
    client_profile = serializers.ReadOnlyField(source='client_profile.full_name')
    credit_proposal = serializers.ReadOnlyField(source='credit_proposal.proposal_name')

    class Meta:
        model = CreditApplication
        fields = ('id', 'creation_datetime', 'sent_datetime',
                  'client_profile', 'credit_proposal', 'status')
