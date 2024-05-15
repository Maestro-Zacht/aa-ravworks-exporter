from django import forms
from django.conf import settings
from django.db.models import Exists, OuterRef


class ExportForm(forms.Form):
    config = forms.FileField(required=True, label='Config file')
    skills = forms.ChoiceField(required=False, label='Skills', choices=[
        (None, 'Do not export'),
    ])
    structures = forms.ChoiceField(required=False, label='Structures', choices=[
        (None, 'Do not export'),
    ])

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'structures' in settings.INSTALLED_APPS:
            self.fields['structures'].choices = [*self.fields['structures'].choices, ('structures', 'Structures')]

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

            self.fields['structures'].choices = [*self.fields['structures'].choices, ('corptools', 'CorpTools')]

        self.fields['skills'].initial = self.fields['skills'].choices[-1][0]
        self.fields['structures'].initial = self.fields['structures'].choices[-1][0]
