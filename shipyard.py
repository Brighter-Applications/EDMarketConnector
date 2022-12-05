"""Export list of ships as CSV."""
import csv

import companion
from edmc_data import ship_name_map


def export(data: companion.CAPIData, filename: str) -> None:
    """
    Write shipyard data in Companion API JSON format.

    :param data: The CAPI data.
    :param filename: Optional filename to write to.
    :return:
    """
    assert data['lastSystem'].get('name')
    assert data['lastStarport'].get('name')
    assert data['lastStarport'].get('ships')

    with open(filename, 'w', newline='') as f:
        c = csv.writer(f)
        c.writerow(('System', 'Station', 'Ship', 'FDevID', 'Date'))

        for (name, fdevid) in [
            (
                ship_name_map.get(ship['name'].lower(), ship['name']),
                ship['id']
            ) for ship in list(
                (data['lastStarport']['ships'].get('shipyard_list') or {}).values()
            ) + data['lastStarport']['ships'].get('unavailable_list')
        ]:
            c.writerow((
                data['lastSystem']['name'], data['lastStarport']['name'],
                name, fdevid, data['timestamp']
            ))
