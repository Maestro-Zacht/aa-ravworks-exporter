from allianceauth.eveonline.models import EveCharacter

from corptools.models import Skill, CharacterAudit

from .skill_settings import SKILL_SET


def import_skills(character: EveCharacter):
    skills = Skill.objects.filter(
        character__character=character,
        skill_id__in=SKILL_SET,
    )

    res = {f"skill_{skill.skill_id}": skill.active_skill_level if skill.active_skill_level != 0 else 1 for skill in skills}

    missing_skills = SKILL_SET.difference(skills.values_list('skill_id', flat=True))
    res.update({f"skill_{skill_id}": 1 for skill_id in missing_skills})

    return res


def is_character_added(character: EveCharacter):
    return CharacterAudit.objects.filter(character=character).exists()
