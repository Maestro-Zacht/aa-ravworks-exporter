from allianceauth.eveonline.models import EveCharacter

from memberaudit.models import CharacterSkill, Character

from .skill_settings import SKILL_SET


def import_skills(character: EveCharacter):
    skills = CharacterSkill.objects.filter(
        character__eve_character=character,
        eve_type_id__in=SKILL_SET,
    )

    return {f"skill_{skill.eve_type_id}": skill.active_skill_level if skill.active_skill_level != 0 else 1 for skill in skills}


def is_character_added(character: EveCharacter):
    return Character.objects.filter(eve_character=character).exists()
