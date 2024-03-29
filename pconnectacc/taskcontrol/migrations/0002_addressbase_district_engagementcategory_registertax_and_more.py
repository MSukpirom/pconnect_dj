# Generated by Django 5.0.3 on 2024-03-29 06:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskcontrol', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('voided_at', models.DateTimeField(blank=True, null=True)),
                ('voided_by', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'address_base',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_th', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, default=None, max_length=255, null=True)),
            ],
            options={
                'db_table': 'district',
            },
        ),
        migrations.CreateModel(
            name='EngagementCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_th', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engagement_category',
            },
        ),
        migrations.CreateModel(
            name='RegisterTax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vat', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('vat_date', models.DateField(blank=True, null=True)),
                ('sbt', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('sbt_date', models.DateField(blank=True, null=True)),
                ('sso', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('sso_date', models.DateField(blank=True, null=True)),
                ('dbd_e_filling', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('dbd_e_filling_date', models.DateField(blank=True, null=True)),
                ('company', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('company_date', models.DateField(blank=True, null=True)),
                ('company_period_date', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'register_tax',
            },
        ),
        migrations.CreateModel(
            name='RegisterType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_th', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'register_type',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default=None, max_length=255, null=True, unique=True)),
                ('company_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('tax_id', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('service_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
                ('create_client_date', models.DateField(blank=True, null=True)),
                ('channal', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('detail', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('voided_at', models.DateTimeField(blank=True, null=True)),
                ('voided_by', models.IntegerField(blank=True, null=True)),
                ('company_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_company_address', to='taskcontrol.addressbase')),
            ],
            options={
                'db_table': 'client',
            },
        ),
        migrations.AddField(
            model_name='addressbase',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_addressbase', to='taskcontrol.client'),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('position', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('line', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('other', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('voided_at', models.DateTimeField(blank=True, null=True)),
                ('voided_by', models.IntegerField(blank=True, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_address', to='taskcontrol.addressbase')),
                ('address2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_address', to='taskcontrol.addressbase')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_client', to='taskcontrol.client')),
            ],
            options={
                'db_table': 'contact',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_contact', to='taskcontrol.contact'),
        ),
        migrations.AddField(
            model_name='addressbase',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_addressbase', to='taskcontrol.contact'),
        ),
        migrations.AddField(
            model_name='addressbase',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.district'),
        ),
        migrations.CreateModel(
            name='Engagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_code', models.CharField(max_length=255, unique=True)),
                ('start_date_service', models.DateField()),
                ('end_date_service', models.DateField()),
                ('start_date_period', models.DateField()),
                ('end_date_period', models.DateField()),
                ('approved_date', models.DateTimeField(blank=True, null=True)),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('voided_at', models.DateTimeField(blank=True, null=True)),
                ('voided_by', models.IntegerField(blank=True, null=True)),
                ('administrator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_engagements', to=settings.AUTH_USER_MODEL)),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approver_engagements', to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.client')),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engagement_create_by', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewer_engagements', to=settings.AUTH_USER_MODEL)),
                ('update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='engagement_update_by', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='engagement_category', to='taskcontrol.engagementcategory')),
            ],
            options={
                'db_table': 'engagement',
            },
        ),
        migrations.CreateModel(
            name='EngagementType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_th', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.engagementcategory')),
            ],
            options={
                'db_table': 'engagement_type',
            },
        ),
        migrations.CreateModel(
            name='EngagementDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('notification', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('review_by', models.BooleanField(default=False)),
                ('approved_by', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('voided_at', models.DateTimeField(blank=True, null=True)),
                ('voided_by', models.IntegerField(blank=True, null=True)),
                ('engagement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.engagement')),
                ('engagement_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='engagement_detail_category', to='taskcontrol.engagementcategory')),
                ('engagement_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='engagement_detail_type', to='taskcontrol.engagementtype')),
            ],
            options={
                'db_table': 'engagement_detail',
            },
        ),
        migrations.AddField(
            model_name='engagement',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='engagement_type', to='taskcontrol.engagementtype'),
        ),
        migrations.CreateModel(
            name='FileManage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_client', models.FileField(blank=True, max_length=255, null=True, upload_to='files/client/')),
                ('image_client', models.ImageField(blank=True, null=True, upload_to='images/client/')),
                ('file_engagement', models.FileField(blank=True, max_length=255, null=True, upload_to='files/engagement/')),
                ('image_engagement', models.ImageField(blank=True, null=True, upload_to='images/engagement/')),
                ('file_task', models.FileField(blank=True, max_length=255, null=True, upload_to='files/task/')),
                ('image_task', models.ImageField(blank=True, null=True, upload_to='images/task/')),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('voided_at', models.DateTimeField(blank=True, null=True)),
                ('voided_by', models.IntegerField(blank=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.client')),
                ('engagement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.engagement')),
            ],
            options={
                'db_table': 'file_manage',
            },
        ),
        migrations.AddField(
            model_name='engagement',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='engagement_file', to='taskcontrol.filemanage'),
        ),
        migrations.AddField(
            model_name='client',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_file', to='taskcontrol.filemanage'),
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_th', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provinces', to='taskcontrol.country')),
                ('geography', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provinces', to='taskcontrol.geography')),
            ],
            options={
                'db_table': 'province',
            },
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='taskcontrol.province'),
        ),
        migrations.AddField(
            model_name='addressbase',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.province'),
        ),
        migrations.AddField(
            model_name='client',
            name='register_tax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_register_tax', to='taskcontrol.registertax'),
        ),
        migrations.CreateModel(
            name='ClientPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('password', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.client')),
                ('type_password', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.registertype')),
            ],
            options={
                'db_table': 'client_password',
            },
        ),
        migrations.CreateModel(
            name='Subdistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_th', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('zipcode', models.PositiveIntegerField()),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.district')),
            ],
            options={
                'db_table': 'subdistrict',
            },
        ),
        migrations.AddField(
            model_name='addressbase',
            name='subdistrict',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.subdistrict'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('OPEN JOB', 'Open Job'), ('IN PROGRESS', 'In Progress'), ('REVIEW', 'Review'), ('PENDING CLIENT', 'Pending Client'), ('DONE', 'Done')], default='OPEN JOB', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('voided_at', models.DateTimeField(blank=True, null=True)),
                ('voided_by', models.IntegerField(blank=True, null=True)),
                ('engagement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.engagement')),
            ],
            options={
                'db_table': 'task',
            },
        ),
        migrations.AddField(
            model_name='filemanage',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskcontrol.task'),
        ),
    ]
