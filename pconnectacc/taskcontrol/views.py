from django.shortcuts import render, redirect, get_object_or_404
from taskcontrol.models import *
from .forms import CustomUserCreationForm, CustomPasswordResetForm
from datetime import datetime, date
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.utils.dateparse import parse_date
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db.models import Max, Count, F, Subquery
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from collections import Counter

# Constants
STATUS_OPEN_JOB = 'OPENJOB'
STATUS_DONE = 'DONE'

def handler404(request, exception):
    return render(request, 'task/404.html')

#TODO Login Logout
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'เข้าสู่ระบบสำเร็จ')
            return redirect('taskcontrol:dashboard')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        last_login_time = request.user.last_login
        logout(request)
        messages.success(request, 'ออกจากระบบเรียบร้อย.')

        if last_login_time is not None:
            current_time = datetime.now()
            time_difference = current_time - last_login_time

            if time_difference.total_seconds() > 3600:
                messages.success(request, 'ออกจากระบบเนื่องจากไม่มีการใช้งานเกิน 1 ชั่วโมง.')
    return redirect('taskcontrol:login')

#TODO Others
def parse_date(date_string):
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        print(f"Error parsing date string: {date_string}")
        return None

def get_districts(request):
    province_id = request.GET.get('province_id')
    district = District.objects.filter(province=province_id).all().values('id','name_th')
    return JsonResponse(list(district),safe=False)

def get_subdistricts(request):
    district_id = request.GET.get('district_id')
    subdistrict = Subdistrict.objects.filter(district=district_id).all().values('id', 'name_th', 'zipcode')
    return JsonResponse(list(subdistrict),safe=False)

def get_latest_job_code(request):
    # ดึงค่า job_code ที่มีค่าสูงสุดจากฐานข้อมูล
    latest_job_code = Engagement.objects.aggregate(Max('job_code'))['job_code__max']

    # ตรวจสอบหาก latest_job_code เป็น None แล้วกำหนดให้เป็น '24-0001'
    if latest_job_code is not None:
        current_number = int(latest_job_code.split('-')[1]) + 1
    else:
        current_number = 1

    # ดึงปีปัจจุบัน
    current_year = datetime.now().year

    # สร้าง job_code ใหม่
    new_job_code = f'24-{current_number:04d}'

    # ส่งค่าในรูปแบบ JSON response กลับไป
    return JsonResponse({'latest_job_code': new_job_code})

def test(request):
    client = Client.objects.all().values('id', 'code', 'company_name')
    return JsonResponse(list(client),safe=False)

@login_required
def user_management(request):
    return render(request,'task/user_management.html')

@login_required
def client_list(request):
    clients_list = Client.objects.all().order_by('code')

    clients_per_page = 10
    paginator = Paginator(clients_list, clients_per_page)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'task/clients/client_list.html', {'clients': page})

@login_required
def client_create(request):
    register_tax = None
    file = None
    contact = None

    subdistrict = Subdistrict.objects.values('id', 'name_th', 'zipcode')
    district = District.objects.values('id', 'name_th')
    province = Province.objects.values('id', 'name_th').order_by('name_th')
    register_types = RegisterType.objects.values('id','short_name','name_th','name_en')

    if request.method == 'POST':
        c_code = request.POST.get('c_code', '')
        c_company_name = request.POST.get('c_company_name', '')
        c_tax_id = request.POST.get('c_tax_id', '')
        c_service_fee = request.POST.get('c_service_fee')
        c_address = request.POST.get('c_address')
        c_address2 = request.POST.get('c_address2')
        c_province = request.POST.get('c_province')
        c_district = request.POST.get('c_district')
        c_subdistrict = request.POST.get('c_subdistrict')
        c_channal = request.POST.get('c_channal')
        c_detail = request.POST.get('c_detail')
        c_status = request.POST.get('c_status')
        c_create_client_date = request.POST.get('c_create_client_date', '')

        if c_status == 'on':
            c_status = True
        else:
            c_status = False

        r_vat = request.POST.get('r_vat')
        r_vat_date = request.POST.get('r_vat_date')
        r_sbt = request.POST.get('r_sbt')
        r_sbt_date = request.POST.get('r_sbt_date')
        r_sso = request.POST.get('r_sso')
        r_sso_date = request.POST.get('r_sso_date')
        r_dbd_e_filling = request.POST.get('r_dbd_e_filling')
        r_dbd_e_filling_date = request.POST.get('r_dbd_e_filling_date')
        r_company = request.POST.get('r_company')
        r_company_date = request.POST.get('r_company_date')
        r_company_period_date = request.POST.get('r_company_period_date')

        date_c_create_client_date = parse_date(c_create_client_date)
        date_vat = parse_date(r_vat_date)
        date_sbt = parse_date(r_sbt_date)
        date_sso = parse_date(r_sso_date)
        date_dbd_e_filling = parse_date(r_dbd_e_filling_date)
        company_date = parse_date(r_company_date)

        company_address = AddressBase(
            address = c_address,
            address2 = c_address2,
            province=Province.objects.filter(id=c_province).first(),
            district=District.objects.filter(id=c_district).first(),
            subdistrict=Subdistrict.objects.filter(id=c_subdistrict).first(),
        )
        company_address.save()

        client = Client(
            code=c_code,
            company_name=c_company_name,
            tax_id=c_tax_id,
            service_fee=c_service_fee,
            create_client_date = date_c_create_client_date,
            channal=c_channal,
            detail=c_detail,
            contact=contact,
            status=c_status,
            register_tax=register_tax,
            company_address = company_address,
            file = file,
            create_by=request.user,
        )
        client.save()

        register_tax = RegisterTax(
            vat=r_vat,
            vat_date=date_vat,
            sbt=r_sbt,
            sbt_date=date_sbt,
            sso=r_sso,
            sso_date=date_sso,
            dbd_e_filling=r_dbd_e_filling,
            dbd_e_filling_date=date_dbd_e_filling,
            company=r_company,
            company_date=company_date,
            company_period_date=r_company_period_date,
        )
        register_tax.save()

        company_address.client = client
        company_address.save()

        client.file = file
        client.contact = contact
        client.register_tax = register_tax
        client.save()

        messages.success(request, 'บันทึกข้อมูลลูกค้าเรียบร้อยแล้ว')

        return redirect("taskcontrol:client_detail", client_id=client.id)
    return render(request, 'task/clients/create.html', {
        'subdistrict': subdistrict,
        'district': district,
        'province': province,
        'register_types': register_types,
    })

@login_required
def client_update(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    subdistrict = Subdistrict.objects.values('id', 'name_th', 'zipcode')
    district = District.objects.values('id', 'name_th')
    province = Province.objects.values('id', 'name_th').order_by('name_th')
    register_types = RegisterType.objects.values('id', 'short_name', 'name_th', 'name_en')

    if request.method == 'POST':
        existing_client = get_object_or_404(Client, id=client_id)

        update_c_code = request.POST.get('c_code', '')
        update_c_company_name = request.POST.get('c_company_name', '')
        update_c_tax_id = request.POST.get('c_tax_id', '')
        update_create_client_date = request.POST.get('c_create_client_date')
        update_c_service_fee = request.POST.get('c_service_fee')
        update_c_address = request.POST.get('c_address')
        update_c_address2 = request.POST.get('c_address2')
        update_c_province = request.POST.get('c_province')
        update_c_district = request.POST.get('c_district')
        update_c_subdistrict = request.POST.get('c_subdistrict')
        update_c_channal = request.POST.get('c_channal')
        update_c_detail = request.POST.get('c_detail')
        update_c_status = request.POST.get('c_status')

        if update_c_status == 'on':
            update_c_status = True
        else:
            update_c_status = False

        update_r_vat = request.POST.get('r_vat')
        update_r_vat_date = request.POST.get('r_vat_date')
        update_r_sbt = request.POST.get('r_sbt')
        update_r_sbt_date = request.POST.get('r_sbt_date')
        update_r_sso = request.POST.get('r_sso')
        update_r_sso_date = request.POST.get('r_sso_date')
        update_r_dbd_e_filling = request.POST.get('r_dbd_e_filling')
        update_r_dbd_e_filling_date = request.POST.get('r_dbd_e_filling_date')
        update_r_company = request.POST.get('r_company')
        update_r_company_date = request.POST.get('r_company_date')
        update_r_company_period_date = request.POST.get('r_company_period_date')

        date_vat = parse_date(update_r_vat_date)
        date_sbt = parse_date(update_r_sbt_date)
        date_sso = parse_date(update_r_sso_date)
        date_dbd_e_filling = parse_date(update_r_dbd_e_filling_date)
        date_company_date = parse_date(update_r_company_date)

        update_company_address, created = AddressBase.objects.update_or_create(
            id=existing_client.company_address.id,
            defaults={
                'address': update_c_address,
                'address2': update_c_address2,
                'province': Province.objects.filter(id=update_c_province).first(),
                'district': District.objects.filter(id=update_c_district).first(),
                'subdistrict': Subdistrict.objects.filter(id=update_c_subdistrict).first(),
            }
        )

        existing_client.code = update_c_code
        existing_client.company_name = update_c_company_name
        existing_client.tax_id = update_c_tax_id
        existing_client.service_fee = update_c_service_fee
        existing_client.create_client_date = update_create_client_date
        existing_client.channal = update_c_channal
        existing_client.detail = update_c_detail
        existing_client.status = update_c_status
        existing_client.company_address = update_company_address
        existing_client.update_by = request.user
        existing_client.save()

        update_register_tax, created = RegisterTax.objects.update_or_create(
            id=existing_client.register_tax.id,
            defaults={
                'vat': update_r_vat,
                'vat_date': date_vat,
                'sbt': update_r_sbt,
                'sbt_date': date_sbt,
                'sso': update_r_sso,
                'sso_date': date_sso,
                'dbd_e_filling': update_r_dbd_e_filling,
                'dbd_e_filling_date': date_dbd_e_filling,
                'company': update_r_company,
                'company_date': date_company_date,
                'company_period_date': update_r_company_period_date,
            }
        )

        existing_client.register_tax = update_register_tax
        existing_client.save()

        return redirect('taskcontrol:client_detail', client_id=existing_client.id)

    return render(request, 'task/clients/update.html', {
        'client': client,
        'subdistrict': subdistrict,
        'district': district,
        'province': province,
        'register_types': register_types,
    })

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    return redirect("taskcontrol:client_list")

@login_required
def update_password(request):
    pw_id = request.POST.get('update_id')
    updated_pw = get_object_or_404(ClientPassword, id=pw_id)
    updated_pw.type_password = get_object_or_404(RegisterType, id=request.POST.get('update_type_password_id'))
    updated_pw.username = request.POST.get('update_username')
    updated_pw.password = request.POST.get('update_password')
    updated_pw.save()

@login_required
def delete_password(request):
    pw_id = request.POST.get('delete_id')
    pw_to_delete = get_object_or_404(ClientPassword, id=pw_id)
    pw_to_delete.delete()

@login_required
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'task/clients/client_detail.html', {'client': client})

#TODO ClientPassword
@login_required
def password_list(request,client_id):
    client = get_object_or_404(Client, id=client_id)
    passwords = ClientPassword.objects.all()
    return render(request, 'task/clients/password_list.html', {'passwords': passwords,'client':client})

@login_required
def create_password(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    register_types = RegisterType.objects.all()
    passwords = ClientPassword.objects.filter(client=client)

    if request.method == 'POST':
        type_password_id = request.POST.get('type_password')
        username = request.POST.get('username')
        password_value = request.POST.get('password')

        password = ClientPassword(
            type_password=RegisterType.objects.filter(id=type_password_id).first(),
            username=username,
            password=password_value,
            client=client
        )
        password.create_by = request.user
        password.save()

        return redirect('taskcontrol:password_list', client_id=client.id)

    return render(request, 'task/clients/password_list.html', {'register_types': register_types, 'client': client, 'passwords': passwords})

@login_required
def update_password(request, password_id):
    register_types = RegisterType.objects.all()
    password_instance = get_object_or_404(ClientPassword, id=password_id)

    if request.method == 'POST':
        type_password_id = request.POST.get('type_password_id')
        username = request.POST.get('username')
        new_password = request.POST.get('password')

        password_instance.type_password = RegisterType.objects.filter(id=type_password_id).first()
        password_instance.username = username
        password_instance.password = new_password
        password_instance.update_by = request.user
        password_instance.save()

        return redirect('taskcontrol:password_list', client_id=password_instance.client.id)

    return render(request, 'task/clients/password_list.html', {'register_types': register_types, 'password': password_instance})

@login_required
def delete_password(request, password_id):
    password_instance = get_object_or_404(ClientPassword, id=password_id)

    if request.method == 'POST':
        password_instance.delete()
        return redirect('taskcontrol:password_list', client_id=password_instance.client.id)

    return render(request, 'task/clients/password_list.html', {'password': password_instance})

#TODO Fileclient
@login_required
def file_client_list(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    files = FileManage.objects.filter(client_id=client_id).all()
    return render(request, 'task/clients/file_client_list.html', {'client': client, 'files': files})

@login_required
def file_client_create(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    files = FileManage.objects.filter(client=client)

    if request.method == 'POST':
        c_file = request.FILES.get('c_file')
        c_description = request.POST.get('c_description')
        c_image = request.FILES.get('c_image')

        user = request.user
        file = FileManage(
            file_client=c_file,
            description=c_description,
            image_client=c_image,
            client=client,
            create_by=user,
        )
        file.save()
        return redirect('taskcontrol:file_client_list', client_id=client.id)

    return render(request, 'task/clients/file_client_list.html', {'client': client, 'files': files})

@login_required
def file_client_delete(request, file_id):
    file_to_delete = get_object_or_404(FileManage, id=file_id)

    if request.user != file_to_delete.create_by:
        return redirect('taskcontrol:file_client_list', client_id=file_to_delete.client.id)

    file_to_delete.delete()
    return redirect('taskcontrol:file_client_list', client_id=file_to_delete.client.id)

@login_required
def file_client_download_file(request, file_id):
    try:
        file_instance = FileManage.objects.get(pk=file_id)
        file_path = file_instance.file_client.path

        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{file_instance.file_client.name}"'
            return response

    except FileManage.DoesNotExist:
        raise Http404("File not found")
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Failed to download file: {e}")
        raise Http404("Failed to download file")

@login_required
def file_client_download_image(request, image_id):
    try:
        image_instance = FileManage.objects.get(pk=image_id)
        image_path = image_instance.image_client.path

        with open(image_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{image_instance.image_client.name}"'
            return response

    except FileManage.DoesNotExist:
        raise Http404("Image not found")
    except Exception as e:
        raise Http404("Failed to download image")

@login_required
def setting(request):
    return render(request,'task/main_setting/setting.html')

#TODO Contact
@login_required
def create_contact(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    subdistrict = Subdistrict.objects.values('id', 'name_th', 'zipcode')
    district = District.objects.values('id', 'name_th')
    province = Province.objects.values('id', 'name_th').order_by('name_th')
    contacts = Contact.objects.filter(client=client)
    company_address = Client.objects.values('company_address')

    if request.method == 'POST':
        ct_name = request.POST.get('ct_name')
        ct_position = request.POST.get('ct_position')
        ct_phone = request.POST.get('ct_phone')
        ct_email = request.POST.get('ct_email')
        ct_line = request.POST.get('ct_line')
        ct_other = request.POST.get('ct_other')
        ct_address = request.POST.get('ct_address')
        ct_address2 = request.POST.get('ct_address2')
        ct_province = request.POST.get('ct_province')
        ct_district = request.POST.get('ct_district')
        ct_subdistrict = request.POST.get('ct_subdistrict')

        contact_address = AddressBase(
            address=ct_address,
            address2=ct_address2,
            province=Province.objects.filter(id=ct_province).first(),
            district=District.objects.filter(id=ct_district).first(),
            subdistrict=Subdistrict.objects.filter(id=ct_subdistrict).first(),
        )
        contact_address.save()

        contact = Contact(
            client=client,
            name=ct_name,
            position=ct_position,
            phone=ct_phone,
            email=ct_email,
            line=ct_line,
            other=ct_other,
            address=contact_address,
        )
        contact.save()

        return redirect('taskcontrol:create_contact', client_id=contact.client.id)

    return render(request, 'task/clients/contact.html', {
        'client': client,
        'subdistrict': subdistrict,
        'district': district,
        'province': province,
        'contacts': contacts,
        'company_address': company_address,
    })

@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        if contact.address:
            contact.address.delete()
        contact.delete()
        return redirect('taskcontrol:create_contact', client_id=contact.client.id)

    return render(request, 'task/clients/contact.html', {'contact': contact})

# TODO Engagement
@login_required
def engagement_list(request):
    engagements = Engagement.objects.all()  # Add filters if needed
    engagement_details = EngagementDetail.objects.prefetch_related('engagement', 'engagement_category').all()
    total_engagements = engagements.count()
    open_engagements = engagements.filter(status='OPENJOB').count()
    closed_engagements = engagements.filter(status='DONE').count()

    return render(request, 'task/engagement/engagement_list.html', {
        'engagements': engagements,
        'engagement_details': engagement_details,
        'total_engagements': total_engagements,
        'open_engagements': open_engagements,
        'closed_engagements': closed_engagements,
    })

@login_required
def engagement_detail(request,engagement_id):
    engagements = get_object_or_404(Engagement, id=engagement_id)
    client_list = Client.objects.values('id','code','company_name')
    reviewers = get_user_model().objects.filter(is_superuser=True)
    approvers = get_user_model().objects.filter(is_superuser=True)
    return render(request,'task/engagement/engagement_detail.html', {
        'engagements': engagements,
        'client_list':client_list,
        'reviewers':reviewers,
        'approvers':approvers
    })

def get_engagement_type(request):
    category_id = request.POST.get('category_id')
    engagement_type = EngagementType.objects.filter(category=category_id).values('id', 'name_th')
    return JsonResponse(list(engagement_type), safe=False)

@login_required
def engagement_create(request):
    clients = Client.objects.values('id', 'code', 'company_name')
    reviewers = get_user_model().objects.filter(is_superuser=True)
    approvers = get_user_model().objects.filter(is_superuser=True)

    user = request.user

    if request.method == 'POST':
        client_id = request.POST.get('client')
        job_code = request.POST.get('job_code')
        start_date_service = request.POST.get('start_date_service')
        end_date_service = request.POST.get('end_date_service')
        start_date_period = request.POST.get('start_date_period')
        end_date_period = request.POST.get('end_date_period')
        approver_id = request.POST.get('approver', '')
        reviewer_id = request.POST.get('reviewer', '')
        category_id = request.POST.get('category_id')
        type_id = request.POST.get('type_id')

        sdate_service = parse_date(start_date_service)
        edate_service = parse_date(end_date_service)
        sdate_period = parse_date(start_date_period)
        edate_period = parse_date(end_date_period)

        client_instance = get_object_or_404(Client, id=client_id)

        approver_instance = None
        reviewer_instance = None

        if approver_id:
            approver_instance = get_object_or_404(get_user_model(), id=approver_id)

        if reviewer_id:
            reviewer_instance = get_object_or_404(get_user_model(), id=reviewer_id)

        if Engagement.objects.filter(job_code=job_code).exists():
            messages.error(request, f'รหัสงาน "{job_code}" มีอยู่แล้ว. โปรดใช้รหัสงานอื่น')
        else:
            with transaction.atomic():
                engagement = Engagement.objects.create(
                    client=client_instance,
                    job_code=job_code,
                    start_date_service=sdate_service,
                    end_date_service=edate_service,
                    start_date_period=sdate_period,
                    end_date_period=edate_period,
                    administrator=user,
                    approver=approver_instance,
                    reviewer=reviewer_instance,
                    status='OPENJOB',
                    create_by=user,
                    create_at=timezone.now(),
                    category_id=category_id,
                    type_id=type_id,
                    notes=None,
                )
            return redirect('taskcontrol:engagement_detail', engagement_id=engagement.id)

    return render(request, 'task/engagement/create.html', {
        'clients': clients,
        'user': user,
        'reviewers': reviewers,
        'approvers': approvers
    })

@login_required
def engagement_update(request, engagement_id):
    engagement = get_object_or_404(Engagement, id=engagement_id)
    clients = Client.objects.values('id', 'code', 'company_name')
    engagements = Engagement.objects.all()
    reviewers = get_user_model().objects.filter(is_superuser=True)
    approvers = get_user_model().objects.filter(is_superuser=True)

    user = request.user

    if request.method == 'POST':
        existing_engagement = get_object_or_404(Engagement, id=engagement_id)

        client_id = request.POST.get('client')
        client_instance = None

        if client_id:
            client_instance = get_object_or_404(Client, id=client_id)
            existing_engagement.client = client_instance

        e_start_date_service = request.POST.get('start_date_service')
        e_end_date_service = request.POST.get('end_date_service')
        e_start_date_period = request.POST.get('start_date_period')
        e_end_date_period = request.POST.get('end_date_period')

        status = request.POST.get('status')
        existing_engagement.status = status

        approver_id = request.POST.get('approver')
        reviewer_id = request.POST.get('reviewer')

        if status == 'on':
            existing_engagement.status = 'OPENJOB'
        else:
            existing_engagement.status = 'DONE'

        start_date_service = parse_date(e_start_date_service)
        end_date_service = parse_date(e_end_date_service)
        start_date_period = parse_date(e_start_date_period)
        end_date_period = parse_date(e_end_date_period)

        approver_instance = get_object_or_404(get_user_model(), id=approver_id)
        reviewer_instance = get_object_or_404(get_user_model(), id=reviewer_id)

        existing_engagement.client = client_instance
        existing_engagement.start_date_service = start_date_service
        existing_engagement.end_date_service = end_date_service
        existing_engagement.start_date_period = start_date_period
        existing_engagement.end_date_period = end_date_period
        existing_engagement.approver = approver_instance
        existing_engagement.reviewer = reviewer_instance
        existing_engagement.update_by = user
        existing_engagement.update_at = timezone.now()
        existing_engagement.save()

        return redirect('taskcontrol:engagement_detail', engagement_id=existing_engagement.id)

    return render(request, 'task/engagement/update.html', {
        'clients': clients,
        'engagement': engagement,
        'engagements': engagements,
        'reviewers': reviewers,
        'approvers': approvers
    })


@login_required
def engagement_delete(request, engagement_id):
    engagement = get_object_or_404(Engagement, id=engagement_id)
    engagement.delete()
    messages.success(request, 'ลบรายการนี้เรียบร้อย.')
    return redirect("taskcontrol:engagement_list")

#TODO FileEngagement
@login_required
def file_engagement_list(request, engagement_id):
    engagement = get_object_or_404(Engagement, id=engagement_id)
    files = FileManage.objects.filter(engagement=engagement)
    context = {'engagement': engagement, 'files': files, 'engagement_id': engagement_id}
    return render(request, 'task/engagement/file_engagement_list.html', context)

@login_required
def file_engagement_create(request, engagement_id):
    engagement = get_object_or_404(Engagement, id=engagement_id)
    files = FileManage.objects.filter(engagement=engagement)

    if request.method == 'POST':
        c_file = request.FILES.get('c_file')
        c_description = request.POST.get('c_description')
        c_image = request.FILES.get('c_image')

        user = request.user

        file = FileManage(
            file_engagement=c_file,
            description=c_description,
            image_engagement=c_image,
            engagement=engagement,
            create_by=user,
        )
        file.save()
        return redirect('taskcontrol:file_engagement_list', engagement_id=engagement.id)
    
    return render(request, 'task/engagement/file_engagement_list.html', {'engagement': engagement, 'files': files})

@login_required
def file_engagement_delete(request, file_id):
    file_to_delete = get_object_or_404(FileManage, id=file_id)

    if request.user != file_to_delete.create_by:
        return redirect('taskcontrol:file_engagement_list', engagement_id=file_to_delete.engagement.id)

    file_to_delete.delete()
    return redirect('taskcontrol:file_engagement_list', engagement_id=file_to_delete.engagement.id)

@login_required
def file_engagement_file_client_download_file(request, file_id):
    try:
        file_instance = FileManage.objects.get(pk=file_id)
        file_path = file_instance.file_engagement.path

        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{file_instance.file_engagement.name}"'
            return response

    except FileManage.DoesNotExist:
        raise Http404("File not found")
    except Exception as e:
        print(f"Failed to download file: {e}")
        raise Http404("Failed to download file")

@login_required
def file_engagement_file_client_download_image(request, image_id):
    try:
        image_instance = FileManage.objects.get(pk=image_id)
        image_path = image_instance.image_engagement.path

        with open(image_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{image_instance.image_engagement.name}"'
            return response

    except FileManage.DoesNotExist:
        raise Http404("Image not found")
    except Exception as e:
        raise Http404("Failed to download image")

#TODO MainSetting
@login_required
def category(request):
    engagement_categories = EngagementCategory.objects.all()
    engagement_types = EngagementType.objects.all()
    return render(request, 'task/main_setting/category.html', {'engagement_categories': engagement_categories, 'engagement_types': engagement_types})

@login_required
def create_category(request):
    user = request.user
    if request.method == 'POST':
        category_name_th = request.POST.get('category_name_th')

        engagement_category = EngagementCategory(
            name_th=category_name_th,
            create_by=user,
            create_at=timezone.now(),
        )
        engagement_category.save()
        return redirect('taskcontrol:category')

    return render(request, 'task/main_setting/create_category.html')

@login_required
def create_type(request):
    user = request.user
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        type_name_th = request.POST.get('type_name_th')

        if category_id and type_name_th:
            category = EngagementCategory.objects.get(id=category_id)
            engagement_type = EngagementType.objects.create(name_th=type_name_th, category=category, create_by=user, create_at=timezone.now())
            return redirect('taskcontrol:category')

    engagement_categories = EngagementCategory.objects.all()
    return render(request, 'task/main_setting/create_type.html', {'engagement_categories': engagement_categories})

#TODO EngagementDetail

@login_required
def engagement_detail_list(request):
    engagement_detail_lists = EngagementDetail.objects.all()
    return render(request,'task/engagement/create_engagement_detail.html', {'engagement_detail_lists': engagement_detail_lists})

@login_required
def engagement_detail_create(request, engagement_id):
    engagement = get_object_or_404(Engagement, id=engagement_id)
    categories = EngagementCategory.objects.all()
    types = EngagementType.objects.all()
    reviewers = get_user_model().objects.filter(is_superuser=True)
    approvers = get_user_model().objects.filter(is_superuser=True)

    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        type_id = request.POST.get('type_id')
        type_name = request.POST.get('type')
        deadline = request.POST.get('deadline')
        notification = request.POST.get('notification')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        review_by = request.POST.get('review_by')
        approved_by = request.POST.get('approved_by')

        job_start_date = parse_date(start_date)
        job_end_date = parse_date(end_date)

        review_by = review_by == 'on'
        approved_by = approved_by == 'on'

        engagement_category_instance = get_object_or_404(EngagementCategory, id=category_id)
        engagement_type_instance = get_object_or_404(EngagementType, id=type_id)

        engagement.category = engagement_category_instance
        engagement.type = engagement_type_instance
        engagement.save()

        engagement_detail = EngagementDetail.objects.create(
            engagement=engagement,
            engagement_category=engagement_category_instance,
            engagement_type=engagement_type_instance,
            type=type_name,
            deadline=deadline,
            notification=notification,
            start_date=job_start_date,
            end_date=job_end_date,
            review_by=review_by,
            approved_by=approved_by,
            create_by=request.user,
            create_at=timezone.now(),
        )

        return redirect('taskcontrol:engagement_detail_create', engagement_id=engagement_id)
    
    engagement_detail_lists = EngagementDetail.objects.filter(engagement=engagement).all()

    return render(request, 'task/engagement/create_engagement_detail.html', {
        'categories': categories,
        'types': types,
        'reviewers': reviewers,
        'approvers': approvers,
        'engagement_detail_lists': engagement_detail_lists,
        'engagement': engagement,
    })

@login_required
def engagement_detail_delete(request, engagement_detail_id):
    engagement_detail = get_object_or_404(EngagementDetail, id=engagement_detail_id)
    engagement_detail.delete()
    messages.success(request, 'ลบรายการนี้เรียบร้อย.')
    return redirect("taskcontrol:engagement_detail_create")

#TODO Dashboard
@login_required
def get_engagement_data(request):
    engagement_data = Engagement.objects.all()
    date_counts = Counter(data.create_at.strftime('%Y-%m-%d') for data in engagement_data)
    
    dates = list(date_counts.keys())
    engagement_counts = list(date_counts.values())
    
    response_data = {
        'dates': dates,
        'engagement_counts': engagement_counts
    }

    return JsonResponse(response_data)

# @login_required
# def dashboard(request):
#     clients = Client.objects.all().order_by('code')
#     total_clients = clients.count()

#     engagements = Engagement.objects.all()
#     engagement_details = EngagementDetail.objects.all()
#     total_engagements = engagements.count()
#     open_job_engagement = engagements.filter(status='OPENJOB').count()
#     done_job_engagement = engagements.filter(status='DONE').count()

#     category = EngagementCategory.objects.all()
#     type = EngagementType.objects.all()

#     engagement_detail_deadlines = EngagementDetail.objects.filter(engagement__in=engagements).values('id', 'deadline')

#     deadlines = [item['deadline'] for item in engagement_detail_deadlines]
#     formatted_dates = []
#     for date_obj in deadlines:
#         formatted_date = date_obj.strftime("%Y-%m-%d")
#         formatted_dates.append(formatted_date)

#     today = date.today()

#     date_deadlines = []
#     for formatted_date in formatted_dates:
#         deadline_date = datetime.strptime(formatted_date, "%Y-%m-%d").date()
#         difference = deadline_date - today
#         date_deadlines.append(difference.days)

#     return render(request, 'task/dashboard.html', {
#         'clients': clients,
#         'total_clients': total_clients,
#         'engagements': engagements,
#         'engagement_details': engagement_details,
#         'total_engagements': total_engagements,
#         'open_job_engagement': open_job_engagement,
#         'done_job_engagement': done_job_engagement,
#         'date_deadlines': date_deadlines,
#         'category': category,
#         'type': type,
#     })

# @login_required
# def search_datatable(request):
#     # รับค่าพารามิเตอร์จากคำขอ GET
#     client_id = request.GET.get('client_id')
#     start_date_period = request.GET.get('start_date_period')
#     to_date_period = request.GET.get('to_date_period')
#     category_id = request.GET.get('category_id')
#     type_id = request.GET.get('type_id')
#     deadline_days = request.GET.get('deadline_days')
#     per_month = request.GET.get('per_month')


#     engagements = Engagement.objects.all().order_by('job_code')

#     if client_id:
#         engagements = engagements.filter(client_id=client_id)
#     if start_date_period:
#         engagements = engagements.filter(start_date_period__gte=start_date_period)
#     if to_date_period:
#         engagements = engagements.filter(end_date_period__lte=to_date_period)
#     if category_id:
#         engagements = engagements.filter(category_id=category_id)
#     if type_id:
#         engagements = engagements.filter(type_id=type_id)

#     if deadline_days:
#         today = timezone.now().date()
#         engagements_with_deadlines = EngagementDetail.objects.filter(deadline__gt=today, deadline__lte=F('engagement__end_date_period')).values('engagement_id')
#         engagements = engagements.filter(id__in=Subquery(engagements_with_deadlines))

#     if per_month:  # เพิ่มเงื่อนไขสำหรับกรองตามเดือนปัจจุบัน
#         current_month = datetime.now().month
#         current_year = datetime.now().year
#         engagements = engagements.filter(start_date_period__month=current_month, start_date_period__year=current_year)

#     engagement_data = []

#     for engagement in engagements:
#         engagement_detail = EngagementDetail.objects.filter(engagement=engagement)

#         remaining_days = []
#         for detail in engagement_detail:
#             difference = detail.deadline - date.today()
#             remaining_days.append(difference.days)

#         engagement_data.append({
#             'job_code': engagement.job_code,
#             'client_id': engagement.client_id,
#             'client__company_name': engagement.client.company_name,
#             'start_date_period': engagement.start_date_period,
#             'administrator__first_name': engagement.administrator.first_name,
#             'administrator__last_name': engagement.administrator.last_name,
#             'type__name_th': engagement.type.name_th if engagement.type else None,
#             'engagement_detail_deadlines': list(engagement_detail.values('id', 'deadline')),
#             'remaining_days': remaining_days,
#         })

#     return JsonResponse(engagement_data, safe=False)


@login_required
def dashboard(request):
    # Retrieve data from the database
    clients = Client.objects.all().order_by('code')
    total_clients = clients.count()
    engagements = Engagement.objects.all()
    engagement_details = EngagementDetail.objects.all()
    total_engagements = engagements.count()
    open_job_engagement = engagements.filter(status=STATUS_OPEN_JOB).count()
    done_job_engagement = engagements.filter(status=STATUS_DONE).count()
    category = EngagementCategory.objects.all()
    engagement_types = EngagementType.objects.all()

    # Process data as needed

    return render(request, 'task/dashboard.html', {
        'clients': clients,
        'total_clients': total_clients,
        'engagements': engagements,
        'engagement_details': engagement_details,
        'total_engagements': total_engagements,
        'open_job_engagement': open_job_engagement,
        'done_job_engagement': done_job_engagement,
        'category': category,
        'engagement_types': engagement_types,
    })

@login_required
def search_datatable(request):
    client_id = request.GET.get('client_id')
    start_date_period = request.GET.get('start_date_period')
    to_date_period = request.GET.get('to_date_period')
    category_id = request.GET.get('category_id')
    type_id = request.GET.get('type_id')
    deadline_days = request.GET.get('deadline_days')
    per_month = request.GET.get('per_month')

    # Retrieve engagements from the database and filter based on query parameters
    engagements = Engagement.objects.all().order_by('job_code')
    if client_id:
        engagements = engagements.filter(client_id=client_id)
    if start_date_period:
        engagements = engagements.filter(start_date_period__gte=start_date_period)
    if to_date_period:
        engagements = engagements.filter(end_date_period__lte=to_date_period)
    if category_id:
        engagements = engagements.filter(category_id=category_id)
    if type_id:
        engagements = engagements.filter(type_id=type_id)
    if deadline_days:
        today = timezone.now().date()
        engagements_with_deadlines = EngagementDetail.objects.filter(deadline__gt=today, deadline__lte=F('engagement__end_date_period')).values('engagement_id')
        engagements = engagements.filter(id__in=Subquery(engagements_with_deadlines))
    if per_month:
        current_month = datetime.now().month
        current_year = datetime.now().year
        engagements = engagements.filter(start_date_period__month=current_month, start_date_period__year=current_year)

    # Process engagements data
    engagement_data = []
    for engagement in engagements:
        engagement_detail = EngagementDetail.objects.filter(engagement=engagement)
        remaining_days = [(detail.deadline - date.today()).days for detail in engagement_detail]
        engagement_data.append({
            'job_code': engagement.job_code,
            'client_id': engagement.client_id,
            'client__company_name': engagement.client.company_name,
            'start_date_period': engagement.start_date_period,
            'administrator__first_name': engagement.administrator.first_name,
            'administrator__last_name': engagement.administrator.last_name,
            'type__name_th': engagement.type.name_th if engagement.type else None,
            'engagement_detail_deadlines': list(engagement_detail.values('id', 'deadline')),
            'remaining_days': remaining_days,
        })

    # Return JSON response
    return JsonResponse(engagement_data, safe=False)


@login_required
def get_engagement_summary(request):
    status_counts = Engagement.objects.values('status').annotate(count=Count('status'))

    labels = ['เปิดงาน', 'กำลังดำเนินการ', 'รอตรวจทาน', 'รอลูกค้า', 'เรียบร้อย']
    counts = [0, 0, 0, 0, 0]

    total_engagement = Engagement.objects.count()
    for status_count in status_counts:
        status = status_count['status']
        if status == 'OPENJOB':
            counts[0] = status_count['count']
        elif status == 'IN_PROGRESS':
            counts[1] = status_count['count']
        elif status == 'REVIEW':
            counts[2] = status_count['count']
        elif status == 'PENDINGCLIENT':
            counts[3] = status_count['count']
        elif status == 'DONE':
            counts[4] = status_count['count']

    percentages = [count / total_engagement * 100 if total_engagement != 0 else 0 for count in counts]

    total_percentages = sum(percentages)
    if total_percentages != 100:
        diff = 100 - total_percentages
        max_count_index = percentages.index(max(percentages))
        counts[max_count_index] += diff
        percentages[max_count_index] += diff

    data = {
        'labels': labels,
        'counts': counts,
        'percentages': percentages,
        'total_counts': total_engagement,
        'total_percentage': 100
    }
    return JsonResponse(data)

@login_required
def get_engagement_accounting(request):
    # Get counts for each engagement type
    accounting_counts = EngagementType.objects.values('name_th').annotate(count=Count('name_th'))

    # Initialize counts for each type of engagement
    counts = [0, 0, 0]

    # Iterate through counts and update the appropriate index
    for entry in accounting_counts:
        name_th = entry['name_th']
        count = entry['count']
        if name_th == 'บันทึกบัญชี':
            counts[0] = count
        elif name_th == 'ตามเอกสาร':
            counts[1] = count
        elif name_th == 'เก็บเอกสาร':
            counts[2] = count

    # Calculate percentages
    total_type_accounting = sum(counts)
    percentages = [count / total_type_accounting * 100 if total_type_accounting != 0 else 0 for count in counts]

    # Ensure percentages sum up to 100
    total_percentages = sum(percentages)
    if total_percentages != 100:
        diff = 100 - total_percentages
        max_count_index = percentages.index(max(percentages))
        counts[max_count_index] += diff
        percentages[max_count_index] += diff

    # Prepare data for JSON response
    data = {
        'labels': ['บันทึกบัญชี', 'ตามเอกสาร', 'เก็บเอกสาร'],
        'counts': counts,
        'percentages': percentages,
        'total_type_accounting': total_type_accounting,
        'total_percentage': 100
    }
    return JsonResponse(data)

#TODO Kanban
@login_required
def kanban_board(request):
    engagements = Engagement.objects.all()
    engagement_details = EngagementDetail.objects.all()
    administrators = get_user_model().objects.all()
    type = EngagementType.objects.all()

    engagement_detail_deadlines = EngagementDetail.objects.filter(engagement__in=engagements).values('id', 'deadline')

    deadlines = [item['deadline'] for item in engagement_detail_deadlines]
    formatted_dates = []
    for date_obj in deadlines:
        formatted_date = date_obj.strftime("%Y-%m-%d")
        formatted_dates.append(formatted_date)

    today = date.today()

    date_deadlines = []
    for formatted_date in formatted_dates:
        deadline_date = datetime.strptime(formatted_date, "%Y-%m-%d").date()
        difference = deadline_date - today
        date_deadlines.append(difference.days)

    return render(request, 'task/kanban/board.html', {
        'engagements': engagements,
        'engagement_details': engagement_details,
        'administrators': administrators,
        'type': type,
        'date_deadlines': date_deadlines,
    })

@login_required
def filter_engagement_details(request):
    if request.method == 'GET':
        deadline_days = request.GET.get('deadline_days')
        administrator_id = request.GET.get('administrator_id')
        type_id = request.GET.get('type_id')
        per_month = request.GET.get('per_month')

        engagements = Engagement.objects.all().order_by('job_code')

        if administrator_id:
            engagements = engagements.filter(administrator_id=administrator_id)
        if type_id:
            engagements = engagements.filter(type_id=type_id)

        if deadline_days:
            today = timezone.now().date()
            engagements_with_deadlines = EngagementDetail.objects.filter(deadline__gt=today, deadline__lte=F('engagement__end_date_period')).values('engagement_id')
            engagements = engagements.filter(id__in=Subquery(engagements_with_deadlines))

        if per_month:
            current_month = timezone.now().month
            current_year = timezone.now().year
            engagements = engagements.filter(start_date_period__month=current_month, start_date_period__year=current_year)

        engagement_data = []

        for engagement in engagements:
            try:
                engagement_detail = EngagementDetail.objects.filter(engagement=engagement).first()
                deadline = engagement_detail.deadline.strftime("%d/%m/%Y") if engagement_detail else ''
            except ObjectDoesNotExist:
                deadline = ''

            reviewer_name = f"{engagement.reviewer.first_name} {engagement.reviewer.last_name}" if engagement.reviewer else ''
            approver_name = f"{engagement.approver.first_name} {engagement.approver.last_name}" if engagement.approver else ''

            engagement_data.append({
                'create_at': engagement.create_at.strftime("%d/%m/%Y"),
                'job_code': engagement.job_code,
                'type_name_th': engagement.type.name_th if engagement.type else '',
                'reviewer': reviewer_name,
                'approver': approver_name,
                'administrator': f"{engagement.administrator.first_name} {engagement.administrator.last_name}",
                'deadline': deadline,
                'status': engagement.status,
            })

        return JsonResponse(engagement_data, safe=False)

@login_required
def get_engagement_details(request):
    if request.method == 'GET':
        job_code = request.GET.get('job_code')
        engagement = get_object_or_404(Engagement, job_code=job_code)
        engagement_details = EngagementDetail.objects.filter(engagement=engagement)

        modal_content = ""

        for engagement_detail in engagement_details:
            reviewer_name = f"{engagement.reviewer.first_name} {engagement.reviewer.last_name}" if engagement.reviewer else ''
            approver_name = f"{engagement.approver.first_name} {engagement.approver.last_name}" if engagement.approver else ''
            administrator_name = f"{engagement.administrator.first_name} {engagement.administrator.last_name}" if engagement.administrator else ''

            modal_content += f"""
            <form action="">
                <div class="row">
                    <div class="col-md-3">
                        <p class="fw-semibold">ชื่อลูกค้า :</p>
                    </div>
                    <div class="col-md-4">
                        {engagement.client.company_name if engagement.client else ''}
                    </div>

                    <div class="col-md-2">
                        <p class="fw-semibold">ผู้ตรวจทาน :</p>
                    </div>
                    <div class="col-md-3">
                        {reviewer_name}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-3">
                        <p class="fw-semibold">ประเภทงาน :</p>
                    </div>
                    <div class="col-md-4">
                        {engagement.category.name_th if engagement.category else ''} 
                        <i class="fa-solid fa-angle-right"></i> 
                        {engagement.type.name_th if engagement.type else ''}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-3">
                        <p class="fw-semibold">ผู้อนุมัติ :</p>
                    </div>
                    <div class="col-md-9">
                        {approver_name}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-3">
                        <p class="fw-semibold">ผู้รับผิดชอบ :</p>
                    </div>
                    <div class="col-md-9">
                        {administrator_name}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-3">
                        <p class="fw-semibold">รอบบัญชี (Period) :</p>
                    </div>
                    <div class="col-md-9">
                        {engagement.start_date_period.strftime('%d/%m/%Y') if engagement.start_date_period else ''}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-3">
                        <p class="fw-semibold">วันที่เปิดงาน :</p>
                    </div>
                    <div class="col-md-4">
                        {engagement.create_at.strftime('%d/%m/%Y') if engagement.create_at else ''}
                    </div>
                    <div class="col-md-2">
                        <p class="fw-semibold" style="color: tomato;">เดดไลน์ :</p>
                    </div>
                    <div class="col-md-3">
                        {engagement_detail.deadline.strftime('%d/%m/%Y') if engagement_detail.deadline else ''}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-3">
                        <p class="fw-semibold">หมายเหตุ (เพิ่มเติม) :</p>
                    </div>
                    <div class="col-md-9">
                        {engagement.notes if engagement.notes else ''}
                    </div>
                </div>
            </form>
        """

        return JsonResponse({'modal_content': modal_content})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
@login_required
def update_engagement_status(request):
    if request.method == 'POST':
        engagement_id = request.POST.get('engagement_id')
        new_status = request.POST.get('new_status')
        engagement = get_object_or_404(Engagement, pk=engagement_id)
        engagement.status = new_status
        engagement.save()

        Task.objects.create(
            engagement=engagement,
            status=new_status,
        )
        return redirect('taskcontrol:kanban_board')
    
@login_required
def update_engagement_notes(request):
    if request.method == 'POST':
        engagement_id = request.POST.get('engagement_id')
        new_notes = request.POST.get('new_notes')
        
        if not (engagement_id and new_notes):
            return HttpResponseBadRequest("Invalid data")

        engagement = get_object_or_404(Engagement, pk=engagement_id)

        # อัปเดตฟิลด์ notes เท่านั้น
        engagement.notes = new_notes
        engagement.save(update_fields=['notes'])
        
        return redirect('taskcontrol:kanban_board')
