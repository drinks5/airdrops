from django.db import models
from rest_framework import serializers
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Account(models.Model):
    zone = models.CharField(default='+86', max_length=10)
    mobile = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    eth = models.CharField(max_length=500)
    json = JSONField()
    profile = JSONField()
    remark = models.CharField("备注", max_length=255, default='')

    class Meta:
        unique_together = (('mobile', 'email', 'name'), )
        ordering = ["id"]

    def __str__(self):
        fields = [x.name for x in self._meta.fields]
        return '\n'.join(
            ['{}: {}'.format(key, getattr(self, key)) for key in fields])
    @property
    def LastName(self):
        return self.profile['LastName']
    @property
    def FirstName(self):
        return self.profile['FirstName']


class Apis(models.Model):
    telegram = JSONField()
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('account', 'telegram'), )


class AirDrop(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    url = models.CharField(max_length=512)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("Updated", auto_now=True)

    #  class Meta:
    #  unique_together = (('name', 'url'), )


class Operation(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    airdrop = models.ForeignKey(AirDrop, on_delete=models.CASCADE)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("Updated", auto_now=True)

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
