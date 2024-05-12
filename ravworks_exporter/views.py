import json
import re

from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile

from allianceauth.services.hooks import get_extension_logger
from allianceauth.eveonline.models import EveCharacter

from .forms import ExportForm

logger = get_extension_logger(__name__)

skills_re = re.compile(r'^(?P<app>memberaudit|corptools)-(?P<character_id>\d+)$')


@login_required
def index(request):
    if request.method == 'POST':
        form = ExportForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            error = False
            config = json.load(form.cleaned_data['config'])

            if form.cleaned_data['skills']:
                m = skills_re.match(form.cleaned_data['skills'])
                app = m.group('app')
                character = get_object_or_404(EveCharacter, character_id=int(m.group('character_id')))

                if app == 'memberaudit':
                    from .exporters.skills.memberaudit import import_skills, is_character_added

                    if not is_character_added(character):
                        messages.error(request, f"Character {character.character_name} is not added to MemberAudit")
                        error = True
                    else:
                        config.update(import_skills(character))
                elif app == 'corptools':
                    from .exporters.skills.corptools import import_skills, is_character_added

                    if not is_character_added(character):
                        messages.error(request, f"Character {character.character_name} is not added to CorpTools")
                        error = True
                    else:
                        config.update(import_skills(character))

            if form.cleaned_data['structures']:
                from .exporters.structures.structures import export_structures

                config['hidden_my_structures'] = export_structures(request.user)
                config['hidden_allocation_dict'] = {}

            if not error:
                updated_config = ContentFile(json.dumps(config, indent=4).encode())
                return FileResponse(updated_config, as_attachment=True, filename='config.json')

    else:
        form = ExportForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'ravworks_exporter/index.html', context=context)
