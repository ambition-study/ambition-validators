from django.db import models
from django.db.models import options
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import ListModelMixin, BaseUuidModel
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


options.DEFAULT_NAMES = (options.DEFAULT_NAMES + ('consent_model',))


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class Appointment(BaseUuidModel):

    visit_code_sequence = models.IntegerField(
        verbose_name=('Sequence'),
        default=0,
        null=True,
        blank=True)


class RequiresConsentMixin(models.Model):

    class Meta:
        abstract = True
        consent_model = None


class SubjectConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    gender = models.CharField(max_length=25)


class SubjectVisit(RequiresConsentMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    class Meta(RequiresConsentMixin.Meta):
        consent_model = 'ambition_validator.subjectconsent'


class SubjectScreening(BaseUuidModel):

    screening_identifier = models.CharField(max_length=25, unique=True)

    report_datetime = models.DateTimeField(
        default=get_utcnow)

    mental_status = models.CharField(
        max_length=10)

    age_in_years = models.IntegerField()


class PatientHistory(BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)

    previous_oi = models.CharField(
        verbose_name='Previous opportunistic infection other than TB?',
        max_length=5,
        choices=YES_NO)

    first_arv_regimen = models.CharField(
        verbose_name='Drug used in first line arv regimen',
        max_length=50)
