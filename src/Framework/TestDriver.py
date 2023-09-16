
from typing import List
from Framework.ITestProject import ITestProject
from Framework.TestSpec.ITestSuite import ITestSuite
from Framework.TestPlantProvider import TestPlantProvider

class TestDriver():
    def launch( self, project : ITestProject) -> None:
        self.__project = project
        self.__prepare()
        self.__execute()
        self.__tear_down()

    def __prepare( self ) -> None:
        TestPlantProvider().setup( self.__project )
        TestPlantProvider().logger().start_test()

    def __execute( self ) -> None:

        for suite in self.__project.suites():
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

