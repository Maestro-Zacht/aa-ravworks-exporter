from django import forms

from django.conf import settings


class ExportForm(forms.Form):
    config = forms.FileField(required=True, label='Config file')
    skills = forms.ChoiceField(required=True, label='Skills', choices=[
        (None, 'Do not export'),
    ])
    character = forms.ChoiceField(required=True, label='Character')
    structures = forms.BooleanField(initial=True, required=False, label='Structures')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'structures' not in settings.INSTALLED_APPS:
            self.fields['structures'].disabled = True
            self.fields['structures'].initial = False
            self.fields['structures'].label = 'Structures (not available)'

        if 'memberaudit' in settings.INSTALLED_APPS and user.has_perm('memberaudit.basic_access'):
            self.fields['skills'].choices = [*self.fields['skills'].choices, ('memberaudit', 'MemberAudit')]

        if 'corptools' in settings.INSTALLED_APPS:
            self.fields['skills'].choices = [*self.fields['skills'].choices, ('corptools', 'CorpTools')]

        self.fields['skills'].initial = self.fields['skills'].choices[-1][0]

        self.fields['character'].choices = [
            (ownership.character.character_id, ownership.character.character_name)
            for ownership in user.character_ownerships.select_related('character').all()
        ]
