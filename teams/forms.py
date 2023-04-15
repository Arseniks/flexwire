from django import forms

from teams import models


class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.widget_type == 'checkbox':
                field.field.widget.attrs['class'] = 'form-check-input'
                field.label_classes = ('form-check-label',)
            elif field.widget_type in ('select', 'selectmultiple'):
                continue
            else:
                field.field.widget.attrs['class'] = 'form-control'


class TeamForm(BootstrapForm):
    class Meta:
        model = models.Team
        fields = (
            models.Team.image.field.name,
            models.Team.title.field.name,
            models.Team.description.field.name,
            models.Team.presentation.field.name,
            models.Team.is_published.field.name,
            models.Team.technologies.field.name,
            models.Team.language.field.name,
        )
