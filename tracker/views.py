from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView

from tracker.models import PressureNote


class NotesList(ListView):
    model = PressureNote
    template_name = "mainpage.html"
    context_object_name = "notes"

    def get_queryset(self):
        start_date = self.request.GET.get("start", None)
        end_date = self.request.GET.get("end", None)
        if start_date and end_date:
            queryset = self.model.objects.between_dates(
                start_date, end_date, self.request.user.id,
            )
        else:
            queryset = self.model.objects.last_note(self.request.user.id)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Поскольку вывод всех записей происходит на главной
        странице нужно как-то подружить получение последней записи
        с получением всех (в одном случае сразу получается список, а в другом
        - один объект)
        """
        context = super().get_context_data(**kwargs)

        context["s_avg"] = -1
        context["d_avg"] = -1

        if type(context["notes"]) is PressureNote:
            last_node = context["notes"]
            context["notes"] = [last_node]
        elif context["notes"] is None:
            context["notes"] = []
        elif len(context["notes"]) >= 1:
            queryset = context["notes"]
            context["s_avg"] = queryset.aggregate(
                Avg("systolic_pressure"))["systolic_pressure__avg"]
            context["d_avg"] = queryset.aggregate(
                Avg("diastolic_pressure"))["diastolic_pressure__avg"]
        return context


class NewNote(View):
    model = PressureNote

    def post(self, request, *args, **kwargs):
        systolic_pressure = request.POST.get("systolic_pressure", None)
        diastolic_pressure = request.POST.get("diastolic_pressure", None)
        if request.user.is_authenticated:
            if systolic_pressure and diastolic_pressure:
                new_note = PressureNote(
                    person=request.user,
                    systolic_pressure=systolic_pressure,
                    diastolic_pressure=diastolic_pressure,
                )
                try:
                    new_note.full_clean()
                except ValidationError:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "Введено невозможное значение",
                    )
                else:
                    messages.add_message(
                        request, messages.SUCCESS, "Запись добавлена успешно",
                    )
                    new_note.save()
                    return redirect(reverse_lazy("tracker:list"))

        messages.add_message(
            request, messages.ERROR,
            (
                "Некорректно заполнена форма: пропущено поле, "
                "либо введено некорректное значение"
            ),
        )
        return redirect(reverse_lazy("tracker:list"))
