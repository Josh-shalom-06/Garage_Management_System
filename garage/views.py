from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Car, ServiceRecord, Invoice, Mechanic,stock
from .forms import CustomerForm, CarForm, ServiceRecordForm, MechanicForm,stock_form
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from xhtml2pdf import pisa
from .utils import send_sms

# Customer Views
def home(request):
    return render(request, 'garage/home.html')

def mygarage(request):
    return render(request,'garage/mygarage.html')

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'garage/customer_list.html', {'customers': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'garage/customer_details.html', {'customer': customer})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'garage/customer_form.html', {'form': form})

def customer_edit(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'garage/customer_form.html', {'form': form})

def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.delete()
    return redirect('customer_list')

def mech_list(request):
    mechanics = Mechanic.objects.all()
    return render(request, 'garage/mechanic_list.html', {'mechanics': mechanics})

def mech_detail(request, pk):
    mechanic = get_object_or_404(Mechanic, pk=pk)
    return render(request, 'garage/mechanic_details.html', {'mechanic': mechanic})

def mech_create(request):
    if request.method == 'POST':
        form = MechanicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mech_list')
    else:
        form = MechanicForm()
    return render(request, 'garage/mechanic_form.html', {'form': form})

def mech_edit(request, mech_id):
    mechanic = get_object_or_404(Mechanic, pk=mech_id)
    if request.method == 'POST':
        form = MechanicForm(request.POST, instance=mechanic)
        if form.is_valid():
            form.save()
            return redirect('mech_list')
    else:
        form = MechanicForm(instance=mechanic)
    return render(request, 'garage/mechanic_form.html', {'form': form})

def mech_delete(request, mech_id):
    mechanic = get_object_or_404(Customer, pk=mech_id)
    mechanic.delete()
    return redirect('mech_list')

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'garage/car_list.html', {'cars': cars})

def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'garage/car_form.html', {'form': form})

def car_edit(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method=='POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    return render(request, 'garage/car_form.html',{'form':form})                

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    service_records = car.service_records.all()  # Get related service records for this car
    return render(request, 'garage/car_details.html', {'car': car, 'service_records': service_records})


# Service Record Views
def service_record_list(request):
    service_records = ServiceRecord.objects.all()
    return render(request, 'garage/service_record_list.html', {'service_records': service_records})

def service_record_create(request):
    if request.method == 'POST':
        form = ServiceRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_record_list')
    else:
        form = ServiceRecordForm()
    return render(request, 'garage/service_record_form.html', {'form': form})

# Generate Invoice View
def generate_invoice(request, service_record_id):
    service_record = get_object_or_404(ServiceRecord, pk=service_record_id)

    # Check if an invoice has already been generated
    if Invoice.objects.filter(service_record=service_record).exists():
        invoice = Invoice.objects.get(service_record=service_record)
    else:
        # Generate invoice if it doesn't exist
        invoice = Invoice(service_record=service_record)
        invoice.calculate_total()

    # Render invoice as HTML
    html = render_to_string('garage/invoice_template.html', {'invoice': invoice})

    # Convert HTML to PDF using xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response


def spareslist(request):
    parts = stock.objects.all()
    return render(request, 'garage/stock_list.html', {'parts': parts})


def stock_create(request):
    if request.method == 'POST':
        form = stock_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = stock_form()
    return render(request, 'garage/stock_form.html', {'form': form})

def stock_edit(request, pk):
    part = get_object_or_404(stock, pk=pk)
    if request.method == 'POST':
        form = stock_form(request.POST, instance=part)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = stock_form(instance=part)
    return render(request, 'garage/stock_form.html', {'form': form})

def spareslist(request):
    parts = stock.objects.all()
    low_stock_parts = [part for part in parts if part.is_low_stock()]
    return render(request, 'garage/stock_list.html', {'parts': parts, 'low_stock_parts': low_stock_parts})


@csrf_exempt
def update_stock_quantity(request):
    if request.method == 'POST':
        stock_id = request.POST.get('stock_id')
        qty = request.POST.get('qty')

        # Validate inputs
        if not stock_id or not qty:
            return JsonResponse({'error': 'Invalid data provided.'}, status=400)

        try:
            stock_item = stock.objects.get(id=stock_id)
            stock_item.qty = int(qty)
            stock_item.save()
            return JsonResponse({'message': 'Stock updated successfully!'})
        except stock.DoesNotExist:
            return JsonResponse({'error': 'Stock item not found.'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity value.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Allow requests without CSRF tokens for testing
def complete_service(request, service_record_id):
    if request.method == 'POST':
        print(f"Service ID: {service_record_id}") 
        service_record = get_object_or_404(ServiceRecord, pk=service_record_id)
        service_record.service_type = "Completed"  # Update status (or use a status field if applicable)
        service_record.save()

        # Send SMS
        customer_phone = service_record.car.customer.phone
        customer_name = service_record.car.customer.name
        car_details = f"{service_record.car.make} {service_record.car.model} ({service_record.car.license_plate})"
        message = f"Hello {customer_name},\nYour service for {car_details} has been completed. Thank you for choosing us!"

        if send_sms(customer_phone, message):
            return JsonResponse({'message': 'Service marked as completed and SMS sent successfully.'})
        else:
            return JsonResponse({'message': 'Service marked as completed, but SMS could not be sent.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)