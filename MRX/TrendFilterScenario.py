from Utils.SetUp import *
from classes.Pages.TrendingMonitoringPageClass import *
from classes.Components.WorkflowStartComponent import *
from MRXUtils import SegmentHelper
from MRXUtils import TMHelper
from MRXUtils.TMHelper import *
from Utils.AvailableMethod import *
import json

def measureAndDimensionAfterMapping(timeRangeFromScreen,measureFromScreen,breakDownFromScreen,screenTooltipData,tableMap):
    query={}
    count=0
    query['table_header'] = tableMap['header']
    query['data'] = []

    if tableMap['rows']!=Constants.NODATA:
        for row_value in tableMap['rows']:
            query['data'].append(row_value)
            count = count + 1

    query['count'] = count
    query['measure']=[]
    query['dimension']=[]

    measures = ConfigManager().getNodeElements("measure_Mapping", "measure")
    dimensions = ConfigManager().getNodeElements("brokendown_Dimension_Mapping", "dimension")

    for k, measure in measures.iteritems():
        if str(k)==str(measureFromScreen):
            query['measure'].append(measure['backEnd_ID'])


    for k, dimension in dimensions.iteritems():
        if str(k)==str(breakDownFromScreen):
            query['dimension'].append(dimension['backEnd_ID'])

    filters = ConfigManager().getNodeElements("filter_Mapping", "filter")
    for k, filter in filters.iteritems():
        if str(k) in screenTooltipData.keys() and screenTooltipData[k] !=[] and str(screenTooltipData[k][0]).lower() != 'ALL'.lower():
            query[filter['backEnd_ID']]=screenTooltipData[k]

    timeRange=timeRangeFromScreen.split(Constants.TimeRangeSpliter)

    if len(timeRange)==1:
        startTime=str(str(timeRange[0]).strip().split('(')[0]).strip()+" 00:00"
        query['starttime']=str(getepoch(startTime,tOffset=MRXConstants.TIMEZONEOFFSET))
        query['endtime'] =str(getepoch(startTime,tOffset=MRXConstants.TIMEZONEOFFSET)+86400)
    else:

        if len(str(timeRange[0]).strip().split(' '))==3:
            query['starttime'] =str(getepoch(str(timeRange[0]).strip()+" 00:00",tOffset=MRXConstants.TIMEZONEOFFSET))
        else:
            query['starttime'] = str(getepoch(str(timeRange[0]).strip(), tOffset=MRXConstants.TIMEZONEOFFSET))

        if len(str(str(timeRange[1]).strip().split('(')[0]).strip().split(' ')) == 3:
            query['endtime'] = str(getepoch(str(str(timeRange[1]).strip().split('(')[0]).strip() + " 00:00", tOffset=MRXConstants.TIMEZONEOFFSET)+86400)
        else:
            query['endtime'] =str(getepoch(str(str(timeRange[1]).strip().split('(')[0]).strip(),tOffset=MRXConstants.TIMEZONEOFFSET))

    return query

def fireBV(query,method,table_name,testcase=''):
    sleep(1)
    query['method']=method
    query['table_name']=table_name
    query['testcase']=testcase
    import time
    query['id']=str(time.time()).split('.')[0]

    logger.info("Going to dump info from UI for Backend Data validation ::" + str(query))
    with open("TNMDumpFile.txt",mode='a') as fs:
        fs.write(json.dumps(query))
        fs.write(" __DONE__" + "\n")

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

    TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
    synchFlagForFilter=True
    for quicklink in MRXConstants.quickLinkListForHover:
        quickLinkLableFlag=True
        for measure in MRXConstants.measureListForHover:
            for brokenDown in MRXConstants.dimensionListForHover:
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
                else:
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

                queryFromUI = measureAndDimensionAfterMapping(timeRangeFromScreen, measureBeforeApplyFilter,breakDownBeforeApplyFilter, {},tableData)
                testcase=getTestCase(measureBeforeApplyFilter,breakDownBeforeApplyFilter)
                fireBV(queryFromUI, AvailableMethod.Top_Row, qs[str(quicklink).replace(' ', '').lower()]['table'],testcase=testcase)

                for i in range(0,MRXConstants.NUMBEROFFILTERSCENARIOFORTM):
                    try:
                        UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
                        SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
                        filterTestCase = setup.cM.getNodeElements("tmScreenFilters", "testcase")

                        expected={}
                        expected = UDHelper.setUDPFilters(TMScreenInstance, setup, str(i),screen=MRXConstants.TMSCREEN)
                        isError(setup)
                        actualtoggleState = UDHelper.getToggleStateForFilters(TMScreenInstance, setup, str(i),screen=MRXConstants.TMSCREEN)
                        popUpTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDPPOPUP,setup)
                        for k in MRXConstants.ListOfFilterContainingTree:
                            if expected[k]!=[]:
                                checkEqualAssert(expected[k],popUpTooltipData[k],message='Verify Tree selection on UI ( it should be like level 1 > level 2 > level 3 and soon',testcase_id='MKR-3198')
                        checkEqualDict(expected,popUpTooltipData,message="Verify Filters Selections On UDP Popup (Functional)",testcase_id=filterTestCase[str(i)]['value'],doSortingBeforeCheck=True)

                        # apply global filters
                        TMScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

                        response=isError(setup)
                        if response[0]:
                            logger.error("Got error after apply filter =%s",str(popUpTooltipData))
                            resultlogger.error("Got error after apply filter =%s <br>",str(popUpTooltipData))
                            continue

                        screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.TMSCREEN, setup)
                        measureFromScreen = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"),parent="trend-header")
                        checkEqualAssert(measureBeforeApplyFilter,measureFromScreen,message="Verify selected measure after apply filter")
                        checkEqualDict(expected, screenTooltipData,quicklink,measureFromScreen,message="Verify Filters Selections:: After clicking on Apply button the selected filter gets applied (Functional)", doSortingBeforeCheck=True)
                        filterFromScreenForDV=UDHelper.mapToggleStateWithSelectedFilter(screenTooltipData,actualtoggleState)

                        queryFromUI = {}
                        TMScreenInstance.table.scrollUpTable(setup)
                        tableHandle = getHandle(setup, MRXConstants.TMSCREEN,"table")
                        tableData = TMScreenInstance.table.getTableDataMap(tableHandle,driver=setup)

                        if tableHandle['table']['ROWS'] ==[]:
                            h=getHandle(setup, MRXConstants.UDSCREEN, "table")['table']['no_data_msg']
                            if len(h)>0:
                                msg=str(h[0].text)
                                checkEqualAssert(MRXConstants.NODATAMSG,msg,measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='MKR-3094')
                            else:
                                checkEqualAssert(MRXConstants.NODATAMSG,'',measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='MKR-3094')
                            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
                            setup.d.save_screenshot(r)
                            logger.debug("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)
                            resultlogger.info("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)

                        else:
                            if synchFlagForFilter:
                                TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.LineChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
                                selectedCompareChartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex_MRX(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"))
                                main_chart_dict, compare_chart_dict, legendOnChart_dict = TMScreenInstance.quicktrends.hoverOverTicksGetMainAndCompareChartText_MRX(setup, getHandle(setup, MRXConstants.TMSCREEN, "trend-main"), MRXConstants.TMSCREEN,active_compare_chart=selectedCompareChartIndex)
                                checkEqualAssert(main_chart_dict, compare_chart_dict, quicklink,measureBeforeApplyFilter,message="Verify main and compare chart value after hover",testcase_id="MKR-3768")
                                synchFlag = verifySynchBetweenTablaAndChart(tableData, legendOnChart_dict, main_chart_dict, TMScreenInstance, measureBeforeApplyFilter)
                                checkEqualAssert(True, synchFlag, message="Verify line chart data with table data")


                                TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.BarChartIndex,getHandle(setup, MRXConstants.TMSCREEN,"trend-main"),parent="trend-main")
                                main_bar_chart_dict, compare_bar_chart_dict, legendOnBar_dict = TMScreenInstance.quicktrends.hoverOverTicksGetMainAndCompareChartText_MRX(setup, getHandle(setup, MRXConstants.TMSCREEN, "trend-main"), MRXConstants.TMSCREEN,active_compare_chart=selectedCompareChartIndex)
                                checkEqualAssert(main_bar_chart_dict, compare_bar_chart_dict, quicklink,measureBeforeApplyFilter, message="Verify main and compare chart value after hover",testcase_id="MKR-3768")
                                synchFlag = verifySynchBetweenTablaAndChart(tableData, legendOnBar_dict, main_bar_chart_dict, TMScreenInstance, measureBeforeApplyFilter, chart='Bar')
                                checkEqualAssert(True, synchFlag, message="Verify bar chart data with table data")
                                checkEqualDict(main_chart_dict, main_bar_chart_dict,message="Verify synch between line and bar chart")

                                TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex,getHandle(setup, MRXConstants.TMSCREEN,"trend-main"),parent="trend-main")


                            totalOnTableFlag = verifyTotalOnTable(TMScreenInstance, tableData,measureBeforeApplyFilter)
                            checkEqualAssert(True, totalOnTableFlag, quicklink, measureBeforeApplyFilter,message="Verify value for selected measure in table after apply filter ::"+str(screenTooltipData))

                        queryFromUI = measureAndDimensionAfterMapping(timeRangeFromScreen, measureBeforeApplyFilter, breakDownBeforeApplyFilter,filterFromScreenForDV,tableData)
                        testcase=getTestCase(measureBeforeApplyFilter,breakDownBeforeApplyFilter)
                        testcase=testcase+","+str(filterTestCase[str(i)]['value'])
                        fireBV(queryFromUI, AvailableMethod.Top_Row,qs[str(quicklink).replace(' ','').lower()]['table'],testcase)

                    except Exception as e:
                        isError(setup)
                        r = "issue_" + str(random.randint(0, 9999999)) + ".png"
                        setup.d.save_screenshot(r)
                        logger.error("Got Exception : %s", str(e))
                        logger.debug("Got Exception from Script Level try catch For filters = %s :: Screenshot with name = %s is saved ",str(screenTooltipData),r)
                        resultlogger.debug("Got Exception from Script Level try catch For filters = %s  :: Screenshot with name = %s is saved <br>",str(screenTooltipData),r)
                        continue
                synchFlagForFilter=False

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()

