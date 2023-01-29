from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail

from robots.models import Robot
from orders.models import Order


@receiver(pre_save, sender=Robot, dispatch_uid="check_orders")
def check_orders(sender, instance, **kwargs):
    serial = instance.serial

    if not Robot.objects.filter(serial=serial):
        queryset = Order.objects.filter(robot_serial=serial).values_list('customer__email')
        if queryset:
            data = []
            admin_email = 'admin@exaple.com'
            subject = 'Робот в наличии!'
            message = f'Добрый день!\n \
                    Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\n \
                    Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'
            for email in queryset:
                mail = (subject, message, admin_email, email)
                data.append(mail)
        
            send_mass_mail(tuple(data))

