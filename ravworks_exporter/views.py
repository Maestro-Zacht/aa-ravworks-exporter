import json

from django.shortcuts import render
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile

from allianceauth.services.hooks import get_extension_logger

from .forms import ExportForm

logger = get_extension_logger(__name__)


@login_required
def index(request):
    if request.method == 'POST':
        form = ExportForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            error = False
            config = json.load(form.cleaned_data['config'])
            ownership = (
                request.user.character_ownerships
                .select_related('character')
                .get(character__character_id=form.cleaned_data['character'])
            )

            if form.cleaned_data['skills'] == 'memberaudit':
                from .exporters.skills.memberaudit import import_skills, is_character_added

                if not is_character_added(ownership.character):
                    messages.error(request, f"Character {ownership.character.character_name} is not added to MemberAudit")
                    error = True
                else:
                    config.update(import_skills(ownership.character))
            elif form.cleaned_data['skills'] == 'corptools':
                from .exporters.skills.corptools import import_skills, is_character_added

                if not is_character_added(ownership.character):
                    messages.error(request, f"Character {ownership.character.character_name} is not added to CorpTools")
                    error = True
                else:
                    config.update(import_skills(ownership.character))

            if form.cleaned_data['structures']:
                from .exporters.structures.structures import export_structures

                config['hidden_my_structures'] = export_structures(ownership.user)

            if not error:
                updated_config = ContentFile(json.dumps(config, indent=4).encode())
                return FileResponse(updated_config, as_attachment=True, filename='config.json')

    else:
        form = ExportForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'ravworks_exporter/index.html', context=context)
