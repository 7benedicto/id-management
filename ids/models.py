from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),

    ]
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year_of_study = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    id_printed = models.BooleanField(default=False)
    payment_status = models.CharField(
        max_length=7,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    id_lost = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class AMISStudent(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    id_printed = models.BooleanField(default=False)
    id_lost = models.BooleanField(default=False)
    id_replacement_requested = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class LossReport(models.Model):
    student_id = models.CharField(max_length=100)
    report_file = models.FileField(upload_to='loss_reports/')
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loss Report for {self.student_id} on {self.reported_at}"
