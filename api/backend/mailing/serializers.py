from .models import *
from rest_framework import serializers

import pytz


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'

    def create(self, validated_data):
        mailing = Mailing(**validated_data)
        mailing.save()
        filter_params = {
            'client_tag': 'tag',
            'client_mobile_operator_code': 'mobile_operator_code',
            'client_time_zone': 'time_zone',
        }
        client_filter = {}
        for param in filter_params.keys():
            if validated_data.get(param):
                client_filter[filter_params[param]] = validated_data[param]
        print(client_filter)
        clients = Client.objects.filter(**client_filter)
        print(clients)
        for client in clients:
            Message.objects.get_or_create(
                client=client,
                mailing=mailing
            )
        return mailing


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('send_date', 'status')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def validate_time_zone(self, time_zone):
        try:
            pytz.timezone(time_zone)
            return time_zone
        except pytz.exceptions.UnknownTimeZoneError:
            raise serializers.ValidationError("Неправильно указан часовой пояс")
