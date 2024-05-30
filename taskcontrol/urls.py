from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = "taskcontrol"

handler404 = 'taskcontrol.views.error_404_view'

urlpatterns = [
    path('coding/', building_code, name='building_code'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('test/', testpage, name='testpage'),
    path('get_districts/', get_districts, name='GetDistrict'),
    path('get_subdistricts/', get_subdistricts, name='GetSubdistrict'),
    path('get_latest_job_code/', get_latest_job_code, name='get_latest_job_code'),
    path('get_channel/', get_channel, name='get_channel'),

    path('get_engagement_type/', get_engagement_type, name='get_engagement_type'),

    path('dashboard/', dashboard, name='dashboard'),
    path('get_filter_dashboard/', get_filter_dashboard, name='get_filter_dashboard'),
    # path('search_datatable/', search_datatable, name='search_datatable'),
    path('get_engagement_data/', get_engagement_data, name='get_engagement_data'),
    path('get_engagement_accounting/', get_engagement_accounting, name='get_engagement_accounting'),
    path('get_engagement_tax/', get_engagement_tax, name='get_engagement_tax'),
    path('get_engagement_payroll/', get_engagement_payroll, name='get_engagement_payroll'),
    path('get_engagement_report/', get_engagement_report, name='get_engagement_report'),

    path('client/list/', client_list, name='client_list'),
    path('client/<int:client_id>/', record_client, name='record_client'),

    path('client/create/', client_create, name='client_create'),
    path('client/detail/<int:client_id>/', client_detail, name='client_detail'),
    path('client/update/<int:client_id>/', client_update, name='client_update'),
    path('client/delete/<int:client_id>/', client_delete, name='client_delete'),

    path('client/contact_create/<int:client_id>/', create_contact, name='create_contact'),
    path('client/contact_delete/<int:contact_id>/', delete_contact, name='delete_contact'),

    path('client/password/<int:client_id>/', password_list, name='password_list'),
    path('client/password_create/<int:client_id>/', create_password, name='create_password'),
    path('client/password_update/<int:password_id>/', update_password, name='update_password'),
    path('client/password_delete/<int:password_id>/', delete_password, name='delete_password'),

    path('client/file_list/<int:client_id>/', file_client_list, name='file_client_list'),
    path('client/file_create/<int:client_id>/', file_client_create, name='file_client_create'),
    path('client/file_delete/<int:file_id>/', file_client_delete, name='file_client_delete'),
    path('client/file_client_download_file/<int:file_id>/', file_client_download_file, name='file_client_download_file'),
    path('client/file_client_download_image/<int:image_id>/', file_client_download_image, name='file_client_download_image'),

    path('engagement/list/', engagement_list, name='engagement_list'),
    path('engagement/create/', engagement_create, name='engagement_create'),
    path('engagement/<int:engagement_id>/', record_engagement, name='record_engagement'),
    path('engagement/detail/<int:engagement_id>', engagement_detail, name='engagement_detail'),
    path('engagement/update/<int:engagement_id>/', engagement_update, name='engagement_update'),
    path('engagement/delete/<int:engagement_id>/', engagement_delete, name='engagement_delete'),

    path('engagement/detail_job/<int:engagement_id>/', engagement_job, name='engagement_job'),
    path('engagement/detail_job/create/<int:engagement_id>/', engagement_job_create, name='engagement_job_create'),
    path('engagement/detail_job/delete/<int:engagement_job_id>/', engagement_job_delete, name='engagement_job_delete'),

    path('file_engagement/list/<int:engagement_id>/', file_engagement_list, name='file_engagement_list'),
    path('file_engagement/create/<int:engagement_id>/', file_engagement_create, name='file_engagement_create'),
    path('file_engagement/delete/<int:file_id>/', file_engagement_delete, name='file_engagement_delete'),
    path('file_engagement/file_client_download_file/<int:file_id>/', file_engagement_file_client_download_file, name='file_engagement_file_client_download_file'),
    path('file_engagement/file_client_download_image/<int:image_id>/', file_engagement_file_client_download_image, name='file_engagement_file_client_download_image'),

    path('manage_category/', manage_category, name='manage_category'),
    path('manage_category/update/<int:category_id>/', update_category, name='update_category'),
    path('manage_category/delete/<int:category_id>/', delete_category, name='delete_category'),

    path('manage_type/', manage_type, name='manage_type'),
    path('manage_type/update/<int:type_id>/', update_type, name='update_type'),
    path('manage_type/delete/<int:type_id>/', delete_type, name='delete_type'),

    path('manage_channel/', manage_channel, name='manage_channel'),
    path('manage_channel/update/<int:channel_id>/', update_channel, name='update_channel'),
    path('manage_channel/delete/<int:channel_id>/', delete_channel, name='delete_channel'),

    path('manage_register_type/', manage_register_type, name='manage_register_type'),
    path('manage_register_type/update/<int:register_type_id>/', update_register_type, name='update_register_type'),
    path('manage_register_type/delete/<int:register_type_id>/', delete_register_type, name='delete_register_type'),

    path('kanban_board/', kanban_board, name='kanban_board'),
    path('update_engagement_status/', update_engagement_status, name='update_engagement_status'),
    path('update_notes/', update_engagement_notes, name='update_engagement_notes'),
    path('get_engagement_details/', get_engagement_details, name='get_engagement_details'),
    path('search_filter_engagement_details/', search_filter_engagement_details, name='search_filter_engagement_details'),
    path('get_filter_engagement_details/', get_filter_engagement_details, name='get_filter_engagement_details'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
