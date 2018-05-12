from django.db import models
from rest_framework import serializers

# Create your models here.


class Account(models.Model):
    mobile = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50, primary_key=True)
    telegram = models.CharField(max_length=50)
    eth = models.CharField(max_length=500)
    ethJson = models.FileField()

    class Meta:
        unique_together = (('mobile', 'email', 'name'), )


class AirDrop(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    url = models.CharField(max_length=255)

    class Meta:
        unique_together = (('name', 'url'), )


class Operation(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    airdrop = models.ForeignKey(AirDrop, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('account', 'airdrop'), )


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = []


class AirDropSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirDrop
        exclude = []


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        exclude = []
