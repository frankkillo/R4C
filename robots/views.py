from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import RobotSerializer
from .robotstoxlsx import robots_to_xlsx, get_robots_last_week


@api_view(['POST'])
def create_robot(request):
    serializer = RobotSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def read_robots_xlsx(request):
    robots = get_robots_last_week()
    if robots:
        content = robots_to_xlsx(robots)
        response = HttpResponse(content=content, content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="robots_last_week.xlsx"'
        return response
    else:
        Response(status=status.HTTP_418_IM_A_TEAPOT, data={"detail": "No robots produced in the last week"})