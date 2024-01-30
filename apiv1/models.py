from django.db import models

# Create your models here.

class AdmCodeList(models.Model):
    lowestAdmCodeNm = models.CharField(max_length=255)
    admCodeNm = models.CharField(max_length=255)
    admCode = models.CharField(max_length=10)   

class AdmSiList(models.Model):
    lowestAdmCodeNm = models.CharField(max_length=255)
    admCodeNm = models.CharField(max_length=255)
    admCode = models.CharField(max_length=10)

class AdmDongList(models.Model):
    lowestAdmCodeNm = models.CharField(max_length=255)
    admCodeNm = models.CharField(max_length=255)
    admCode = models.CharField(max_length=10)

class AdmReeList(models.Model):
    lowestAdmCodeNm = models.CharField(max_length=255)
    admCodeNm = models.CharField(max_length=255)
    admCode = models.CharField(max_length=10)