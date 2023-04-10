import django.forms

import teams.models


class EditTeamForm(django.forms.ModelForm):
    class Meta:
        model = teams.models.Team
        fields = (
            teams.models.Team.image.field.name,
            teams.models.Team.title.field.name,
            teams.models.Team.description.field.name,
            teams.models.Team.presentation.field.name,
            teams.models.Team.is_published.field.name,
            teams.models.Team.languages.field.name,
            teams.models.Team.technologies.field.name,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.widget_type == 'checkbox':
                field.field.widget.attrs['class'] = 'form-check-input'
                field.label_classes = ('form-check-label',)
            elif field.widget_type == 'selectmultiple':
                field.field.widget.attrs['class'] = 'form-select'
            else:
                field.field.widget.attrs['class'] = 'form-control'
