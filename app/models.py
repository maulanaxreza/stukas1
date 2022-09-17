from django.db import models

# Create your models here.
class pelayan (models.Model):
  id_pelayan=models.CharField(max_length=5, primary_key=True)
  nama_pelayan=models.CharField(max_length=50)
  no_hp = models.IntegerField()

  def __str__(self):
    return str(self.nama_pelayan)

class transaksi (models.Model):
  id_transaksi=models.CharField(max_length=5, primary_key=True)
  id_pelayan=models.ForeignKey(pelayan, on_delete=models.CASCADE)
  nama_pelanggan=models.CharField(max_length=50)
  tanggal=models.DateField()

  def __str__(self):
    return str (self.nama_pelanggan)

class layanan(models.Model):
  id_layanan=models.CharField(max_length=5, primary_key=True)
  nama_layanan=models.CharField(max_length=50)
  harga = models.IntegerField()

  def __str__(self):
    return str (self.nama_layanan)
  
class detail_layanan (models.Model):
  id_detail_layanan = models.CharField(max_length=5, primary_key=True)
  id_transaksi=models.ForeignKey(transaksi, on_delete=models.CASCADE)
  id_layanan=models.ForeignKey(layanan, on_delete=models.CASCADE)