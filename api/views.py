import datetime
import uuid
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Attendance, User
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        try:
            user_id = request.data.get("user_id")
            date_str = request.data.get("date")
            status_value = request.data.get("status")

           
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

           
            if date_obj.weekday() >= 5: 
                return Response({"error": "Cannot mark attendance on weekend."}, status=status.HTTP_400_BAD_REQUEST)

          
            if Attendance.objects.filter(user_id=user_id, date=date_obj).exists():
                return Response({"error": "Attendance for this date already exists."}, status=status.HTTP_400_BAD_REQUEST)

           
            attendance = Attendance(
                attendance_id=uuid.uuid4(),
                user_id=User.objects.get(user_id=user_id),
                date=date_obj,
                status=status_value
            )
            attendance.save()

            return Response({"message": "Attendance recorded."}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "Invalid user_id."}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def generate_salary(request, user_id, date):
    try:
        
        given_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        
        
        if not (1 <= given_date.day <= 5):
            return Response({"error": "Salary can only be generated between the 1st and 5th of the month."}, status=status.HTTP_400_BAD_REQUEST)

        
        first_day_of_current_month = given_date.replace(day=1)
        previous_month = first_day_of_current_month - datetime.timedelta(days=1)
        previous_month_start = previous_month.replace(day=1)
        previous_month_end = first_day_of_current_month - datetime.timedelta(days=1)

        
        user = User.objects.get(user_id=user_id)

        
        attendance_records = Attendance.objects.filter(user_id=user_id, date__range=[previous_month_start, previous_month_end])

        
        total_salary = 0
        for record in attendance_records:
            if record.status == "PRESENT":
                total_salary += user.present_wage
            elif record.status == "HALF_DAY":
                total_salary += user.half_day_wage
            

        return Response({
            "user_id": user_id,
            "total_salary": total_salary
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "Invalid user_id."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
