import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_planet_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Fully-qualified tag names (namespace-expanded)
    illum_az_tag = '{http://earth.esa.int/opt}illuminationAzimuthAngle'
    illum_el_tag = '{http://earth.esa.int/opt}illuminationElevationAngle'
    ps_az_tag = '{http://schemas.planet.com/ps/v1/planet_product_metadata_geocorrected_level}azimuthAngle'
    sc_view_tag = '{http://schemas.planet.com/ps/v1/planet_product_metadata_geocorrected_level}spaceCraftViewAngle'

    def get_float(tag):
        el = root.find('.//' + tag)
        if el is None or el.text is None:
            raise ValueError(f"Missing tag: {tag}")
        return float(el.text)

    illum_az = get_float(illum_az_tag)
    illum_el = get_float(illum_el_tag)
    ps_az = get_float(ps_az_tag)
    sc_view = get_float(sc_view_tag)

    # Compute sun zenith from illumination elevation
    sun_zenith = 90.0 - illum_el
    sun_azimuth = illum_az

    view_zenith = sc_view
    view_azimuth = ps_az

    return {
        'sun_zenith': sun_zenith,
        'sun_azimuth': sun_azimuth,
        'view_zenith': view_zenith,
        'view_azimuth': view_azimuth,
    }


def parse_aerdb_json(json_path):
    with open(json_path, 'r') as fh:
        d = json.load(fh)

    vars = d.get('variables', {})
    aod = vars.get('AOD_550', {}).get('median')
    water = vars.get('Precipitable_Water', {}).get('median')
    ozone = vars.get('Total_Column_Ozone', {}).get('median')

    if aod is None or water is None or ozone is None:
        raise ValueError('AERDB JSON missing expected median values')

    return {
        'aod550': float(aod),
        'water': float(water),
        'ozone': float(ozone),
    }


def main():
    p = argparse.ArgumentParser(description='Extract geometry and atmospheric representatives')
    p.add_argument('--xml', default='data/20250124_181752_33_2532_basic_analytic_4b_xml.xml')
    p.add_argument('--aerdb', default='data/aerdb_representative_values.json')
    args = p.parse_args()

    xml_path = Path(args.xml)
    aerdb_path = Path(args.aerdb)

    if not xml_path.exists():
        raise SystemExit(f'XML not found: {xml_path}')
    if not aerdb_path.exists():
        raise SystemExit(f'AERDB JSON not found: {aerdb_path}')

    geom = parse_planet_xml(xml_path)
    atm = parse_aerdb_json(aerdb_path)

    # Print as Python assignment lines for easy copy-paste into a notebook
    print(f"sun_zenith  = {geom['sun_zenith']:.5f}")
    print(f"sun_azimuth = {geom['sun_azimuth']:.5f}")
    print(f"view_zenith = {geom['view_zenith']:.5f}")
    print(f"view_azimuth= {geom['view_azimuth']:.5f}")
    print()
    print(f"aod550 = {atm['aod550']:.5f}")
    print(f"water  = {atm['water']}  # cm")
    print(f"ozone  = {atm['ozone']}   # atm-cm")


if __name__ == '__main__':
    main()
