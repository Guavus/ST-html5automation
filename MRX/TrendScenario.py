from Utils.SetUp import *
from classes.Pages.TrendingMonitoringPageClass import *
from classes.Components.WorkflowStartComponent import *
from MRXUtils import SegmentHelper
from MRXUtils import TMHelper
from MRXUtils.TMHelper import *
from Utils.AvailableMethod import *
import json
try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    tm_Click_Flag=wfstart.launchScreen("Trend",getHandle(setup,MRXConstants.WFSTARTSCREEN))
    sleep(MRXConstants.SleepForTNMScreen)
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)
    TMScreenInstance.quicktrends.clickOnExpandButton(getHandle(setup, MRXConstants.TMSCREEN, 'trend-slider'),setup=setup)

    qs0 = ConfigManager().getNodeElements("wizardquicklinks1", "wizardquicklink")
    qs1 = ConfigManager().getNodeElements("wizardquicklinks1", "customquicklink")
    qs = merge_dictionaries(qs0, qs1)

    if MRXConstants.RANDOM_SELECTION_FOR_HOVER_ON_TNM:
        quickLinkListForHover = random.sample(set(MRXConstants.quickLinkListForTNM), 2) if len(MRXConstants.quickLinkListForTNM) > 1 else random.sample(set(MRXConstants.quickLinkListForTNM), 1)
        measureListForHover = random.sample(set(MRXConstants.measureListForTNM), 2) if len(MRXConstants.measureListForTNM) > 1 else random.sample(set(MRXConstants.measureListForTNM), 1)
        dimensionListForHover = random.sample(set(MRXConstants.dimensionListForTNM), 2) if len(MRXConstants.dimensionListForTNM) > 1 else random.sample(set(MRXConstants.dimensionListForTNM), 1)
    else:
        quickLinkListForHover = MRXConstants.quickLinkListForHover
        measureListForHover = MRXConstants.measureListForHover
        dimensionListForHover = MRXConstants.dimensionListForHover

    TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
    for quicklink in MRXConstants.quickLinkListForTNM:
        quickLinkLableFlag=True
        for measure in MRXConstants.measureListForTNM:
            for brokenDown in MRXConstants.dimensionListForTNM:
                timeRangeFromScreen, measureBeforeApplyFilter, breakDownBeforeApplyFilter = TMHelper.setQuickLink_Measure_BreakDown(setup, TMScreenInstance, quicklink,measure,brokenDown,quickLinkLableFlag)
                quickLinkLableFlag=False
                time.sleep(MRXConstants.SleepForTNMScreen)

                TMScreenInstance.table.scrollUpTable(setup)
                tableHandle = getHandle(setup, MRXConstants.TMSCREEN, "table")
                tableData = TMScreenInstance.table.getTableDataMap(tableHandle,driver=setup)

                queryFromUI = {}

                if tableHandle['table']['ROWS'] == []:
                    h = getHandle(setup, MRXConstants.UDSCREEN, "table")['table']['no_data_msg']
                    if len(h) > 0:
                        msg = str(h[0].text)
                        checkEqualAssert(MRXConstants.NODATAMSG, msg,measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='MKR-3094')
                    else:
                        checkEqualAssert(MRXConstants.NODATAMSG, '',measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='MKR-3094')

                    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
                    setup.d.save_screenshot(r)
                    logger.debug("No Table Data for measure = %s dimension =%s quicklink= %s :: Screenshot with name = %s is saved",measure,brokenDown,quicklink,r)
                    resultlogger.info("No Table Data for measure = %s dimension =%s quicklink= %s :: Screenshot with name = %s is saved",measure,brokenDown,quicklink,r)

                elif quicklink in quickLinkListForHover and measure in measureListForHover and brokenDown in dimensionListForHover:
                    TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.LineChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
                    selectedCompareChartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex_MRX(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare"))
                    main_chart_dict, compare_chart_dict ,legendOnChart_dict = TMScreenInstance.quicktrends.hoverOverTicksGetMainAndCompareChartText_MRX(setup, getHandle(setup, MRXConstants.TMSCREEN, "trend-main"), MRXConstants.TMSCREEN,active_compare_chart=selectedCompareChartIndex)
                    checkEqualAssert(main_chart_dict,compare_chart_dict,quicklink,measureBeforeApplyFilter,message="Verify main and compare chart value after hover",testcase_id="MKR-3768")
                    synchFlag=verifySynchBetweenTablaAndChart(tableData,legendOnChart_dict,main_chart_dict,TMScreenInstance,measureBeforeApplyFilter)
                    checkEqualAssert(True,synchFlag,message="Verify line chart data with table data",testcase_id="MKR-3782")

                    TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.BarChartIndex,getHandle(setup, MRXConstants.TMSCREEN,"trend-main"), parent="trend-main")
                    main_bar_chart_dict, compare_bar_chart_dict ,legendOnBar_dict = TMScreenInstance.quicktrends.hoverOverTicksGetMainAndCompareChartText_MRX(setup, getHandle(setup, MRXConstants.TMSCREEN, "trend-main"), MRXConstants.TMSCREEN,active_compare_chart=selectedCompareChartIndex)
                    checkEqualAssert(main_bar_chart_dict,compare_bar_chart_dict,quicklink,measureBeforeApplyFilter,message="Verify main and compare chart value after hover",testcase_id="MKR-3768")
                    synchFlag=verifySynchBetweenTablaAndChart(tableData, legendOnBar_dict,main_bar_chart_dict,TMScreenInstance,measureBeforeApplyFilter,chart='Bar')
                    checkEqualAssert(True,synchFlag,message="Verify bar chart data with table data",testcase_id="MKR-3782")
                    checkEqualDict(main_chart_dict,main_bar_chart_dict,message="Verify synch between line and bar chart",testcase_id="MKR-3782")

                    TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")

                    totalOnTableFlag = verifyTotalOnTable(TMScreenInstance, tableData, measureBeforeApplyFilter)
                    checkEqualAssert(True, totalOnTableFlag, quicklink, measureBeforeApplyFilter,message="Verify value for selected measure in table")

                queryFromUI = measureAndDimensionAfterMapping(timeRangeFromScreen, measureBeforeApplyFilter,breakDownBeforeApplyFilter,{},tableData)
                testcase=getTestCase(measureBeforeApplyFilter,breakDownBeforeApplyFilter)
                fireBV(queryFromUI, AvailableMethod.Top_Row, qs[str(quicklink).replace(' ', '').lower()]['table'],testcase=testcase)

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()

