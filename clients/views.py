from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *
from decimal import Decimal

# Create your views here.


def client_list(request):
    clientes = Client.objects.all()
    return render(request, "list.html", {"clientes": clientes})


def client_create(request):

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']

            client = Client(
                cpf=cpf,
                name=request.POST['name'],
                address=request.POST['address'],
                phone=request.POST['phone']
            )

            client.save()
        
            messages.success(request, "Cliente adicionado com sucesso")
            return redirect('clients-list')

        else:
            return render(request, 'create.html', {'clienteForm': form})
    else: 
        return render(request, 'create.html', {'clienteForm': ClienteForm()})
    

    

def client_edit(request, id):
    obj = get_object_or_404(Client, id = id)
      
    form = ClienteForm(initial={
        'name': obj.name,
        'cpf': obj.cpf,
        'phone': obj.phone,
        'address': obj.address
    })

    context = {'client': obj, 'clienteForm': form}
    return render(request, "edit.html", context)



def client_update(request, id):

    client = get_object_or_404(Client, id=id)
    form = ClienteForm(request.POST, instance=client)

    if request.method == 'POST':
        if form.is_valid():
            client.cpf=form.cleaned_data['cpf']
            client.name=request.POST['name']
            client.address=request.POST['address']
            client.phone=request.POST['phone']
            
            client.save()

            messages.success(request, "Dados do cliente atualizados!")
            return redirect('clients-list')
        
        else:

            return render(request, 'edit.html', {'client': client, 'clienteForm': form})


def client_delete(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        client.delete()
        messages.warning(request, "Dados do cliente apagados!")

    return redirect("clients-list")
     




def sales_list(request):

    sales = Sales.objects.all()
    context = {"sales": sales}

    return render(request, 'sales_list.html', context)


def sales_create(request):
    
    form = SaleForm(request.POST)

    if request.method == 'POST':
        product_id = form.data['products']
        amount = form.data['amount']
        product = Products.objects.get(id=product_id)
            
        price = Decimal(product.price) * Decimal(amount)

        if product.amount >= int(amount):
            sale = Sales(
                    product=product,
                    amount=amount,
                    price=price,
                    created_at=timezone.now()
                )
            sale.save()

            product.amount -= int(amount)
            product.save()
                
            return redirect('sales-list')

        else:
            message = 'Quantidade indisponível'

            saleform = SaleForm(initial={
                'products': product_id,
                'amount': amount
            })

            return render(request, 'sales_create.html', {"saleForm": saleform, 'message': message})

    return render(request, 'sales_create.html', {"saleForm": SaleForm()})
    


def products_list(request):
    products = Products.objects.all()
    return render(request, 'product_list.html', {"products": products})