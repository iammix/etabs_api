from typing import Union

__all__ = ['Analyze']


class Analyze:
    def __init__(self, SapModel=None, etabs=None, ):
        if not SapModel:
            self.etabs = etabs
            self.SapModel = etabs.SapModel
        else:
            self.SapModel = SapModel

    def set_load_cases_to_analyze(self, load_cases='all_load_cases'):
        if load_cases == "all_load_cases":
            self.SapModel.Analyze.SetRunCaseFlag('all_load_cases', True, True)
            return
        self.SapModel.Analyze.SetRunCaseFlag('all_load_cases', False, True)
        all_load_case = self.SapModel.Analyze.GetCaseStatus()[1]
        if not isinstance(load_cases, (list, tuple, set)):
            load_cases = [load_cases]
        for lc in load_cases:
            if lc in all_load_case:
                self.SapModel.Analyze.SetRunCaseFlag(lc, True)

    def change_run_status_of_load_cases(self, load_cases: Union[list, None] = None, run_flag=True, ):
        all_load_cases = self.SapModel.Analyze.GetCaseStatus()[1]
        if load_cases is None:
            load_cases = all_load_cases
        for lc in load_cases:
            if lc in all_load_cases:
                self.SapModel.Analyze.SetRunCaseFlag(lc, run_flag)
