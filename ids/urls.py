from django.urls import path
from .views import index, login_view, logout_view, dup_dashboard, pc_officer_dashboard, management_dashboard, verify_students, upload_students, view_report, print_ids, students_by_course, view_verified_students, view_printed_ids, fetch_student_from_amis, fetch_all_students_from_amis, print_id, report_lost_id, handle_lost_id, view_verified_lost_ids, lost_id_report, lost_id_verification

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dup-dashboard/', dup_dashboard, name='dup_dashboard'),
    path('pc-officer-dashboard/', pc_officer_dashboard, name='pc_officer_dashboard'),
    path('management-dashboard/', management_dashboard, name='management_dashboard'),
    path('verify_students/', verify_students, name='verify_students'),
    path('upload_students/', upload_students, name='upload_students'),
    path('view_report/', view_report, name='view_report'),
    path('print_ids/', print_ids, name='print_ids'),
    path('students_by_course/', students_by_course, name='students_by_course'),
    path('view_verified_students/', view_verified_students, name='view_verified_students'),
    path('view_printed_ids/', view_printed_ids, name='view_printed_ids'),
    path('fetch_student/', fetch_student_from_amis, name='fetch_student'),
    path('fetch_all_students/', fetch_all_students_from_amis, name='fetch_all_students'),
    path('print_id/<str:student_id>/', print_id, name='print_id'),
    path('report_lost_id/', report_lost_id, name='report_lost_id'),
    path('handle_lost_id/', handle_lost_id, name='handle_lost_id'),
    path('verified_lost_ids/', view_verified_lost_ids, name='view_verified_lost_ids'),
    path('lost_id_report/', lost_id_report, name='lost_id_report'),
    path('lost_id_verification/', lost_id_verification, name='lost_id_verification'),
]
