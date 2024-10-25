from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse_lazy

from tracker.models import PressureNote


class StaticURLTest(TestCase):
    def test_list_page_without_params(self):
        response = self.client.get(reverse_lazy("tracker:list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ContextTest(TestCase):
    def setUp(self):
        self.new_user = User.objects.create(
            username="test", email="1@y.ru", password="123",
        )
        self.new_user.save()
        new_note = PressureNote.objects.create(
            person=self.new_user,
            systolic_pressure=100,
            diastolic_pressure=100,
        )
        new_note.save()
        self.loginned_client = Client()
        self.loginned_client.force_login(self.new_user)

    def test_list_page_without_params_ul(self):
        response = self.client.get(reverse_lazy("tracker:list"))
        self.assertEqual(
            len(response.context["notes"]),
            0,
            "Незалогиненный пользователь получил другой контекст",
        )

    def test_list_page_without_params_l(self):
        response = self.loginned_client.get(reverse_lazy("tracker:list"))
        self.assertEqual(
            len(response.context["notes"]),
            1,
            "Залогиненный пользователь получил другой контекст",
        )

    def test_list_page_without_params_only_last(self):
        new_note = PressureNote.objects.create(
            person=self.new_user,
            systolic_pressure=102,
            diastolic_pressure=102,
        )
        new_note.save()

        response = self.loginned_client.get(reverse_lazy("tracker:list"))
        self.assertEqual(
            len(response.context["notes"]),
            1,
            "Залогиненный пользователь получил больше записей",
        )
        last_note = response.context["notes"][0]
        # запись созданная последней
        self.assertEqual(last_note.systolic_pressure, 102)


class NoteCreationTest(TestCase):
    def setUp(self):
        self.new_user = User.objects.create(
            username="test", email="1@y.ru", password="123",
        )
        self.new_user.save()
        self.loginned_client = Client()
        self.loginned_client.force_login(self.new_user)

    def test_validator_uncorrect(self):
        cases = [
            (-100, 100), (-100, 100),
            (-100, -100), (1000, 100),
            (100, 1000), (1000, 1000),
        ]
        notes_cnt = PressureNote.objects.count()
        for case in cases:
            with self.assertRaises(ValidationError):
                new_note = PressureNote(
                    person=self.new_user,
                    systolic_pressure=case[0],
                    diastolic_pressure=case[1],
                )
                new_note.full_clean()
                new_note.save()
        self.assertEqual(
            PressureNote.objects.count(),
            notes_cnt,
        )

    def test_validator_correct(self):
        cases = [
            (100, 100), (200, 200),
            (0, 200), (200, 0),
        ]
        notes_cnt = PressureNote.objects.count()
        for i, case in enumerate(cases):
            new_note = PressureNote(
                person=self.new_user,
                systolic_pressure=case[0],
                diastolic_pressure=case[1],
            )
            new_note.full_clean()
            new_note.save()
            self.assertEqual(
                PressureNote.objects.count(),
                notes_cnt + i + 1,
            )

    def test_correct_note_create_l(self):
        notes_cnt = PressureNote.objects.count()
        response = self.loginned_client.post(
            reverse_lazy("tracker:create_note"),
            {
                "systolic_pressure": 100,
                "diastolic_pressure": 100,
            },
        )
        self.assertEqual(PressureNote.objects.count(), notes_cnt + 1)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_uncorrect_note_create_l(self):
        cases = [
            (-100, 100), (-100, 100),
            (-100, -100), (1000, 100),
            (100, 1000), (1000, 1000),
        ]
        notes_cnt = PressureNote.objects.count()
        for case in cases:
            self.loginned_client.post(
                reverse_lazy("tracker:create_note"),
                {
                    "systolic_pressure": case[0],
                    "diastolic_pressure": case[1],
                },
            )
        self.assertEqual(PressureNote.objects.count(), notes_cnt)

    def test_correct_note_create_ul(self):
        notes_cnt = PressureNote.objects.count()
        self.client.post(
            reverse_lazy("tracker:create_note"),
            {
                "systolic_pressure": 100,
                "diastolic_pressure": 100,
            },
        )
        self.assertEqual(PressureNote.objects.count(), notes_cnt)
