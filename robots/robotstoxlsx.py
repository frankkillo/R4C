import xlsxwriter
from io import BytesIO
from datetime import timedelta

from django.utils import timezone
from django.db.models import Count

from .models import Robot


def get_robots_last_week():
    queryset = Robot.objects.filter(created__gte=timezone.now()-timedelta(days=7)). \
        values('model','version','created__day').annotate(Count('created')). \
        values('model','version','created__count').order_by('model')
    robots = list(queryset)

    return robots


def robots_to_xlsx(robots):
    current_model = robots[0]['model']
    current_row = 1
    columns = ["Модель", "Версия", "Количество за день"]

    output = BytesIO()
    with xlsxwriter.Workbook(output) as workbook:
        worksheet = workbook.add_worksheet(f'Model={current_model}')
        worksheet.write_row(0, 0, columns)

        for  robot in robots:
            if robot['model'] != current_model:
                current_model = robot['model']
                current_row = 1
                worksheet = workbook.add_worksheet(f"Model={current_model}")
                worksheet.write_row(0, 0, columns)

            worksheet.write_row(current_row, 0, robot.values())
            current_row += 1
    xlsx_data = output.getvalue()
    return xlsx_data
                