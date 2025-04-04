from statuspage.forms import StatusPageModelBulkEditForm
from utilities.forms import StaticSelect, StaticSelectMultiple, add_blank_choice, BulkEditNullBooleanSelect
from .. import choices
from ..models import Incident, IncidentUpdate, IncidentTemplate
from django import forms
from components.models import Component

__all__ = (
    'IncidentBulkEditForm',
    'IncidentUpdateBulkEditForm',
    'IncidentTemplateBulkEditForm',
)


class IncidentBulkEditForm(StatusPageModelBulkEditForm):
    status = forms.ChoiceField(
        choices=add_blank_choice(choices.IncidentStatusChoices),
        required=False,
        widget=StaticSelect(),
    )
    impact = forms.ChoiceField(
        choices=add_blank_choice(choices.IncidentImpactChoices),
        required=False,
        widget=StaticSelect(),
    )
    visibility = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect,
        label='Visible',
    )
    components = forms.ModelMultipleChoiceField(
        queryset=Component.objects.all(),
        required=False,
        widget=StaticSelectMultiple(),
    )

    model = Incident
    fieldsets = (
        ('Incident', ('status', 'impact', 'visibility', 'components')),
    )
    nullable_fields = ('components',)


class IncidentUpdateBulkEditForm(StatusPageModelBulkEditForm):
    new_status = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect,
        label='New Status',
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(choices.IncidentStatusChoices),
        required=False,
        widget=StaticSelect(),
    )

    model = IncidentUpdate
    fieldsets = (
        ('Incident Update', ('new_status', 'status',)),
    )


class IncidentTemplateBulkEditForm(StatusPageModelBulkEditForm):
    status = forms.ChoiceField(
        choices=add_blank_choice(choices.IncidentStatusChoices),
        required=False,
        widget=StaticSelect(),
    )
    impact = forms.ChoiceField(
        choices=add_blank_choice(choices.IncidentImpactChoices),
        required=False,
        widget=StaticSelect(),
    )
    visibility = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect,
        label='Visible',
    )
    components = forms.ModelMultipleChoiceField(
        queryset=Component.objects.all(),
        required=False,
        widget=StaticSelectMultiple(),
    )
    update_component_status = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect,
        label='Update Component Status',
    )

    model = IncidentTemplate
    fieldsets = (
        ('Incident Template', ('status', 'impact', 'visibility', 'components', 'update_component_status')),
    )
    nullable_fields = ('components',)
