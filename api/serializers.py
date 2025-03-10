from rest_framework import serializers
from .models import User, Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
    
    def validate(self, data):
        if data['date'].weekday() >= 5:
            raise serializers.ValidationError("Cannot mark attendance on weekends.")

        if Attendance.objects.filter(user=data['user'], date=data['date']).exists():
            raise serializers.ValidationError("Attendance already recorded for this date.")

        return data
