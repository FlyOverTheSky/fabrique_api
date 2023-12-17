from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator


class Mailing(models.Model):
    start_date_time = models.DateTimeField(
        verbose_name='Время и дата начала рассылки',
    )
    end_date_time = models.DateTimeField(
        verbose_name='Время и дата окончания рассылки',
    )
    text = models.TextField(
        verbose_name='Текст рассылки',
    )
    client_mobile_operator_code = models.CharField(
        verbose_name='Код мобильного оператора для фильтрации',
        max_length=3,
        # validators=[MinLengthValidator(3)],
        null=True,
        blank=True,
    )
    client_tag = models.CharField(
        verbose_name='Метка клиентов для фильтрации',
        max_length=250,
        null=True,
        blank=True,
    )
    client_time_zone = models.CharField(
        verbose_name='Временной пояс для фильтрации',
        max_length=30,
        null=True,
        blank=True,
    )


class Client(models.Model):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{11,11}$',
        message="Телефон должен быть в формате: '7999999999'."
    )

    phone_number = models.CharField(
        max_length=11,
        verbose_name='Номер телефона',
        validators=[phone_validator],
        unique=True,
    )

    mobile_operator_code = models.CharField(
        verbose_name='Код мобильного оператора',
        max_length=3,
        validators=[MinLengthValidator(3)]
    )

    tag = models.CharField(
        verbose_name='Метка',
        max_length=250,
        null=True,
        blank=True
    )

    time_zone = models.CharField(
        verbose_name='Временной пояс',
        max_length=30,
    )


class Message(models.Model):
    def __str__(self):
        return self.mailing.text

    send_date = models.DateTimeField(
        verbose_name='Время отправки',
        null=True,
        blank=True
    )
    status = models.CharField(
        verbose_name='Статус отправки',
        max_length=15,
        default='NOT SEND'
    )
    mailing = models.ForeignKey(
        to=Mailing,
        on_delete=models.CASCADE,
        verbose_name='Посылка',
    )
    client = models.ForeignKey(
        to=Client,
        on_delete=models.DO_NOTHING,
        verbose_name='Получатель'
    )
