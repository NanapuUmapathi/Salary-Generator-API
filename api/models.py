from django.db import models
import uuid

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    present_wage = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    half_day_wage = models.DecimalField(max_digits=10, decimal_places=2, default=500)

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('HALF_DAY', 'Half Day'),
        ('ABSENT', 'Absent')
    ]
    
    attendance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('user', 'date')
