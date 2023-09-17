
from collections.abc import Iterator
from Framework.ITestCase import *
from Framework.TestPlantProvider import *

class Case_Sample_00001(ITestCase):
    def name( self ) -> str:
        return "SWE5TST-SAMPLE-00001"

    def description( self ) -> str:
        return "特記事項無し"

    def prepare(self) -> None:
        TestPlantProvider().logger().log("preparing...")
        TestPlantProvider().logger().log("finished")

    
    def steps(self) -> Iterator:# Iterator[bool]: # CPythonは通るが、IronPythonだとエラーになる
        TestPlantProvider().logger().log("Any log.")
        TestPlantProvider().system().test_variable("VariableA", 0 )
        yield True
        TestPlantProvider().system().test_variable("VariableB", 5 )
        yield True
        TestPlantProvider().system().test_variable("VariableC", 10 )
        TestPlantProvider().system().test_variable("VariableD", 55 )
        yield False

    def tear_down(self) -> None:
        TestPlantProvider().logger().log("tear down...")
        TestPlantProvider().logger().log("finished")
