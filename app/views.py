from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from . import models
from datetime import datetime
import tempfile
from django.http import HttpResponse
from weasyprint import HTML
from django.db.models import Sum

# Create your views here.
def home (request):
  layanan_obj = models.layanan.objects.all()
  return render(request,'home.html',{
    'layanan': layanan_obj
  })


def pelayan(request):
  pelayan_obj = models.pelayan.objects.all()
  return render(request,'pelayan.html',{
  'pelayan': pelayan_obj
  })

def add_pelayan(request):
  if request.method == "GET":
    return render(request,'addpelayan.html')
  else:
    nama_pelayan = request.POST['nama_pelayan']
    no_hp = request.POST['no_hp']
    jumlah_pelayan = models.pelayan.objects.all().count()
    total_len = len(str(jumlah_pelayan))
    if total_len == 1:
      id_pelayan = 'P_00'+str(jumlah_pelayan+1)
    else:
      id_pelayan = 'P_00'+str(jumlah_pelayan+1)

  new_pelayan = models.pelayan(
    id_pelayan = id_pelayan,
    nama_pelayan = nama_pelayan,
    no_hp = no_hp
  )
  new_pelayan.save()

  return redirect ('pelayan')

def update_pelayan(request,id):
  pelayan_obj = models.pelayan.objects.get(id_pelayan = id)
  if request.method == "GET":
    return render(request, 'updatepelayan.html',{
      'pelayan': pelayan_obj,
    })
  else:
    pelayan_obj.nama_pelayan = request.POST['nama_pelayan']
    pelayan_obj.no_hp = request.POST['no_hp']
    pelayan_obj.save()
    return redirect('pelayan')

def delete_pelayan(request,id):
  pelayan_obj = models.pelayan.objects.get(id_pelayan=id)
  pelayan_obj.delete()
  return redirect ('pelayan')

def layanan (request):
  layanan_obj = models.layanan.objects.all()
  return render(request,'layanan.html',{
    'layanan': layanan_obj
  })

def add_layanan(request):
  if request.method == "GET":
    return render(request,'addlayanan.html')
  else:
    nama_layanan = request.POST['nama_layanan']
    harga = request.POST['harga']
    jumlah_layanan = models.layanan.objects.all().count()
    total_len = len(str(jumlah_layanan))
    if total_len == 1:
      id_layanan = 'L_00'+str(jumlah_layanan+1)
    else:
      id_layanan = 'L_00'+str(jumlah_layanan+1)

    new_layanan = models.layanan(
      id_layanan=id_layanan,
      nama_layanan = nama_layanan,
      harga = harga
    )
    new_layanan.save()
    return redirect('home')

def update_layanan(request,id):
  layanan_obj = models.layanan.objects.get(id_layanan = id)
  if request.method == "GET":
    return render(request,"updatelayanan.html",{
      'layanan' : layanan_obj
    })
  else:
    layanan_obj.nama_layanan=request.POST['nama_layanan']
    layanan_obj.harga=request.POST['harga']
    layanan_obj.save()
    return redirect('home')
    
def delete_layanan(request,id):
  layanan_obj = models.layanan.objects.get(id_layanan=id)
  layanan_obj.delete()
  return redirect ('home')

def transaksi (request):
  transaksi_obj = models.transaksi.objects.all()
  return render(request,'transaksi.html',{
    'transaksi': transaksi_obj
  })

def add_transaksi(request):
  pelayan_obj = models.pelayan.objects.all()
  layanan_obj = models.layanan.objects.all()

  if request.method == "GET":
    return render (request,'addtransaksi.html',{
            'pelayan' : pelayan_obj,
            'layanan' : layanan_obj
            })
  else:
    nama_pelayan = request.POST['nama_pelayan']
    pelayan_obj = models.pelayan.objects.get(id_pelayan = nama_pelayan)
    nama_pelanggan = request.POST['nama_pelanggan']
    tanggal = request.POST['tanggal']
    jumlah_transaksi = models.transaksi.objects.all().count()
    total_len = len(str(jumlah_transaksi))
    if total_len == 1:
      id_transaksi = 'T_00'+str(jumlah_transaksi+1)
    else:
      id_transaksi = 'T_00'+str(jumlah_transaksi+1)
    
    new_transaksi = models.transaksi(
      id_transaksi = id_transaksi,
      id_pelayan = pelayan_obj,
      nama_pelanggan=nama_pelanggan,
      tanggal = tanggal
    )
    new_transaksi.save()
    return redirect ('home')
  
def update_transaksi (request,id):
  pelayan_obj = models.pelayan.objects.get(id_pelayan = id)
  transaksi_obj = models.transaksi.objects.get(id_transaksi=id)
  tanggal = datetime.strftime(transaksi_obj.tanggal, '%Y-%m-%d')
  if request.method =="GET":
    return render(request,'updatetransaksi.html',{
      'transaksi' : transaksi_obj,
      'pelayan' : pelayan_obj,
      'tanggal' : tanggal
    })
  else:
    transaksi_obj.nama_pelanggan = request.POST['nama_pelanggan']
    transaksi_obj.tanggal = request.POST['tanggal']
    transaksi_obj.id_pelayan = request.POST['pelayan']
  
def delete_transaksi (request,id):
  transaksi_obj = models.transaksi.objects.get(id_transaksi=id)
  transaksi_obj.delete()
  return redirect ('home')

def detail_layanan (request,id):
  detail_layanan_obj = models.detail_layanan.objects.filter(idpelanggan = id)
  return render(request,'detaillayanan.html',{
        'detail_layanan':detail_layanan_obj
    })

def laporan(request):
  if request.method == "GET":
    return render(request, 'laporan.html')
  elif request.method == "POST":
    mulai = request.POST ['mulai']
    akhir = request.POST ['akhir']
    transaksi_obj = models.transaksi.objects.filter(tanggalsewa__range=(mulai,akhir))
    for item in transaksi_obj:
      data=[]
      detail_layanan_obj = models.detail_layanan.objects.filter(id_transaksi = item.id_transaksi)
      data.append(item)
      data.append(detail_layanan_obj)
      totallayanan = detail_layanan_obj.aggregate(Sum('hargalayanan'))
      

def notapdf(request,id):
    # Get selected object 
    layanan_obj = models.layanan.objects.get(id_layanan = id)
    # Get Detail penyewaan
    transaksi_obj = models.transaksi.objects.get(id_transaksi = id)
    # Get detail charge
    detail_layanan_obj = models.detail_layanan.objects.filter(id_detail_layanan = id)
    # total charge
    totallayanan = detail_layanan_obj.aggregate(Sum('hargalayanan'))
    totallayanan = totallayanan['hargalayanan__sum']
    # if totallayanan is not None : 
    #     grandtotal = int(total_layanan)+int(transaksi_obj.hargasewa)
    # else :
    #     grandtotal = int(penyewaanobj.hargasewa)

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_of_students.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string(
        'notapdf.html',{
            'transaksi' : transaksi_obj,
            'detail_layanan' : detail_layanan_obj,
            'totallayanan' : totallayanan
            
            }
    )
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())
    
    return response