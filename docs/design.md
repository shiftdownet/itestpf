---
# Setting for Markdown Preview Enhanced v0.6.3
toc:                        # 目次設定
  depth_from: 1             # - 目次化する開始ネスト
  depth_to: 4               # - 目次化する終了ネスト
  ordered: false            # - オーダーを表示しない
html:                       # HTMLファイル出力に関する設定
  embed_local_images: true  # - ローカル埋め込み画像ファイルを有効にする
  embed_svg: true           # - SVGの埋め込みを有効にする
  offline: true             # - offlineでの生成を有効にする
  toc: true                 # - デフォルトでサイドバーにTOCを表示する
export_on_save:             # ファイル保存時の振る舞い
  html: true                # - htmlで出力(※Markdown PDF等他のAddinの自動保存機能は無効化してください)
---



# 1. テストプラント


```plantuml
!include ./objects.iuml

remove TestCaseX
remove TestSuiteX
remove TestSpec

'skinparam groupInheritance 2
Framework.Logger.XmlTestLogger -up[hidden]-- ITestLogger
Framework.TestPlantProvider *-up-> Framework.Logger.XmlTestLogger : <<composite>>\n生成し保持します
Framework.TestPlantProvider -up.> Framework.TestPlant.CsPlusSimulator : <<create>>\n生成しデコレータに渡します。
Framework.TestPlantProvider *-up-> Framework.TestPlant.TestSystemCallNotifier : <<composite>>\n生成し保持します
Framework.TestPlant.TestSystemCallNotifier o-up- Framework.TestPlant.ITestSystem : <<aggregate>>\nコンストラクタで受け取った\nインスタンスを保有します


circle "ITestSystem" as Framework.Logger.ITestSystem_Implements_By

Framework.TestPlant.TestSystemCallNotifier -( Framework.Logger.ITestSystem_Implements_By : <<notify>>\nテストシステムの\nコールを通知します
Framework.Logger.XmlTestLogger - Framework.Logger.ITestSystem_Implements_By


```


# 2. テスト仕様の構成


```plantuml
!include ./objects.iuml

remove TestPlantProvider
remove Logger
remove TestPlant
remove ITestLogger
remove ITestSystem
remove ITestSystemDecorator

TestEntry "1" -ri-> "*" TestSuiteX : <<create>>\n生成しTestDriverに渡します。
TestEntry -up-> TestDriver : <<delegate>>\nexecute( テストスイートのインスタンス )\nの形でテストを実行します
TestDriver -> ITestSuite : <<call>>\n
ITestSuite "1" *-> "*" ITestCase : <<composite>>\n生成し保持します
TestSuiteX "1" *-> "*" TestCaseX : <<composite>>\n生成し保持します

TestDriver -> ITestCase : <<call>> \nITestSuiteから取得したテストケースを\n順番に実行します。

```

# 3. テスト仕様とテストプラントの関係

```plantuml
!include ./objects.iuml

remove Logger
remove TestPlant
remove $interface
remove $abstract


TestDriver -> TestPlantProvider

TestSuiteX -up-> TestPlantProvider
TestCaseX -up-> TestPlantProvider


```

# 4. ログ仕様のイメージ

```xml
<Test>
    <Summary>
        <Date>テストの日時</Date>
        <TimeSpent>テストの実行時間</TimeSpent>
        <Total>テストの総数</Total>
        <Passed>合格したテスト件数</Passed>
        <Failed>不合格のテスト件数</Failed>
    </Summary>
    <TestSuite name="TEST-SUITE-A">
        <Summary>
            <Total>1</Total>
            <Passed>0</Passed>
            <Failed>1</Failed>
        </Summary>
        <Log>
            <Prepare></Prepare>
            <TestCases>
                <TestCase name="SWE5TST-CASE-1">
                    <result>Failed</result>
                    <Prepare></Prepare>
                    <Steps>
                        <Step number="1">
                            <result>Passed</result>
                            <Message>前提条件を設定する</Message>
                            <Write to="Rte_Input_Interface" as="0x55"><Write>
                        </Step>
                        <Step number="2">
                            <result>Passed</result>
                            <Message>期待値1を確認する</Message>
                            <Assert name="Rte_Output_Interface1">
                                <Format>hex</Format>
                                <Expect>00 55 AA FF</Expect>
                                <Actual>00 55 AA FF</Actual>
                            </Assert>
                        </Step>
                        <Step number="3">
                            <result>Failed</result>
                            <Message>期待値2を確認する</Message>
                            <Assert name="Rte_Output_Interface2">
                                <Format>dec</Format>
                                <Expect>65535</Expect>
                                <Actual>0</Actual>
                            </Assert>
                        </Step>
                    </Steps>
                    <TearDown></TearDown>
                </TestCase>
            </TestCases>
            <TearDown></TearDown>
        <Log>
    </TestSuite>
</Test>
```

# 5. 実行シーケンス

```plantuml
!pragma teoz true
skinparam SequenceLifeLineBackgroundColor LightSteelBlue

participant IronPythonConsole

participant TestEntry
box Framework
    participant TestDriver
    box Logger
        participant XmlTestLogger
    endbox
    box TestPlant
        participant CsPlusSimulator
        participant TestSystemCallNotifier
        participant TestPlantProvider
    endbox
endbox

participant TestSuiteX
participant TestCaseX

autoactivate on

activate IronPythonConsole

IronPythonConsole -> TestEntry  : execute()

    create TestSuiteX
    TestEntry -> TestSuiteX  : __init()\n ※スイート数だけ生成
    return


    '#----------------------------------------------------
    '# TestDriver.execute()
    '#----------------------------------------------------
    TestEntry -> TestDriver  : execute( TestSuiteX[] )

        TestDriver -> TestDriver  : prepare()
            hnote over TestDriver : ファイルオープン
            '#----------------------------------------------------
            '# TestPlantProvider.setup()
            '#----------------------------------------------------
            TestDriver -> TestPlantProvider  : setup()
                create XmlTestLogger
                TestPlantProvider -> XmlTestLogger  : set_stream( stream )
                return
               
                create CsPlusSimulator
                TestPlantProvider -> CsPlusSimulator  : __init()
                return
                create TestSystemCallNotifier
                TestPlantProvider -> TestSystemCallNotifier  :  __init( instance of CsPlusSimulator )
                return
            return
        return

        TestDriver -> XmlTestLogger  : TestPlantProvider.logger.start_test()
        return

        loop すべてのテストスイートが実行し終わるまで

            TestDriver -> XmlTestLogger : TestPlantProvider.logger.start_suite( suite_name )
            return
            TestDriver -> TestSuiteX  : prepare()
            return

            loop ジェネレータがテストケースを返さなくなるまで
                TestDriver -> TestSuiteX : testcases()\nテストケースをジェネレータで\n1件づつ取得
                return
                TestDriver -> TestDriver : execute_testcase( testcase )
                    TestDriver -> XmlTestLogger : TestPlantProvider.logger.start_case( case_name )
                    return
                    TestDriver -> TestCaseX : prepare()
                    return
                    loop ジェネレータがテストステップを返さなくなるまで
                        TestDriver -> XmlTestLogger : TestPlantProvider.logger.start_step()
                        return
                        TestDriver -> TestCaseX : steps()
                            TestCaseX -> TestSystemCallNotifier : TestPlantProvider.system.assert( 変数名, 期待値 )
                                TestSystemCallNotifier -> CsPlusSimulator : assert( 変数名, 期待値 )
                                return
                                TestSystemCallNotifier -> XmlTestLogger : assert( 変数名, 期待値 )
                                return
                            return
                        return
                        TestDriver -> XmlTestLogger : TestPlantProvider.logger.end_step()
                        return
                    end loop
                    TestDriver -> TestCaseX : tear_down()
                    return
                    TestDriver -> XmlTestLogger : TestPlantProvider.logger.end_case( case_name )
                    return
                return

            end loop

            TestDriver -> TestSuiteX  : tear_down()
            return

            TestDriver -> XmlTestLogger : TestPlantProvider.logger.end_suite( suite_name )
            return
        end loop

        TestDriver -> TestDriver  : tear_down()
            TestDriver -> XmlTestLogger  : TestPlantProvider.logger.end_test()
            return
            hnote over TestDriver : ファイルクローズ
        return
    return

return



'TestEntry 


```


