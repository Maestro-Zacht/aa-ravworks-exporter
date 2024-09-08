from corptools.models import CorpAsset, Structure

from .structures_settings import AVAIABLE_RIGS


def export_structures(user):
    structures = (
        Structure
        .get_visible(user)
        .filter(type_name__group__category_id=65)
        .exclude(type_name_id=81826)
        .select_related('system_name')
    )
    res = []

    for i, structure in enumerate(structures, 1):
        rig_items = CorpAsset.get_visible(user).filter(
            location_flag__icontains="rig",
            location_id=structure.structure_id,
            type_name__name__in=AVAIABLE_RIGS,
        ).values_list('type_name__name', flat=True).distinct()

        rigs = {f"Rig{j}": "No Rig" for j in range(1, 4)}

        for j, rig in enumerate(rig_items, 1):
            rigs[f"Rig{j}"] = rig

        if round(structure.system_name.security_status, 1) >= 0.5:
            security = 'High'
        elif 0 < round(structure.system_name.security_status, 1) < 0.5:
            security = 'Low'
        else:
            security = 'Null / Wormhole'

        res.append({
            'id': f"Structure {i}",
            'name': structure.name,
            'security': security,
            'structure': structure.type_name.name,
            **rigs,
        })

    return res
