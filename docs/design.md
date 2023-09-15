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

remove TestDriver
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
                TestPlantProvider -> TestSystemCallNotifier  :  set_notifee( instance of XmlTestLogger )
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


<header id="header"><div id="title">{meta.documentName}</div><div id="document_info"><div id="document_id">{meta.documentID}-{meta.version}</div><div id="version">{meta.version}</div></div></header>
<footer id="footer">- {meta.issued} - CONFIDENTIAL</footer>
<style> header { position:fixed !important; height: 60px; width:100%; z-index:3000; top: 0px; left:0px; background-color: rgba(255,255,255,0.8); border-bottom: 1px solid gray !important; box-sizing: border-box;} #title { padding-left:0.5em; font-size:20px; font-weight:bold; } #document_info { display:block; position:fixed; top:0.5em; right:1em; font-weight:bold; color:#666, font-size:14px; text-align:right;} #document_id::before {content:"DOCUMENT ID: "} #version { display:inline;} #version::before { content: "VERSION: "} footer { position:fixed !important; bottom:0px; left:0px; width:100%; height:20px; z-index:3500; background-color:white; border-top: 1px solid slategray; text-align:center; font-size:15px; color:#333; font-weight:bold; } .md-sidebar-toc{ top:60px !important; height: calc(100% - 60px - 20px) !important; overflow:scroll !important; white-space:nowrap; font-size:12px !important; } .markdown-preview { margin:0 !important; padding: 1em 1em 1em 1em !important; position:fixed !important; top:60px !important; height:calc(100% - 60px) !important; overflow:scroll !important;} html body[for="html-export"]:not([data-presentation-mode]):not([html-show-sidebar-toc]) .markdown-preview{left:0% !important; transform: initial !important;} .md-sidebar-toc::-webkit-scrollbar { height:8px !important; } #sidebar-toc-btn { bottom:0px !important; top:60px;} h1, h2, h3, h4, h5, h6 { border-bottom: solid 2px #333 !important; font-weight:bold; margin:2em 0em 0em 0em !important; } h1 + h2 { page-break-before:auto; margin-top : 0.5em !important; } h2 + h3 { page-break-before: auto; margin-top: 0.5em !important; } h3 + h4 { page-break-before: auto; margin-top: 0.5em !important; }  h3 + h4 { page-break-before: auto; margin-top: 0.5em !important; }  h4 + h5 { page-break-before: auto; margin-top: 0.5em !important; }  h5 + h6 { page-break-before: auto; margin-top: 0.5em !important; } h1,h2,h3{ font-size:24px !important;} h4,h5,h6 { font-size:22px !important; } .column-left{ float: left; width: calc(50% - 10px); text-align: left;} .column-right{ float: right; width: calc(50% - 10px);text-align: left;}  .three-column{ float: left; width: calc(33% - 15px); text-align: left; margin-left: 10px;} .clearfix::after{ content: ""; clear: both; display: block; } pre, code, var, samp, kbd, .mono { font-family: 'ＭＳ ゴシック', Consolas, 'Courier New', Courier, Monaco, monospace !important; line-height: 1.2 !important;}
</style>
