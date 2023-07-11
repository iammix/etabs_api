import sys
from pathlib import Path
import pytest

etabs_api_path = Path(__file__).parent.parent
sys.path.insert(0, str(etabs_api_path))

from shayesteh import shayesteh

@pytest.mark.getmethod
def test_get_xy_period():
    Tx, Ty, i_x, i_y = etabs.results.get_xy_period()
    assert pytest.approx(Tx, abs=.01) == 1.291
    assert pytest.approx(Ty, abs=.01) == 1.291
    assert i_x == 2
    assert i_y == 2

def test_get_base_react():
    vx, vy = etabs.results.get_base_react()
    assert vx == pytest.approx(-110709.5, .1)
    assert vy == pytest.approx(-110709.5, .1)

def test_get_base_react_loadcases():
    V = etabs.results.get_base_react(
        loadcases=['QX', 'QY', 'SPX'],
        directions=['x', 'y', 'x'],
        absolute=True,
        )
    assert V[0] == pytest.approx(110709.5, .1)
    assert V[1] == pytest.approx(110709.5, .1)
    assert V[2] == pytest.approx(58251.6, .1)

def test_get_point_abs_displacement():
    etabs.set_current_unit('N', 'cm')
    etabs.run_analysis()
    V = etabs.results.get_point_abs_displacement(
        '116',
        'DEAD',
        )
    assert V == pytest.approx((-.0508, .1243, -.0199), abs=.001)

def test_get_point_displacement():
    etabs.set_current_unit('N', 'cm')
    etabs.run_analysis()
    V = etabs.results.get_point_displacement(
        '116',
        'DEAD',
        )
    assert V == pytest.approx((-.0508, .1243, -.0199), abs=.001)