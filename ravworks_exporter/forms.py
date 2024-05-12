from django import forms
from django.conf import settings
from django.db.models import Exists, OuterRef


class ExportForm(forms.Form):
    config = forms.FileField(required=True, label='Config file')
    skills = forms.ChoiceField(required=False, label='Skills', choices=[
        (None, 'Do not export'),
    ])
    structures = forms.BooleanField(initial=True, required=False, label='Structures')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'structures' not in settings.INSTALLED_APPS:
            self.fields['structures'].disabled = True
            self.fields['structures'].initial = False
            self.fields['structures'].label = 'Structures (not available)'

        if 'memberaudit' in settings.INSTALLED_APPS and user.has_perm('memberaudit.basic_access'):
            from memberaudit.models import Character

            ownerships = (
                user.character_ownerships
                .filter(
                    Exists(
                        Character.objects.filter(
                            eve_character=OuterRef('character')
                        )
                    )
                )
                .select_related('character')
            )

            choices = [
                (f"memberaudit-{ownership.character.character_id}", f"MemberAudit - {ownership.character.character_name}")
                for ownership in ownerships
            ]

            self.fields['skills'].choices = [*self.fields['skills'].choices, *choices]

        if 'corptools' in settings.INSTALLED_APPS:
            from corptools.models import CharacterAudit

            ownerships = (
                user.character_ownerships
                .filter(
                    Exists(
                        CharacterAudit.objects.filter(
                            character=OuterRef('character')
                        )
                    )
                )
                .select_related('character')
            )

            choices = [
                (f"corptools-{ownership.character.character_id}", f"CorpTools - {ownership.character.character_name}")
                for ownership in ownerships
            ]

            self.fields['skills'].choices = [*self.fields['skills'].choices, *choices]

        self.fields['skills'].initial = self.fields['skills'].choices[-1][0]
