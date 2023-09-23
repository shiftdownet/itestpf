
from collections.abc import Iterator
from Framework.ITestSuite import *

from Suites.Cases.Case_Sample_00001 import *

class Suite_Sample1(ITestSuite):
    count = 0
    def name( self ) -> str:
        Suite_Sample1.count += 1
        return "SWE5-SUITE-SAMPLE-" + str(Suite_Sample1.count)

    def description( self ) -> str:
        return "特記事項無し"

    def testcases(self) -> Iterator:# Iterator[ITestCase]: # CPythonは通るが、IronPythonだとエラーになる
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()
        yield Case_Sample_00001()

    def prepare(self) -> None:
        TestPlantProvider().logger().log("preparing...")
        TestPlantProvider().logger().log("finished")

    def tear_down(self) -> None:
        TestPlantProvider().logger().log("tear_down...")
        TestPlantProvider().logger().log("finished")

