from structures.models import Structure


def export_structures(user):
    structures = (
        Structure.objects
        .visible_for_user(user)
        .filter(eve_type__eve_group__eve_category__name='Structure')
    )
