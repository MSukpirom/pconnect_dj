from django.db import models
from django.conf import settings
from django.utils import timezone

class Country(models.Model):
    name_th =  models.CharField(max_length=255, default=None, null=True, blank=True)
    name_en =  models.CharField(max_length=255, default=None, null=True, blank=True)

    class Meta:
        db_table = 'country'

class Geography(models.Model):
    name_th =  models.CharField(max_length=255, default=None, null=True, blank=True)
    name_en =  models.CharField(max_length=255, default=None, null=True, blank=True)

    class Meta:
        db_table = 'geography'

class AddressBase(models.Model):
    address = models.CharField(max_length=255, default=None, null=True, blank=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey('District', on_delete=models.CASCADE, blank=True, null=True)
    subdistrict = models.ForeignKey('Subdistrict', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, blank=True, null=True, related_name='client_addressbase')
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, blank=True, null=True, related_name='contact_addressbase')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)
    voided_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'address_base'

class Client(models.Model):
    code = models.CharField(max_length=255, unique=True, default=None, null=True, blank=True)
    company_name = models.CharField(max_length=255, default=None, null=True, blank=True)
    tax_id = models.CharField(max_length=255, default=None, null=True, blank=True)
    service_fee = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    create_client_date = models.DateField(blank=True, null=True)
    channal = models.CharField(max_length=255, default=None, null=True, blank=True)
    detail = models.CharField(max_length=255, default=None, null=True, blank=True)
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, blank=True, null=True, related_name='client_contact')
    status = models.BooleanField(default=False)
    register_tax = models.ForeignKey('RegisterTax', on_delete=models.CASCADE, blank=True, null=True, related_name='client_register_tax')
    company_address = models.ForeignKey(AddressBase, on_delete=models.CASCADE, blank=True, null=True, related_name='client_company_address')
    file = models.ForeignKey('FileManage', on_delete=models.CASCADE, blank=True, null=True, related_name='client_file')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)
    voided_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'client'

class FileManage(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    file_client = models.FileField(upload_to='files/client/', null=True, max_length=255, blank=True)
    image_client = models.ImageField(upload_to='images/client/', null=True, blank=True)
    engagement = models.ForeignKey('Engagement', on_delete=models.CASCADE, blank=True, null=True)
    file_engagement = models.FileField(upload_to='files/engagement/', null=True, max_length=255, blank=True)
    image_engagement = models.ImageField(upload_to='images/engagement/', null=True, blank=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, blank=True, null=True)
    file_task = models.FileField(upload_to='files/task/', null=True, max_length=255, blank=True)
    image_task = models.ImageField(upload_to='images/task/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)
    voided_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'file_manage'

class Province(models.Model):
    name_th =  models.CharField(max_length=255, default=None, null=True, blank=True)
    name_en =  models.CharField(max_length=255, default=None, null=True, blank=True)
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE, blank=True, null=True, related_name='provinces')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name='provinces')

    class Meta:
        db_table = 'province'

class District(models.Model):
    name_th =  models.CharField(max_length=255, default=None, null=True, blank=True)
    name_en =  models.CharField(max_length=255, default=None, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True, related_name='districts')

    class Meta:
        db_table = 'district'

class Subdistrict(models.Model):
    name_th =  models.CharField(max_length=255, default=None, null=True, blank=True)
    name_en =  models.CharField(max_length=255, default=None, null=True, blank=True)
    zipcode = models.PositiveIntegerField()
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'subdistrict'

class RegisterTax(models.Model):
    vat = models.CharField(max_length=255, default=None, null=True, blank=True)
    vat_date = models.DateField(blank=True, null=True)
    sbt = models.CharField(max_length=255, default=None, null=True, blank=True)
    sbt_date = models.DateField(blank=True, null=True)
    sso = models.CharField(max_length=255, default=None, null=True, blank=True)
    sso_date = models.DateField(blank=True, null=True)
    dbd_e_filling = models.CharField(max_length=255, default=None, null=True, blank=True)
    dbd_e_filling_date = models.DateField(blank=True, null=True)
    company = models.CharField(max_length=255, default=None, null=True, blank=True)
    company_date = models.DateField(blank=True, null=True)
    company_period_date = models.CharField(max_length=255, default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'register_tax'

class RegisterType(models.Model):
    short_name = models.CharField(max_length=255, default=None, null=True, blank=True)
    name_th =  models.CharField(max_length=255, default=None, null=True, blank=True)
    name_en =  models.CharField(max_length=255, default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'register_type'

class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contact_client')
    name = models.CharField(max_length=255, default=None, null=True, blank=True)
    position = models.CharField(max_length=255, default=None, null=True, blank=True)
    phone = models.CharField(max_length=255, default=None, null=True, blank=True)
    email = models.EmailField(default=None, null=True, blank=True)
    line = models.CharField(max_length=255, default=None, null=True, blank=True)
    other = models.CharField(max_length=255, default=None, null=True, blank=True)
    address = models.ForeignKey(AddressBase, on_delete=models.CASCADE, blank=True, null=True, related_name='contact_address')
    address2 = models.ForeignKey(AddressBase, on_delete=models.CASCADE, blank=True, null=True, related_name='company_address')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)
    voided_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'contact'

class ClientPassword(models.Model):
    client = models.ForeignKey('Client', null=True, blank=True, on_delete=models.CASCADE)
    type_password = models.ForeignKey('RegisterType', null=True, blank=True, on_delete=models.CASCADE)
    username =  models.CharField(max_length=255, default=None, null=True, blank=True)
    password = models.TextField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'client_password'

class Engagement(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    job_code = models.CharField(max_length=255, unique=True)
    start_date_service = models.DateField()
    end_date_service = models.DateField()
    start_date_period = models.DateField()
    end_date_period = models.DateField()
    administrator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_engagements')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approver_engagements',null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviewer_engagements',null=True, blank=True)
    review_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default=None, null=True, blank=True)
    file = models.ForeignKey('FileManage', on_delete=models.CASCADE, related_name='engagement_file', null=True, blank=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='engagement_create_by')
    create_at = models.DateTimeField(auto_now_add=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='engagement_update_by')
    update_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('EngagementCategory', on_delete=models.CASCADE, related_name='engagement_category', null=True, blank=True)
    type = models.ForeignKey('EngagementType', on_delete=models.CASCADE, related_name='engagement_type', null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)
    voided_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'engagement'

    def update_status(self):
        # นับจำนวน Task ที่เป็นแต่ละสถานะ
        open_jobs = self.task_set.filter(status='OPEN JOB').count()
        in_progress = self.task_set.filter(status='IN PROGRESS').count()
        review = self.task_set.filter(status='REVIEW').count()
        pending_client = self.task_set.filter(status='PENDING CLIENT').count()
        done = self.task_set.filter(status='DONE').count()

        # กำหนดสถานะ Engagement ตามสถานะของ Task
        if done > 0:
            self.status = 'DONE'
        elif pending_client > 0:
            self.status = 'PENDING CLIENT'
        elif review > 0:
            self.status = 'REVIEW'
        elif in_progress > 0:
            self.status = 'IN PROGRESS'
        else:
            self.status = 'OPEN JOB'

        # บันทึกการเปลี่ยนแปลง
        self.save()

class EngagementCategory(models.Model):
    name_th = models.CharField(max_length=255, default=None, null=True, blank=True)
    name_en = models.CharField(max_length=255, default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'engagement_category'

class EngagementDetail(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    engagement_category = models.ForeignKey('EngagementCategory', on_delete=models.CASCADE, related_name='engagement_detail_category', null=True, blank=True)
    engagement_type = models.ForeignKey('EngagementType', on_delete=models.CASCADE, related_name='engagement_detail_type', null=True, blank=True)
    type = models.CharField(max_length=255, default=None, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    notification = models.CharField(max_length=255, default=None, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    review_by = models.BooleanField(default=False)
    approved_by = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)
    voided_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'engagement_detail'
        
class EngagementType(models.Model):
    name_th = models.CharField(max_length=255, default=None, null=True, blank=True)
    name_en = models.CharField(max_length=255, default=None, null=True, blank=True)
    description = models.CharField(max_length=255, default=None, null=True, blank=True)
    category = models.ForeignKey(EngagementCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'engagement_type'

class Task(models.Model):
    OPENJOB = 'OPEN JOB'
    IN_PROGRESS = 'IN PROGRESS'
    REVIEW = 'REVIEW'
    PENDINGCLIENT = 'PENDING CLIENT'
    DONE = 'DONE'

    STATUS_CHOICES = [
        (OPENJOB, 'Open Job'),
        (IN_PROGRESS, 'In Progress'),
        (REVIEW, 'Review'),
        (PENDINGCLIENT, 'Pending Client'),
        (DONE, 'Done'),
    ]
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OPENJOB)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)
    voided_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'task'

    def update_engagement_status(self):
        if self.status != Task.OPENJOB:
            engagement = self.engagement
            engagement.status = self.status
            engagement.save()