from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import OTHER, YES

from ..form_validators import RecurrenceSymptomFormValidator
from .models import ListModel


class TestRecurrenceSymptomFormValidator(TestCase):

    #     def test_meningitis_symptom_other_none(self):
    #         options = {
    #             'meningitis_symptom': OTHER,
    #             'meningitis_symptom_other': None}
    #         form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
    #         self.assertRaises(ValidationError, form_validator.validate)

    #     def test_meningitis_symptom_other_valid(self):
    #         options = {
    #             'meningitis_symptom': OTHER,
    #             'meningitis_symptom_other': 'blah'}
    #         form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
    #         try:
    #             form_validator.validate()
    #         except forms.ValidationError as e:
    #             self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_neurological_focal_neurologic_deficit_none(self):
        options = {
            'neurological': YES,
            'focal_neurologic_deficit': None}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('focal_neurologic_deficit', form_validator._errors)

    def test_amb_administered_no_duration_invalid(self):
        options = {
            'amb_administered': YES,
            'amb_duration': None}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_amb_administered_duration_valid(self):
        options = {
            'amb_administered': YES,
            'amb_duration': 5}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_steroids_administered_no_choices_invalid(self):
        options = {
            'steroids_administered': YES,
            'steroids_choices': None,
            'steroids_duration': 5}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_steroids_administered_choices_valid(self):
        options = {
            'steroids_administered': YES,
            'steroids_choices': 'oral_prednisolone',
            'steroids_duration': 5}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_steroids_administered_no_duration_invalid(self):
        options = {
            'steroids_administered': YES,
            'steroids_choices': 'oral_prednisolone',
            'steroids_duration': None}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_steroids_administered_duration_valid(self):
        options = {
            'steroids_administered': YES,
            'steroids_choices': 'oral_prednisolone',
            'steroids_duration': 5}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_steroids_administered_no_other_invalid(self):
        options = {
            'steroids_administered': YES,
            'steroids_duration': 5,
            'steroids_choices': OTHER,
            'steroids_choices_other': None}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_steroids_administered_other_valid(self):
        options = {
            'steroids_administered': YES,
            'steroids_duration': 5,
            'steroids_choices': OTHER,
            'steroids_choices_other': 'blah'}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_m2m_other(self):
        ListModel.objects.create(name='something', short_name='something')
        ListModel.objects.create(name=OTHER, short_name=OTHER)
        options = [
            ('meningitis_symptom', 'meningitis_symptom_other'),
            ('neurological', 'other_cn_palsy_chosen'),
            ('antibiotic_treatment', 'antibiotic_treatment_other')]
        for field, field_other in options:
            with self.subTest(field=field):
                cleaned_data = {
                    'meningitis_symptom': ListModel.objects.exclude(name=OTHER),
                    'neurological': ListModel.objects.exclude(name=OTHER),
                    'antibiotic_treatment': ListModel.objects.exclude(name=OTHER)}
                cleaned_data.update(
                    {field: ListModel.objects.filter(name=OTHER),
                     field_other: None})
                form_validator = RecurrenceSymptomFormValidator(
                    cleaned_data=cleaned_data)
                self.assertRaises(ValidationError, form_validator.validate)
                self.assertIn(field_other, form_validator._errors)

    def test_on_arvs_no_date_invalid(self):
        options = {
            'on_arvs': YES,
            'arv_date': None}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_on_arvs_with_date_valid(self):
        options = {
            'on_arvs': YES,
            'arv_date': get_utcnow()}
        form_validator = RecurrenceSymptomFormValidator(cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')