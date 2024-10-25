from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


PRESSURE_RANGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(300)]


class PressureNotesManager(models.Manager):
    def select_related_user(self):
        return (
            self.get_queryset()
            .order_by(PressureNote.created_at.field.name)
            .select_related(PressureNote.person.field.name)
        )

    def last_note(self, user_id):
        return self.select_related_user().filter(person__id=user_id).last()

    def between_dates(self, start_date, finish_date, user_id):
        return (
            self.select_related_user()
            .filter(person__id=user_id)
            .filter(
                created_at__range=[start_date, finish_date],
            )
            .reverse()
        )


class PressureNote(models.Model):
    objects = PressureNotesManager()

    person = models.ForeignKey(
        User, on_delete=models.CASCADE,
    )
    systolic_pressure = models.IntegerField(
        help_text="верхнее давление",
        validators=PRESSURE_RANGE_VALIDATOR,
    )
    diastolic_pressure = models.IntegerField(
        help_text="нижнее давление",
        validators=PRESSURE_RANGE_VALIDATOR,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "запись давления"
        verbose_name_plural = "записи давления"

    def __str__(self):
        return f"Note #{self.id}"
