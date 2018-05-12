from django.shortcuts import render

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Account, AirDrop, Operation
from . import models
# Create your views here.


class AccountViewSet(ViewSet):
    model = models.Account
    serializer_class = models.AccountSerializer
    def list(self, request):
        obj = self.model.objects.all()
        return Response(self.serializer_class(obj, many=True).data)

    def create(self, request):
        obj = self.model.objects.create(**request.data)
        return Response(self.serializer_class(obj).data)

    def update(self, request, pk):
        obj = self.model.objects.get(name=pk)
        for key, value in request.data.items():
            setattr(obj, key, value)
        obj.save()
        return Response(self.serializer_class(obj).data)

    def delete(self, request, pk):
        obj = self.model.objects.get(name=pk)
        obj.delete()
        return Response(self.serializer_class(obj).data)


class AirDropViewSet(ViewSet):
    model = models.AirDrop
    serializer_class = models.AirDropSerializer
    def list(self, request):
        obj = self.model.objects.all()
        return Response(self.serializer_class(obj, many=True).data)

    def create(self, request):
        obj = self.model.objects.create(**request.data)
        return Response(self.serializer_class(obj).data)

    def update(self, request, pk):
        obj = self.model.objects.get(id=pk)
        for key, value in request.data.items():
            setattr(obj, key, value)
        obj.save()
        return Response(self.serializer_class(obj).data)

    def delete(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.delete()
        return Response(self.serializer_class(obj).data)

class OperationViewSet(ViewSet):
    model = models.Operation
    serializer_class = models.OperationSerializer
    def list(self, request):
        obj = self.model.objects.all()
        return Response(self.serializer_class(obj, many=True).data)

    def create(self, request):
        data = request.data
        obj = self.model.objects.create(account_id=data['account'], airdrop_id=data['airdrop'])
        return Response(self.serializer_class(obj).data)

    def update(self, request, pk):
        obj = self.model.objects.get(id=pk)
        for key, value in request.data.items():
            setattr(obj, key, value)
        obj.save()
        return Response(self.serializer_class(obj).data)

    def delete(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.delete()
        return Response(self.serializer_class(obj).data)
