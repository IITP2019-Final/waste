# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Business(models.Model):
    businessid = models.AutoField(db_column='businessID', primary_key=True)  # Field name made lowercase.
    city_cityid = models.ForeignKey('City', models.DO_NOTHING, db_column='city_cityID')  # Field name made lowercase.
    dong = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business'


class City(models.Model):
    cityid = models.AutoField(db_column='cityID', primary_key=True)  # Field name made lowercase.
    sido = models.CharField(max_length=45)
    sigungu = models.CharField(max_length=45)
    weblink = models.TextField()
    guide = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city'


class Order(models.Model):
    orderid = models.AutoField(db_column='orderID', primary_key=True)  # Field name made lowercase.
    waste_wasteid = models.ForeignKey('Waste', models.DO_NOTHING, db_column='waste_wasteID')  # Field name made lowercase.
    order_time = models.DateTimeField(blank=True, null=True)
    business_businessid = models.ForeignKey(Business, models.DO_NOTHING, db_column='business_businessID')  # Field name made lowercase.
    picture = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class Waste(models.Model):
    wasteid = models.AutoField(db_column='wasteID', primary_key=True)  # Field name made lowercase.
    city_cityid = models.ForeignKey(City, models.DO_NOTHING, db_column='city_cityID')  # Field name made lowercase.
    category = models.CharField(max_length=45, blank=True, null=True)
    item = models.CharField(max_length=45, blank=True, null=True)
    size = models.CharField(max_length=80, blank=True, null=True)
    price = models.CharField(max_length=45, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waste'
