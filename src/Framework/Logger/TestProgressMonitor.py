
from Framework.TestPlant.ITestSystem import ITestSystem
from Framework.Logger.ITestLogger import ITestLogger
from Framework.ITestSuite import ITestSuite
from Framework.ITestCase import ITestCase
from Framework.TestPlantProvider import TestPlantProvider

class TestProgressMonitor(ITestLogger, ITestSystem):
    def __init__(self):
        self.step_no = 1
        self.nest = 0
        self.passed_count_of_suite = 0
        self.failed_count_of_suite = 0
        self.passed_count_of_case = 0
        self.failed_count_of_case = 0
        self.passed_count_of_step = 0
        self.failed_count_of_step = 0
        self.passed_count_of_command = 0
        self.failed_count_of_command = 0
        self.total_passed_count_of_case = 0
        self.total_failed_count_of_case = 0
    #--------------------------------------------------
    # ITestLogger
    #--------------------------------------------------
    def set_stream(self, stream) -> None:
        self.stream = stream

    def log(self, message: str) -> None:
        pass

    def start_test(self) -> None:
        self.nest+=1
        self.passed_count_of_suite = 0
        self.failed_count_of_suite = 0

    def start_suite(self, suite: ITestSuite) -> None:
        self.nest+=1
        self.passed_count_of_case = 0
        self.failed_count_of_case = 0

    def start_case(self, testcase: ITestCase) -> None:
        self.nest+=1
        self.passed_count_of_step = 0
        self.failed_count_of_step = 0
        self.step_no = 1

    def start_step(self) -> None:
        self.nest+=1
        self.passed_count_of_command = 0
        self.failed_count_of_command = 0
        self.step_no+=1

    def end_step(self) -> None:
        self.nest-=1
        if self.failed_count_of_command == 0:
            self.passed_count_of_step += 1
        else:
            self.failed_count_of_step += 1

    def end_case(self) -> None:
        self.nest-=1
        if self.failed_count_of_step == 0:
            self.passed_count_of_case += 1
        else:
            self.failed_count_of_case += 1

    def end_suite(self) -> None:
        self.nest-=1
        if self.failed_count_of_case == 0:
            self.passed_count_of_suite += 1
        else:
            self.failed_count_of_suite += 1
        self.total_passed_count_of_case += self.passed_count_of_case
        self.total_failed_count_of_case += self.failed_count_of_case

    def end_test(self) -> None:
        self.nest-=1

    #--------------------------------------------------
    # ITestSystem
    #--------------------------------------------------
    def test_variable(self, variable_name, expected_value) -> bool:
        actual_value = TestPlantProvider().system().get_value_by( variable_name )

        if actual_value == expected_value:
            self.passed_count_of_command += 1
            return True
        else:
            self.failed_count_of_command += 1
            return False

    def get_value_by( self, variable_name : str ):
        return 0 # 実装不要
