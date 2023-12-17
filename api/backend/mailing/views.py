from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from django.http import Http404


from .models import *
from .serializers import *


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    @action(detail=True, methods=['get'])
    def get_mailing_stats(self, request, *args, **kwargs):
        try:
            mailing = self.queryset.get(pk=kwargs.get('pk'))
        except Mailing.DoesNotExist:
            raise Http404
        messages = Message.objects.filter(mailing=mailing)
        count = messages.count()
        messages_stats = {}

        for msg in messages:
            messages_stats[msg.id] = {
                "Client id": msg.client.id,
                "Sending time & date": msg.send_date,
                "Status": msg.status
            }

        data = {
            "Mailing id": mailing.id,
            "Total": count,
            "Messages": messages_stats,
        }
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs.get('pk'))
        except Mailing.DoesNotExist:
            raise Http404
        serializer = MailingSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs.get('pk'))
        except Mailing.DoesNotExist:
            raise Http404
        context = {
            'Deleted mailing id': instance.id
        }
        instance.delete()
        return Response(data=context, status=status.HTTP_204_NO_CONTENT)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs.get('pk'))
        except Client.DoesNotExist:
            raise Http404
        serializer = ClientSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs.get('pk'))
        except Client.DoesNotExist:
            raise Http404
        context = {
            'Deleted client id': instance.id
        }
        instance.delete()
        return Response(data=context, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_all_stats(request):
    mailings = Mailing.objects.all()
    mailings_stats = {}
    for mailing in mailings:
        messages = Message.objects.filter(
            mailing=mailing
        )
        msg_statuses = {}
        for msg in messages:
            if msg_statuses.get(msg.status):
                msg_statuses[msg.status] += 1
            else:
                msg_statuses["text"] = mailing.text
                msg_statuses[msg.status] = 1
        mailings_stats[mailing.id] = msg_statuses
    return Response(data=mailings_stats, status=status.HTTP_200_OK)

