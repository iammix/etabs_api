import sys
from pathlib import Path
import pytest
import comtypes.client

etabs_api_path = Path(__file__).parent.parent
sys.path.insert(0, str(etabs_api_path))
from load_combinations import generate_concrete_load_combinations

import etabs_obj

Tx_drift, Ty_drift = 1.085, 1.085

@pytest.fixture
def shayesteh(edb="shayesteh.EDB"):
    try:
        etabs = etabs_obj.EtabsModel(backup=False)
        if etabs.success:
            filepath = Path(etabs.SapModel.GetModelFilename())
            if 'test.' in filepath.name:
                return etabs
            else:
                raise NameError
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        helper = comtypes.client.CreateObject('ETABSv1.Helper') 
        helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
        ETABSObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
        ETABSObject.ApplicationStart()
        SapModel = ETABSObject.SapModel
        SapModel.InitializeNewModel()
        SapModel.File.OpenFile(str(Path(__file__).parent / 'files' / edb))
        asli_file_path = Path(SapModel.GetModelFilename())
        dir_path = asli_file_path.parent.absolute()
        test_file_path = dir_path / "test.EDB"
        SapModel.File.Save(str(test_file_path))
        etabs = etabs_obj.EtabsModel(backup=False)
        return etabs

@pytest.mark.setmethod
def test_create_concrete_beam(shayesteh):
    ret = shayesteh.prop_frame.create_concrete_beam('B20X20', 'C25', 200, 200, 'S400', 'S340', 400)
    assert ret

@pytest.mark.setmethod
def test_create_concrete_column(shayesteh):
    ret = shayesteh.prop_frame.create_concrete_column('C50X80', 'C25', 800, 500, 'S400', 'S340', 75, 3, 6, '20', '10')
    assert ret


if __name__ == '__main__':
    from pathlib import Path
    etabs_api = Path(__file__).parent.parent
    import sys
    sys.path.insert(0, str(etabs_api))
    from etabs_obj import EtabsModel
    etabs = EtabsModel(backup=False)
    SapModel = etabs.SapModel
    test_add_load_combination(etabs)