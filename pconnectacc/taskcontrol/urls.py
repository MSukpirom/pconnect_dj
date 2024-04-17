from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = "taskcontrol"

urlpatterns = [

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # path('test/', testpage, name='testpage'),

    path('get_districts/', get_districts, name='GetDistrict'),
    path('get_subdistricts/', get_subdistricts, name='GetSubdistrict'),
    path('get_latest_job_code/', get_latest_job_code, name='get_latest_job_code'),

    path('get_engagement_type/', get_engagement_type, name='GetEngagementType'),

    path('dashboard/', dashboard, name='dashboard'),
    path('get_engagement_data/', get_engagement_data, name='get_engagement_data'),
    # path('search_datatable/', search_datatable, name='search_datatable'),
    path('get_engagement_summary/', get_engagement_summary, name='get_engagement_summary'),
    path('get_engagement_accounting/', get_engagement_accounting, name='get_engagement_accounting'),
    path('get_filter_dashboard/', get_filter_dashboard, name='get_filter_dashboard'),

    path('client/list/', client_list, name='client_list'),
    path('client/create/', client_create, name='client_create'),
    path('client/detail/<int:client_id>/', client_detail, name='client_detail'),
    path('client/update/<int:client_id>/', client_update, name='client_update'),
    path('client/delete/<int:client_id>/', delete_client, name='delete_client'),

    path('file_client/list/<int:client_id>/', file_client_list, name='file_client_list'),
    path('file_client/create/<int:client_id>/', file_client_create, name='file_client_create'),
    path('file_client/delete/<int:file_id>/', file_client_delete, name='file_client_delete'),
    path('file_client/file_client_download_file/<int:file_id>/', file_client_download_file, name='file_client_download_file'),
    path('file_client/file_client_download_image/<int:image_id>/', file_client_download_image, name='file_client_download_image'),

    path('client_contact/create/<int:client_id>/', create_contact, name='create_contact'),
    path('client_contact/delete/<int:contact_id>/', delete_contact, name='delete_contact'),

    path('password/<int:client_id>/', password_list, name='password_list'),
    path('password/create/<int:client_id>/', create_password, name='create_password'),
    path('password/update/<int:password_id>/', update_password, name='update_password'),
    path('password/delete/<int:password_id>/', delete_password, name='delete_password'),

    path('engagement/list/', engagement_list, name='engagement_list'),
    path('engagements/create/', engagement_create, name='engagement_create'),
    path('engagements/update/<int:engagement_id>/', engagement_update, name='engagement_update'),
    path('engagements/delete/<int:engagement_id>/', engagement_delete, name='engagement_delete'),

    path('engagements_detail/<int:engagement_id>/', engagement_detail, name='engagement_detail'),
    path('engagement_detail/create/<int:engagement_id>/', engagement_detail_create, name='engagement_detail_create'),
    path('engagement_detail/delete/<int:engagement_detail_id>/', engagement_detail_delete, name='engagement_detail_delete'),

    path('file_engagement/list/<int:engagement_id>/', file_engagement_list, name='file_engagement_list'),
    path('file_engagement/create/<int:engagement_id>/', file_engagement_create, name='file_engagement_create'),
    path('file_engagement/delete/<int:file_id>/', file_engagement_delete, name='file_engagement_delete'),
    path('file_engagement/file_client_download_file/<int:file_id>/', file_engagement_file_client_download_file, name='file_engagement_file_client_download_file'),
    path('file_engagement/file_client_download_image/<int:image_id>/', file_engagement_file_client_download_image, name='file_engagement_file_client_download_image'),

    # path('user_management/', user_management, name='user_management'),

    path('category/', category, name='category'),
    path('category/create/', create_category, name='create_category'),
    path('category/delete/<int:category_id>/', delete_category, name='delete_category'),
    path('category/type/create', create_type, name='create_type'),

    path('kanban_board/', kanban_board, name='kanban_board'),
    path('update_engagement_status/', update_engagement_status, name='update_engagement_status'),
    path('update_notes/', update_engagement_notes, name='update_engagement_notes'),
    path('get_engagement_details/', get_engagement_details, name='get_engagement_details'),
    path('search_filter_engagement_details/', search_filter_engagement_details, name='search_filter_engagement_details'),
    path('get_filter_engagement_details/', get_filter_engagement_details, name='get_filter_engagement_details'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
