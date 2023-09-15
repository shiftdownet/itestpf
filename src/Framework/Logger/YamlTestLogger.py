

from Framework.TestPlant.ITestSystem import *
from Framework.Logger.ITestLogger import *
from Framework.TestSpec.ITestSuite import *
from Framework.TestSpec.ITestCase import *

class YamlTestLogger(ITestLogger, ITestSystem):
    #--------------------------------------------------
    # ITestLogger
    #--------------------------------------------------
    def set_stream(self, stream) -> None:
        self.stream = stream
        self.step_no = 0
        self.nest = 0

    def log(self, message: str) -> None:
        self.stream.write( message )

    def start_test(self) -> None:
        self.stream.write( self.__format("test:") )
        self.nest+=1
        self.stream.write( self.__format("suites:") )
        self.nest+=1

    def start_suite(self, suite: ITestSuite) -> None:
        self.stream.write( self.__format("-") )
        self.nest+=1
        self.stream.write( self.__format("name: " + self.__dq(suite.name())) )
        self.stream.write( self.__format("description: " + self.__dq(suite.description())) )
        self.stream.write( self.__format("test_cases:") )
        self.nest+=1

    def start_case(self, testcase: ITestLogger) -> None:
        self.stream.write( self.__format("-") )
        self.nest+=1
        self.stream.write( self.__format("name: " + self.__dq(testcase.name())) )
        self.stream.write( self.__format("description: " + self.__dq(testcase.description())) )
        self.step_no = 0
        self.stream.write( self.__format("steps:") )
        self.nest+=1

    def start_step(self) -> None:
        self.step_no += 1
        self.stream.write( self.__format("-") )
        self.nest+=1
        self.stream.write( self.__format("number: " + str(self.step_no) ) )
        self.stream.write( self.__format("commands:") )
        self.nest+=1

    def end_step(self) -> None:
        self.nest-=1
        self.nest-=1

    def end_case(self) -> None:
        self.nest-=1
        self.nest-=1

    def end_suite(self) -> None:
        self.nest-=1
        self.nest-=1

    def end_test(self) -> None:
        self.nest-=1
        self.nest-=1

    #--------------------------------------------------
    # ITestSystem
    #--------------------------------------------------
    def test_variable(self, variable_name, expected_value) -> bool:
        self.stream.write( self.__format("-") )
        self.nest+=1
        self.stream.write( self.__format("command: " + self.__dq("test_variable") ))
        self.stream.write( self.__format("actual: " + self.__dq(variable_name) ) )
        self.stream.write( self.__format("expect: " + str(expected_value) ) )
        self.nest-=1
        return True

    #--------------------------------------------------
    # private
    #--------------------------------------------------
    def __dq( self, item:str) -> str:
        return "\"" + item + "\""

    def __format( self, item:str) -> str:
        return self.__indent() + str(item) + "\n"

    def __indent( self ) -> str:
        return "  " * self.nest
