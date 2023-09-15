
from typing import List
from Framework.TestSpec.ITestSuite import *
from Framework.TestSpec.ITestCase import *
from Framework.TestPlantProvider import *

class TestDriver():
    def execute( self, suites : List[ITestSuite]) -> None:
        self.__prepare()
        self.__execute( suites )
        self.__tear_down()

    def __prepare( self ) -> None:
        TestPlantProvider().setup()
        TestPlantProvider().logger().start_test()

    def __execute( self, suites : List[ITestSuite] ) -> None:

        for suite in suites:
            TestPlantProvider().logger().start_suite( suite )
            suite.prepare()

            for testcase in suite.testcases():
                TestPlantProvider().logger().start_case( testcase )
                testcase.prepare()

                steps = testcase.steps()
                while True:
                    TestPlantProvider().logger().start_step()
                    try:
                        if (not next(steps)):
                            break
                    except StopIteration:
                        break
                    finally:
                        TestPlantProvider().logger().end_step()

                testcase.tear_down()
                TestPlantProvider().logger().end_case()

            suite.tear_down()
            TestPlantProvider().logger().end_suite()
        pass

    def __tear_down( self ) -> None:
        TestPlantProvider().logger().end_test()
        TestPlantProvider().tear_down()





