import sys
from pathlib import Path
import pytest

etabs_api_path = Path(__file__).parent.parent
sys.path.insert(0, str(etabs_api_path))

if 'shayesteh19' not in dir(__builtins__):
    from shayesteh import *

FREECADPATH = 'G:\\program files\\FreeCAD 0.19\\bin'
sys.path.append(FREECADPATH)
import FreeCAD

filename = Path(__file__).absolute().parent / 'files' / 'freecad' / 'strip.FCStd'
filename_mat = Path(__file__).absolute().parent / 'files' / 'freecad' / 'mat.FCStd'
document= FreeCAD.openDocument(str(filename))

def test_get_names_of_areas_of_type():
    area_names = etabs.area.get_names_of_areas_of_type(type_='floor')
    assert len(area_names) == 232
    
def test_calculate_deck_weight_per_area():
    df = etabs.area.calculate_deck_weight_per_area()
    print(df)
    df = etabs.area.calculate_deck_weight_per_area(use_user_deck_weight=False)
    print(df)

def test_calculate_slab_weight_per_area():
    df = etabs.area.calculate_slab_weight_per_area()
    print(df)

def test_get_expanded_shell_uniform_load_sets():
    df = etabs.area.get_expanded_shell_uniform_load_sets()
    print(df)

def test_get_shell_uniform_loads():
    df = etabs.area.get_shell_uniform_loads()
    # assert len(df) == 200
    print(df)

def test_get_all_slab_types():
    d = etabs.area.get_all_slab_types()
    assert d['SLAB1'] == d['SLAB2'] == d['PLANK1']


def test_calculate_equivalent_height_according_to_volume():
    import area
    h_equal = area.calculate_equivalent_height_according_to_volume(
        s1=800, s2=800, d=380, tw1=130, tw2=130, hc=100
    )
    assert pytest.approx(h_equal, abs=.1) == 183.6

def test_deck_plate_equivalent_height_according_to_volume():
    import area
    h_equal = area.deck_plate_equivalent_height_according_to_volume(
        s=800, d=380, tw_top=140, tw_bot=120, hc=100, t_deck=50
    )
    assert pytest.approx(h_equal, abs=.01) == 1340.357

if __name__ == '__main__':
    test_calculate_slab_weight_per_area()