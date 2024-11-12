from django import forms
from django.conf import settings
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models import Exists, OuterRef


class ExportForm(forms.Form):
    config = forms.FileField(required=True, label=_('Config file'))
    skills = forms.ChoiceField(required=False, label=_('Skills'), choices=[
        (None, _('Do not export')),
    ])
    structures = forms.ChoiceField(required=False, label=_('Structures'), choices=[
        (None, _('Do not export')),
    ])

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'structures' in settings.INSTALLED_APPS:
            from structures import __title__ as structures_title
            self.fields['structures'].choices = [*self.fields['structures'].choices, ('structures', structures_title)]

        if 'memberaudit' in settings.INSTALLED_APPS and user.has_perm('memberaudit.basic_access'):
            from memberaudit.models import Character
            from memberaudit.app_settings import MEMBERAUDIT_APP_NAME

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
                (f"memberaudit-{ownership.character.character_id}", format_lazy("{app_name} - {character_name}", app_name=MEMBERAUDIT_APP_NAME, character_name=ownership.character.character_name))
                for ownership in ownerships
            ]

            self.fields['skills'].choices = [*self.fields['skills'].choices, *choices]

        if 'corptools' in settings.INSTALLED_APPS:
            from corptools.models import CharacterAudit
            from corptools.app_settings import CORPTOOLS_APP_NAME

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
                (f"corptools-{ownership.character.character_id}", format_lazy("{app_name} - {character_name}", app_name=CORPTOOLS_APP_NAME, character_name=ownership.character.character_name))
                for ownership in ownerships
            ]

            self.fields['skills'].choices = [*self.fields['skills'].choices, *choices]

            self.fields['structures'].choices = [*self.fields['structures'].choices, ('corptools', CORPTOOLS_APP_NAME)]

        self.fields['skills'].initial = self.fields['skills'].choices[-1][0]
        self.fields['structures'].initial = self.fields['structures'].choices[-1][0]
