from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from MRXUtils.MRXConstants import *
from Utils.utility import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.TrendingMonitoringPageClass import *
import sys
import random

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    wfstart.launchScreen("Trend",getHandle(setup,MRXConstants.WFSTARTSCREEN))
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)
    selectedMeasure = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"), parent="trend-header")
    TMScreenInstance.quicktrends.clickOnExpandButton(getHandle(setup, MRXConstants.TMSCREEN, 'trend-slider'),setup=setup)

    ############################### Multiple Selection on Table ########################################################

    TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex, getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
    sleep(MRXConstants.SleepForTNMScreen)
    data = TMScreenInstance.table.getTableData1(getHandle(setup, MRXConstants.TMSCREEN, "table"))
    numberofRows = len(data['rows'])
    if data['rows']!=Constants.NODATA and len(data['rows'])>1:
        startIndex=random.randint(1, numberofRows-1)
        endIndex=random.randint(startIndex+1,numberofRows)
        Indices = [startIndex,endIndex]

        TMScreenInstance.table.setSpecialSelection(setup.d,Indices,Keys.SHIFT,getHandle(setup, MRXConstants.TMSCREEN, 'table'))
        selectedData = TMScreenInstance.table.getSelectedRowWithScroll(setup,MRXConstants.TMSCREEN)
        selectedValueList=[]
        colIndex = TMScreenInstance.table.getIndexForValueInArray(selectedData['header'],selectedMeasure)
        if colIndex!=-1:
            for rows in selectedData['rows']:
                selectedValueList.append(UnitSystem().getRawValueFromUI(rows[colIndex]))
        valueFromTable=sum(selectedValueList)

        TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.LineChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
        main_chart_text_on_line_view = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"))
        main_chart_value_on_line_view=UnitSystem().getRawValueFromUI(main_chart_text_on_line_view)
        selectedIndicesFromLineChart=TMScreenInstance.quicktrends.getSelectionFromChart(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))

        checkEqualValueAssert(valueFromTable,main_chart_value_on_line_view,message="Verify value on line chart after doing multiple selection on table",testcase_id="MKR-3765")
        checkEqualAssert(startIndex-1,selectedIndicesFromLineChart[0],message="Verify selection on line chart after doing multiple selection on table :: StartIndex",testcase_id="MKR-3765")
        checkEqualAssert(endIndex-1,selectedIndicesFromLineChart[len(selectedIndicesFromLineChart)-1],message="Verify selection on line chart after doing multiple selection on table :: EndIndex",testcase_id="MKR-3765")

        TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.BarChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
        main_chart_text_on_bar_view = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"))
        main_chart_value_on_bar_view = UnitSystem().getRawValueFromUI(main_chart_text_on_bar_view)
        selectedIndicesFromBarChart = TMScreenInstance.quicktrends.getSelectionFromChart(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))

        checkEqualValueAssert(valueFromTable,main_chart_value_on_bar_view,message="Verify value on bar chart after doing multiple selection on table",testcase_id="MKR-3765")
        checkEqualAssert(startIndex-1,selectedIndicesFromBarChart[0],message="Verify selection on bar chart after doing multiple selection on table :: StartIndex",testcase_id="MKR-3765")
        checkEqualAssert(endIndex-1,selectedIndicesFromBarChart[len(selectedIndicesFromBarChart)-1],message="Verify selection on bar chart after doing multiple selection on table :: EndIndex",testcase_id="MKR-3765")


        TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
        TMScreenInstance.table.setSpecialSelection(setup.d,[1,1],Keys.SHIFT, getHandle(setup, MRXConstants.TMSCREEN, 'table'))



    ############################### Multiple Selection on Line Chart ###################################################

    TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.LineChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
    sleep(MRXConstants.SleepForTNMScreen)
    baselinePathOnBarChart = TMScreenInstance.quicktrends.getBaseLinePath_MRX(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
    checkEqualAssert(MRXConstants.BaselinePath,baselinePathOnBarChart,message="Verify baseline at bar chart view",testcase_id="MKR-3769")

    totalbar,barHandle=TMScreenInstance.quicktrends.getAllBarForHover_DCT(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
    TMScreenInstance.quicktrends.doMultipleSelectionOnChart(setup, barHandle,[1,1], Keys.SHIFT)
    if totalbar>1:
        startIndex = random.randint(0, totalbar- 2)
        endIndex = random.randint(startIndex+1, totalbar-1)
        Indices = [startIndex, endIndex]

        TMScreenInstance.quicktrends.doMultipleSelectionOnChart(setup,barHandle,Indices,Keys.SHIFT)
        main_chart_text_on_line_view = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"))
        main_chart_value_on_line_view = UnitSystem().getRawValueFromUI(main_chart_text_on_line_view)
        comparechartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex_MRX(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"))
        compare_chart_text = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"), parent="trend-compare", index=comparechartIndex)
        compare_chart_value_on_line_view = UnitSystem().getRawValueFromUI(compare_chart_text)
        checkEqualValueAssert(main_chart_value_on_line_view, compare_chart_value_on_line_view,message="Verify value on compare chart with main chart after multiple selection on line chart",testcase_id="MKR-3770")



        TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.BarChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
        main_chart_text_on_bar_view = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"))
        main_chart_value_on_bar_view = UnitSystem().getRawValueFromUI(main_chart_text_on_bar_view)
        selectedIndicesFromBarChart=TMScreenInstance.quicktrends.getSelectionFromChart(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))

        checkEqualValueAssert(main_chart_value_on_line_view, main_chart_value_on_bar_view,message="Verify value on bar chart after doing multiple selection on line chart",testcase_id="MKR-3765")
        checkEqualAssert(startIndex, selectedIndicesFromBarChart[0],message="Verify selection on bar chart after doing multiple selection on line chart :: StartIndex",testcase_id="MKR-3765")
        checkEqualAssert(endIndex, selectedIndicesFromBarChart[len(selectedIndicesFromBarChart) - 1],message="Verify selection on bar chart after doing multiple selection on line chart :: EndIndex",testcase_id="MKR-3765")


        TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
        selectedData = TMScreenInstance.table.getSelectedRowWithScroll(setup, MRXConstants.TMSCREEN)
        selectedValueList = []
        colIndex = TMScreenInstance.table.getIndexForValueInArray(selectedData['header'], selectedMeasure)
        if colIndex != -1:
            for rows in selectedData['rows']:
                selectedValueList.append(UnitSystem().getRawValueFromUI(rows[colIndex]))
        valueFromTable = sum(selectedValueList)
        checkEqualValueAssert(main_chart_value_on_line_view, valueFromTable,message="Verify value on table after doing multiple selection on line chart",testcase_id="MKR-3765")

        TMScreenInstance.table.setSpecialSelection(setup.d,[1,1],Keys.SHIFT, getHandle(setup, MRXConstants.TMSCREEN, 'table'))

    else:
        logger.info("Total available bar on chart are =%s ,hence not able to perform multiple selection on chart",str(totalbar))



    ############################### Multiple Selection on Bar Chart ###################################################

    TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.BarChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
    sleep(MRXConstants.SleepForTNMScreen)
    baselinePathOnLineChart = TMScreenInstance.quicktrends.getBaseLinePath_MRX(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
    checkEqualAssert(MRXConstants.BaselinePath,baselinePathOnLineChart,message="Verify baseline at line chart view",testcase_id="MKR-3769")

    totalbar,barHandle=TMScreenInstance.quicktrends.getAllBarForHover_DCT(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
    TMScreenInstance.quicktrends.doMultipleSelectionOnChart(setup, barHandle, [1, 1], Keys.SHIFT)
    if totalbar>1:
        startIndex = random.randint(0, totalbar- 2)
        endIndex = random.randint(startIndex+1, totalbar-1)
        Indices = [startIndex, endIndex]

        TMScreenInstance.quicktrends.doMultipleSelectionOnChart(setup,barHandle,Indices,Keys.SHIFT)
        main_chart_text_on_bar_view = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"))
        main_chart_value_on_bar_view = UnitSystem().getRawValueFromUI(main_chart_text_on_bar_view)
        comparechartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex_MRX(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"))
        compare_chart_text = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"), parent="trend-compare", index=comparechartIndex)
        compare_chart_value_on_bar_view = UnitSystem().getRawValueFromUI(compare_chart_text)
        checkEqualValueAssert(main_chart_value_on_bar_view, compare_chart_value_on_bar_view,message="Verify value on compare chart with main chart after multiple selection on bar chart",testcase_id="MKR-3770")


        TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.BarChartIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
        main_chart_text_on_line_view = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"))
        main_chart_value_on_line_view = UnitSystem().getRawValueFromUI(main_chart_text_on_line_view)
        selectedIndicesFromLineChart=TMScreenInstance.quicktrends.getSelectionFromChart(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))

        checkEqualValueAssert(main_chart_value_on_bar_view,main_chart_value_on_line_view,message="Verify value on line chart after doing multiple selection on bar chart",testcase_id="MKR-3765")
        checkEqualAssert(startIndex,selectedIndicesFromLineChart[0],message="Verify selection on line chart after doing multiple selection on bar chart :: StartIndex",testcase_id="MKR-3765")
        checkEqualAssert(endIndex,selectedIndicesFromLineChart[len(selectedIndicesFromLineChart)-1],message="Verify selection on line chart after doing multiple selection on bar chart :: EndIndex",testcase_id="MKR-3765")


        TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
        selectedData = TMScreenInstance.table.getSelectedRowWithScroll(setup, MRXConstants.TMSCREEN)
        selectedValueList = []
        colIndex = TMScreenInstance.table.getIndexForValueInArray(selectedData['header'], selectedMeasure)
        if colIndex != -1:
            for rows in selectedData['rows']:
                selectedValueList.append(UnitSystem().getRawValueFromUI(rows[colIndex]))
        valueFromTable = sum(selectedValueList)
        checkEqualValueAssert(main_chart_value_on_bar_view, valueFromTable,message="Verify selection on table after doing multiple selection on bar chart",testcase_id="MKR-3765")

    else:
        logger.info("Total available bar on chart are =%s ,hence not able to perform multiple selection on chart",str(totalbar))

    setup.d.close()


except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved<br>", r)
    setup.d.close()