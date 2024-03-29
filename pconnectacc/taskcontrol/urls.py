from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "taskcontrol"

urlpatterns = [
    path('', home),

    # path('error404/', error_page404, name="error_page404"),
    # path('login/', login_view, name="login"),
    # path('logout/', logout_view, name="logout"),
    # path('user_view/', user_view, name="user_view"),
    # path('sign_up/', sign_up, name="sign_up"),
    # path('error404/', error_page, name="error_page"),

    # path('testpage/', testpage, name='testpage'),
    # path('test2/', test, name='test'),

    # path('get_districts/', get_districts, name='GetDistrict'),
    # path('get_subdistricts/', get_subdistricts, name='GetSubdistrict'),
    # path('get_latest_job_code/', get_latest_job_code, name='get_latest_job_code'),

    # path('get_engagement_type/', get_engagement_type, name='GetEngagementType'),

    # path('dashboard/', dashboard, name='dashboard'),
    # path('get_engagement_data/', get_engagement_data, name='get_engagement_data'),
    # path('search_datatable/', search_datatable, name='search_datatable'),
    # path('get_engagement_summary/', get_engagement_summary, name='get_engagement_summary'),
    # path('get_engagement_accounting/', get_engagement_accounting, name='get_engagement_accounting'),

    # path('client/list/', client_list, name='client_list'),
    # path('client/create/', client_create, name='client_create'),
    # path('client/detail/<int:client_id>/', client_detail, name='client_detail'),
    # path('client/update/<int:client_id>/', client_update, name='client_update'),
    # path('delete/client/<int:client_id>/', delete_client, name='delete_client'),

    # path('file/list/<int:client_id>/', file_list, name='file_list'),
    # path('create/file/<int:client_id>', create_file, name='create_file'),
    # path('delete/file/<int:file_id>/', delete_file, name='delete_file'),
    # path('download_file/<int:file_id>/', download_file, name='download_file'),
    # path('download_image/<int:image_id>/', download_image, name='download_image'),

    # path('client/contact/create/<int:client_id>/', create_contact, name='create_contact'),
    # path('client/contact/delete/<int:contact_id>/', delete_contact, name='delete_contact'),

    # path('passwords/<int:client_id>/', password_list, name='password_list'),
    # path('password/create/<int:client_id>/', create_password, name='create_password'),
    # path('password/update/<int:password_id>/', update_password, name='update_password'),
    # path('password/delete/<int:password_id>/', delete_password, name='delete_password'),

    # path('engagement-list/', engagement_list, name='engagement_list'),
    # path('engagements/create/', engagement_create, name='engagement_create'),
    # path('engagements/<int:engagement_id>/', engagements, name='engagements'),
    # path('engagements/update/<int:engagement_id>/', engagement_update, name='engagement_update'),
    # path('engagements/delete/<int:engagement_id>/', engagement_delete, name='engagement_delete'),

    # path('engagement/detail/create/<int:engagement_id>/', engagement_detail_create, name='engagement_detail_create'),
    # path('engagement/detail/delete/<int:engagement_detail_id>/', engagement_detail_delete, name='engagement_detail_delete'),

    # path('setting/', setting, name='setting'),
    # path('user_management/', user_management, name='user_management'),
    # path('setting/category/', category, name='category'),
    # path('setting/category/create_category', create_category, name='create_category'),
    # path('setting/category/create_type', create_type, name='create_type'),

    # path('kanban_board/', kanban_board, name='kanban_board'),
    # path('update_engagement_status/', update_engagement_status, name='update_engagement_status'),
    # path('update_notes/', update_engagement_notes, name='update_engagement_notes'),
    # path('get_engagement_details/', get_engagement_details, name='get_engagement_details'),
    # path('filter_engagement_details/', filter_engagement_details, name='filter_engagement_details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
