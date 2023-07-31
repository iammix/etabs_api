import sys
from pathlib import Path
import pytest

etabs_api_path = Path(__file__).parent.parent
sys.path.insert(0, str(etabs_api_path))

if 'etabs' not in dir(__builtins__):
    from shayesteh import etabs, open_model, version

def test_set_concrete_framing_type():
    etabs.design.set_concrete_framing_type()
    beam_names, column_names = etabs.frame_obj.get_beams_columns(type_=2)
    etabs.SapModel.DesignConcrete.SetCode("ACI 318-19")
    etabs.design.set_concrete_framing_type()
    for name in beam_names + column_names:
        ret = etabs.SapModel.DesignConcrete.ACI318_19.GetOverwrite(name,1)
        assert ret[0] == 2
    etabs.design.set_concrete_framing_type(type_=1)
    for name in beam_names + column_names:
        ret = etabs.SapModel.DesignConcrete.ACI318_19.GetOverwrite(name,1)
        assert ret[0] == 1

def test_get_code_string():
    code = "ACI 318-08"
    code_string = etabs.design.get_code_string(code=code)
    assert code_string == "ACI318_08_IBC2009"

def test_set_phi_joint_shear_aci19():
    phi_joint_shear = 0.87
    etabs.SapModel.DesignConcrete.SetCode("ACI 318-19")
    etabs.design.set_phi_joint_shear(value=phi_joint_shear)
    ret = etabs.SapModel.DesignConcrete.ACI318_19.GetPreference(15)
    assert ret[0] == phi_joint_shear

def test_set_phi_joint_shear_aci14():
    phi_joint_shear = 0.87
    etabs.SapModel.DesignConcrete.SetCode("ACI 318-14")
    etabs.design.set_phi_joint_shear(value=phi_joint_shear)
    ret = etabs.SapModel.DesignConcrete.ACI318_14.GetPreference(15)
    assert ret[0] == phi_joint_shear

def test_set_phi_joint_shear_aci11():
    phi_joint_shear = 0.87
    etabs.SapModel.DesignConcrete.SetCode("ACI 318-11")
    etabs.design.set_phi_joint_shear(value=phi_joint_shear)
    ret = etabs.SapModel.DesignConcrete.ACI318_11.GetPreference(15)
    assert ret[0] == phi_joint_shear

def test_set_phi_joint_shear_aci08():
    phi_joint_shear = 0.87
    etabs.SapModel.DesignConcrete.SetCode("ACI 318-08/IBC 2009")
    etabs.design.set_phi_joint_shear(value=phi_joint_shear)
    ret = etabs.SapModel.DesignConcrete.ACI318_08_IBC2009.GetPreference(10)
    assert ret[0] == phi_joint_shear

def test_get_rho():
    rho, _ = etabs.design.get_rho('130', distance=0)
    assert pytest.approx(rho, abs=.0001) == .01517

def test_get_deflection_of_beam():
    open_model(etabs=etabs, filename='madadi.EDB')
    dead = etabs.load_patterns.get_special_load_pattern_names(1)
    supper_dead = etabs.load_patterns.get_special_load_pattern_names(2)
    l1 = etabs.load_patterns.get_special_load_pattern_names(3)
    l2 = etabs.load_patterns.get_special_load_pattern_names(4)
    l3 = etabs.load_patterns.get_special_load_pattern_names(11)
    lives = l1 + l2 + l3
    def1, def2, _ = etabs.design.get_deflection_of_beam(
        dead=dead,
        supper_dead=supper_dead,
        lives=lives,
        beam_name='157',
        distance_for_calculate_rho='middle',
    )
    assert pytest.approx(def1, abs=.001) == 1.5722
    assert pytest.approx(def2, abs=.001) == 2.25477

def test_get_deflection_of_beam_console():
    open_model(etabs=etabs, filename='madadi.EDB')
    dead = etabs.load_patterns.get_special_load_pattern_names(1)
    supper_dead = etabs.load_patterns.get_special_load_pattern_names(2)
    l1 = etabs.load_patterns.get_special_load_pattern_names(3)
    l2 = etabs.load_patterns.get_special_load_pattern_names(4)
    l3 = etabs.load_patterns.get_special_load_pattern_names(11)
    lives = l1 + l2 + l3
    etabs.design.get_deflection_of_beam(
        dead=dead,
        supper_dead=supper_dead,
        lives=lives,
        beam_name='129',
        distance_for_calculate_rho='end', #The frame is reverse
        is_console=True,
        rho=0.00579,
    )
    assert True

def test_get_deflection_check_result():
    open_model(etabs=etabs, filename='madadi.EDB')
    import design
    text = design.get_deflection_check_result(
        -1.8,
        -2.4,
        800,
    )
    print(text)
    assert type(text) == str
