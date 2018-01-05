from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from MRXUtils.TMHelper import *
from MRXUtils.MRXConstants import *
from Utils.utility import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.TrendingMonitoringPageClass import *

import sys

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    tm_Click_Flag=wfstart.launchScreen("Trend",getHandle(setup,MRXConstants.WFSTARTSCREEN))
    checkEqualAssert(True,tm_Click_Flag,message="Verify that user can open the T&M screen from the worflows tab",testcase_id="MKR-3757")
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)
    time.sleep(MRXConstants.SleepForTNMScreen)

    actualDefaultValue =[]
    switcherHandle=getHandle(setup, MRXConstants.TMSCREEN, "trend-main")
    defaultSelectedSwitcher=TMScreenInstance.switcher.getMeasureChangeSelectedSwitcher(switcherHandle,parent='trend-main')
    actualDefaultValue.append(defaultSelectedSwitcher)

    defaultSelectedQuicklink=TMScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))
    actualDefaultValue.append(str(defaultSelectedQuicklink).strip())

    defaultSelectedMeasure=TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN,"trend-header"),parent="trend-header")
    actualDefaultValue.append(str(defaultSelectedMeasure).strip())

    h = getHandle(setup, MRXConstants.TMSCREEN, 'trend-slider')
    actualDefaultValue.append(len(h['trend-slider']['expand-btn']))
    checkEqualAssert(MRXConstants.ExpectedDefaultValueOnTM,actualDefaultValue,message="Verify the default functionality of the T& M screen",testcase_id="MKR-3759")

    availableView={MRXConstants.BarChartIndex:'Bar Chart',MRXConstants.LineChartIndex:'Line Chart',MRXConstants.TableViewIndex:'Grid'}
    for view in availableView.keys():
        viewFlag=TMScreenInstance.switcher.measureChangeSwitcher(view,switcherHandle,parent="trend-main")
        checkEqualAssert(True,viewFlag,message="Verify the functionality of the switcher by click on "+availableView[view]+" Icon",testcase_id="MKR-3758")
        title=TMScreenInstance.switcher.getMeasureChangeSwitcherTitle(view,switcherHandle,parent="trend-main")
        checkEqualAssert(availableView[view],title,message="Verify the title after hover on " + availableView[view] + " Icon", testcase_id="MKR-3768")
        if viewFlag:
            availableMeasureOnSelectedView=TMScreenInstance.dropdown.availableDropDownOption(getHandle(setup, MRXConstants.TMSCREEN,"trend-header"),index=0, parent="trend-header")
            checkEqualAssert(MRXConstants.ExpectedMeasureForDE, availableMeasureOnSelectedView,message="Verify that all the measures should be there in the T&M screen For " +availableView[view] + " View", testcase_id="MKR-3760")
            availableDimensionOnSelectedView = TMScreenInstance.dropdown.availableDropDownOption(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"), index=1, parent="trend-header")
            checkEqualAssert(MRXConstants.ExpectedBrokenDownValue,availableDimensionOnSelectedView,message="Verify that all the dimensions should be there in the drop down menu For "+availableView[view]+" View",testcase_id="MKR-3761")

    TMScreenInstance.quicktrends.clickOnExpandButton(getHandle(setup, MRXConstants.TMSCREEN, 'trend-slider'),setup=setup)
    numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
    numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"), parent="trend-compare")
    checkEqualAssert(7, numberofmainchart + numberofcomparechart,message="Verify total number of Chart after click on expand button",testcase_id="MKR-3763")

    TMScreenInstance.quicktrends.clickOnExpandButton(getHandle(setup, MRXConstants.TMSCREEN, 'trend-slider'),child='collapse-btn',setup=setup)
    numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
    numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"), parent="trend-compare")
    checkEqualAssert(2, numberofmainchart + numberofcomparechart,message="Verify total number of Chart after click on cross button", testcase_id="MKR-3763")

    TMScreenInstance.quicktrends.clickOnExpandButton(getHandle(setup, MRXConstants.TMSCREEN, 'trend-slider'),setup=setup)
    #footerText = str(getHandle(setup, MRXConstants.TMSCREEN, 'footer')['footer']['label'][0].text).split(':')[1].strip()

    measures = setup.cM.getNodeElements("compare_mes", "measure")
    dimensions = setup.cM.getNodeElements("brokendown_dim", "dimension")
    mes = []

    for k, measure in measures.iteritems():
        mes.append(measure['locatorText'])

    dim = []
    for k, dimension in dimensions.iteritems():
        dim.append(dimension['locatorText'])

    qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")

    for e in quicklink:
        TMScreenInstance.timeBar.setQuickLink(qs[e]['locatorText'],getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))
        isError(setup)
        selectedQuicklink = TMScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))

        t = TimeRangeComponentClass().get_Label(e)
        t1 = TMScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))
        checkEqualAssert(t[1], t1, selectedQuicklink,message="verify quicklink label")

        #expectedTableLength=BaseComponentClass().getExpectedTableLengthForQuickLink(setup, footerText,t1,qs[e]['locatorText'])
        TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex, getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
        sleep(MRXConstants.SleepForTNMScreen)
        data = TMScreenInstance.table.getTableDataMap(getHandle(setup, MRXConstants.TMSCREEN, "table"), driver=setup)

        if data['rows']=='No Data':
            logger.debug('Data not available for quickink =%s',selectedQuicklink)
            continue

        # checkEqualAssert(expectedTableLength,len(data['rows']),selectedQuicklink,'','Verify total number of entry in Table')

        for m in range(len(mes)):
            selectedMeasure = TMScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN,"trend-header"),str(mes[m]), index=0, parent="trend-header")
            isError(setup)
            legendFlag = True
            for d in range(len(dim)):
                selectedDimension=TMScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN,"trend-header"),str(dim[d]), index=1, parent="trend-header")
                isError(setup)
                TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.LineChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
                sleep(MRXConstants.SleepForTNMScreen)
                numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
                numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MRXConstants.TMSCREEN,"trend-compare"), parent="trend-compare")
                checkEqualAssert(7, numberofmainchart + numberofcomparechart, selectedQuicklink, selectedMeasure, "Verify total number of Chart")

                l1 = TMScreenInstance.quicktrends.getLegends_tm(getHandle(setup, MRXConstants.TMSCREEN, "trend-legend"))
                checkEqualAssert(True, len(l1) <= MuralConstants.Maximum_Trend_Legend, selectedQuicklink,selectedMeasure, "Verify Maximum number of legand")

                if not (selectedMeasure in MRXConstants.Non_Aggregable_Measure):
                    main_chart_text = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"))
                    comparechartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex_MRX(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"))
                    compare_chart_text = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"),parent="trend-compare",index=comparechartIndex)
                    checkEqualAssert(str(compare_chart_text), str(main_chart_text), selectedQuicklink,selectedMeasure, "Verify Compare Chart value with Main Chart Value",testcase_id="MKR-3770")

                    active_legend_value_before_clicking=getTotalActiveLegendValue(l1)
                    main_chart_value=UnitSystem().getRawValueFromUI(main_chart_text)
                    compare_chart_value=UnitSystem().getRawValueFromUI(compare_chart_text)
                    checkEqualValueAssert(str(active_legend_value_before_clicking),str(main_chart_value),selectedQuicklink,selectedMeasure,"Verify value from legend with main chart value")
                    checkEqualValueAssert(str(active_legend_value_before_clicking),str(compare_chart_value),selectedQuicklink,selectedMeasure, "Verify value from legend with compare chart value")

                # TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
                # TMScreenInstance.table.scrollUpTable(setup)
                # tableData = TMScreenInstance.table.getTableDataMap(getHandle(setup, MRXConstants.TMSCREEN, "table"),driver=setup)
                # TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.LineChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
                #
                # if dim[d] in MRXConstants.dimensionListForHover and mes[m] in MRXConstants.measureListForHover and selectedQuicklink in MRXConstants.quickLinkListForHover:
                #     selectedCompareChartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex_MRX(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare"))
                #     main_chart_dict, compare_chart_dict ,legendOnChart_dict = TMScreenInstance.quicktrends.hoverOverTicksGetMainAndCompareChartText_MRX(setup, getHandle(setup, MRXConstants.TMSCREEN, "trend-main"), MRXConstants.TMSCREEN,active_compare_chart=selectedCompareChartIndex)
                #     checkEqualAssert(main_chart_dict,compare_chart_dict,selectedQuicklink,selectedMeasure,message="Verify main and compare chart value after hover",testcase_id="MKR-3768")
                #     synchFlag=verfiySynchBetweenTablaAndChart(tableData,legendOnChart_dict,main_chart_dict,TMScreenInstance,selectedMeasure)
                #     checkEqualValueAssert(True,synchFlag,message="Verify line chart data with table data")
                #
                #     TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.BarChartIndex,getHandle(setup, MRXConstants.TMSCREEN,"trend-main"), parent="trend-main")
                #     main_bar_chart_dict, compare_bar_chart_dict ,legendOnBar_dict = TMScreenInstance.quicktrends.hoverOverTicksGetMainAndCompareChartText_MRX(setup, getHandle(setup, MRXConstants.TMSCREEN, "trend-main"), MRXConstants.TMSCREEN,active_compare_chart=selectedCompareChartIndex)
                #     checkEqualAssert(main_bar_chart_dict,compare_bar_chart_dict,selectedQuicklink,selectedMeasure,message="Verify main and compare chart value after hover",testcase_id="MKR-3768")
                #     synchFlag=verfiySynchBetweenTablaAndChart(tableData, legendOnBar_dict,main_bar_chart_dict,TMScreenInstance,selectedMeasure,chart='Bar')
                #     checkEqualValueAssert(True,synchFlag,message="Verify bar chart data with table data")
                #     checkEqualDict(main_chart_dict,main_bar_chart_dict,message="Verify synch between line and bar chart")
                #     TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.LineChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")

                #active_legend_value_before_clicking=getTotalActiveLegendValue(l1)
                #main_chart_value=UnitSystem().getRawValueFromUI(main_chart_text)
                #compare_chart_value=UnitSystem().getRawValueFromUI(compare_chart_text)

                #checkEqualValueAssert(str(active_legend_value_before_clicking),str(main_chart_value),selectedQuicklink,selectedMeasure,"Verify value from active legend with main chart value")
                #checkEqualValueAssert(str(active_legend_value_before_clicking),str(compare_chart_value),selectedQuicklink,selectedMeasure, "Verify value from active legend with compare chart value")
                # checkEqualValueAssert(valueformtable, active_legend_value_before_clicking, selectedQuicklink, selectedMeasure,"Verify value from active legend with Table")

                chartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex_MRX(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"))
                measurefromcompare = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"), index=chartIndex, parent="trend-compare")
                checkEqualAssert(selectedMeasure, str(measurefromcompare), str(selectedQuicklink),message="Verify measure on Main and Compare Chart")
                dimensionfromcompare = TMScreenInstance.quicktrends.getDimensionFromCompareChart(getHandle(setup, MRXConstants.TMSCREEN,"trend-compare"),index=chartIndex)
                checkEqualAssert(selectedDimension,str(dimensionfromcompare),str(selectedQuicklink),message="Verify dimension on main and compare chart")
                numberOfPathOnMainChart = TMScreenInstance.quicktrends.getPaths_MRX(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
                checkEqualAssert(len(numberOfPathOnMainChart),len(l1),selectedQuicklink,selectedMeasure,message="Verfiy total number of lines with total legends")

                if legendFlag or len(l1)==0:
                    legendIteration=len(l1)
                else:
                    legendIteration=1

                if len(l1)==1:
                    c1 = TMScreenInstance.quicktrends.clickLegendByIndex_tm(0, getHandle(setup,MRXConstants.TMSCREEN,"trend-legend"))
                    p2 = TMScreenInstance.quicktrends.getPaths_MRX(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"))
                    checkEqualAssert(1,len(p2),selectedQuicklink,selectedMeasure,"When only 1 legend, Verify that legend can't be deactivate")
                else:
                    for i in range(legendIteration):
                        p1 = TMScreenInstance.quicktrends.getPaths_MRX(getHandle(setup, MRXConstants.TMSCREEN,"trend-main"))
                        c1 = TMScreenInstance.quicktrends.clickLegendByIndex_tm(i, getHandle(setup, MRXConstants.TMSCREEN,"trend-legend"))

                        #main_chart_text = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"))
                        #main_chart_value = UnitSystem().getRawValueFromUI(main_chart_text)

                        l2 = TMScreenInstance.quicktrends.getLegends_tm(getHandle(setup, MRXConstants.TMSCREEN, "trend-legend"))
                        #active_legend_value_after_clicking=getTotalActiveLegendValue(l2)
                        #checkEqualValueAssert(active_legend_value_after_clicking, main_chart_value, selectedQuicklink,selectedMeasure, "Verify value from active legend with main chart value")
                        checkEqualAssert(True, str(c1).upper() in p1, selectedQuicklink, selectedMeasure, "Checking disabled color in previous view. Color = " + c1)

                        p2 = TMScreenInstance.quicktrends.getPaths_MRX(getHandle(setup, MuralConstants.TMSCREEN,"trend-main"))
                        checkEqualAssert(False, p1 == p2, selectedQuicklink, selectedMeasure, "Line Chart should not show deactivated Dimension")
                        checkEqualAssert(False, str(c1).upper() in p2, selectedQuicklink, selectedMeasure, "Line Chart should not show deactivated Dimension Color = " + c1)
                        chartIndex=TMScreenInstance.quicktrends.getSelectedCompareChartIndex_MRX(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"))

                        compareTrend1 = TMScreenInstance.quicktrends.getPaths_MRX(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"),parent="trend-compare", indexOfComp=chartIndex)
                        checkEqualAssert(p2, compareTrend1, selectedQuicklink, selectedMeasure, "Verify equal activated dimension on main chart and compare chart")

                        TMScreenInstance.quicktrends.clickLegendByIndex_tm(i, getHandle(setup, MuralConstants.TMSCREEN,"trend-legend"))
                        legendFlag=False

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved<br>", r)
    setup.d.close()