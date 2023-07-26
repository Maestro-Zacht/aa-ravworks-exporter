from structures.models import Structure
from structures.constants import EveCategoryId

from .structures_settings import AVAIABLE_RIGS

FIT_PERMISSIONS = ["structures.view_structure_fit"]


def extract_slot_assets(fittings: list, slot_name: str) -> list:
    """Return assets for slot sorted by slot number"""
    return [
        asset[0]
        for asset in sorted(
            [
                (asset, asset.location_flag[-1])
                for asset in fittings
                if asset.location_flag.startswith(slot_name)
            ],
            key=lambda x: x[1],
        )
    ]


def export_structures(user):
    res = []
    if user.has_perms(FIT_PERMISSIONS):
        structures = (
            Structure.objects
            .visible_for_user(user)
            .filter(eve_type__eve_group__eve_category_id=EveCategoryId.STRUCTURE)
            .select_related("eve_solar_system", 'eve_type')
            .prefetch_related('items__eve_type')
        )

        for i, structure in enumerate(structures, 1):
            assets = structure.items.all()
            rig_slots = extract_slot_assets(assets, "RigSlot")

            rigs = {f"Rig{j}": "No Rig" for j in range(1, 4)}

            for j, rig in enumerate(rig_slots, 1):
                if rig.eve_type.name in AVAIABLE_RIGS:
                    rigs[f"Rig{j}"] = rig.eve_type.name

            if structure.eve_solar_system.is_high_sec:
                security = 'High'
            elif structure.eve_solar_system.is_low_sec:
                security = 'Low'
            else:
                security = 'Null / Wormhole'

            res.append({
                'id': f"Structure {i}",
                'name': structure.name,
                'security': security,
                'structure': structure.eve_type.name,
                **rigs,
            })

    return res
