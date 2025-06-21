from django.contrib import admin
from .models import Student, Course, AMISStudent, LossReport


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'mobile', 'year_of_study', 'course', 'is_verified', 'payment_status')
    search_fields = ('student_id', 'name', 'course')
    list_filter = ('course', 'is_verified', 'id_lost', 'payment_status')


@admin.register(AMISStudent)
class AMISStudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'course', 'year_of_study', 'mobile')


@admin.register(LossReport)
class LossReportAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'report_file', 'reported_at')


admin.site.register(Student)
admin.site.register(Course)
