from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.pelayan)
admin.site.register(models.transaksi)
admin.site.register(models.layanan)
admin.site.register(models.detail_layanan)