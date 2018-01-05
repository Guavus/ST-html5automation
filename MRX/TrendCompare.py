from Utils.SetUp import *
from MRXUtils.MRXConstants import *
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
    sleep(MRXConstants.SleepForTNMScreen)
    checkEqualAssert(True,tm_Click_Flag,message="Verify that user can open the T&M screen from the worflows tab",testcase_id="MKR-3757")
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)

    TMScreenInstance.quicktrends.clickOnExpandButton(getHandle(setup, MRXConstants.TMSCREEN, 'trend-slider'),setup=setup)

    measures = setup.cM.getNodeElements("compare_mes", "measure")
    dimensions = setup.cM.getNodeElements("brokendown_dim", "dimension")
    mes = []

    for k, measure in measures.iteritems():
        mes.append(measure['locatorText'])

    dim = []
    for k, dimension in dimensions.iteritems():
        dim.append(dimension['locatorText'])

    selectedQuicklink = TMScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))

    numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
    numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"), parent="trend-compare")
    checkEqualAssert(7, numberofmainchart + numberofcomparechart, selectedQuicklink,message="Verify total number of Chart")

    viewForCompareChart=[]
    selectNone=True
    for i in range(6):
        TMScreenInstance.dropdown.customClick(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare")["trend-compare"]["trendchart"][i])
        selectedMeasure = TMScreenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(getHandle(setup, MRXConstants.TMSCREEN,"trend-header"), random.randint(0,len(mes)-1), index=0, parent="trend-header")
        isError(setup)
        sleep(MRXConstants.SleepForTNMScreen)
        if selectNone:
            selectedDimension = TMScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"), "__", index=1,parent="trend-header")
            selectNone=False
        else:
            selectedDimension = TMScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN,"trend-header"), random.choice(dim),index=1, parent="trend-header")
        isError(setup)
        sleep(MRXConstants.SleepForTNMScreen)
        availablView=[MRXConstants.BarChartIndex,MRXConstants.LineChartIndex]

        TMScreenInstance.switcher.measureChangeSwitcher(random.choice(availablView), getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
        selectedView = TMScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent='trend-main')
        viewForCompareChart.append(int(selectedView[0]))

    comparechartIndexForDimension = -1

    for i in range(6):
        TMScreenInstance.dropdown.customClick(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare")["trend-compare"]["trendchart"][i])
        isError(setup)
        comparechartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex_MRX(getHandle(setup, MRXConstants.TMSCREEN,"trend-compare"))
        checkEqualAssert(i,comparechartIndex,selectedQuicklink,"","Verify click on compare Chart with index = "+str(i))

        view = TMScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"), parent="trend-main")
        checkEqualAssert(int(view[0]),viewForCompareChart[i], str(selectedQuicklink),message="Verify view after click on compare chart")

        numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
        numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MRXConstants.TMSCREEN,"trend-compare"),parent="trend-compare")
        checkEqualAssert(7, numberofmainchart + numberofcomparechart, selectedQuicklink,message="Verify total number of Chart after click on compare chart")

        if int(view[0])==MRXConstants.LineChartIndex:
            p1 = TMScreenInstance.quicktrends.getPaths_MRX(getHandle(setup, MRXConstants.TMSCREEN,"trend-main"))
            compareTrend1 = TMScreenInstance.quicktrends.getPaths_MRX(getHandle(setup, MRXConstants.TMSCREEN,"trend-compare"),parent="trend-compare",indexOfComp=i)
            checkEqualAssert(compareTrend1,p1,selectedQuicklink,message="Verify equal activated dimension on main chart and compare chart")
        elif int(view[0])==MRXConstants.BarChartIndex:
            p1 = TMScreenInstance.quicktrends.getColorFromBar_DCT(getHandle(setup, MRXConstants.TMSCREEN, "trend-main"))
            compareTrend1 = TMScreenInstance.quicktrends.getColorFromBar_DCT(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"), parent="trend-compare", indexOfComp=i)
            checkEqualAssert(compareTrend1, p1, selectedQuicklink,message="Verify equal activated dimension on main chart and compare chart")


        main_chart_value = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"))
        compare_chart_value = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MRXConstants.TMSCREEN, "trend-compare"), parent="trend-compare", index=comparechartIndex)
        checkEqualAssert(compare_chart_value,main_chart_value,selectedQuicklink,message="Verify Main Chart Value with Compare Chart Value")

        measurefrommain = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN,"trend-header"), index=0, parent="trend-header")
        measurefromcompare = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN,"trend-compare"), index=i, parent="trend-compare")
        checkEqualAssert(str(measurefrommain), str(measurefromcompare), str(selectedQuicklink),message="Verify measure on Main and Compare Chart")

        dimensionfrommain = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN,"trend-header"), index=1, parent="trend-header")
        if str(dimensionfrommain).strip() != '__':
            comparechartIndexForDimension = comparechartIndexForDimension + 1
            dimensionfromcompare = TMScreenInstance.quicktrends.getDimensionFromCompareChart(getHandle(setup, MRXConstants.TMSCREEN,"trend-compare"),index=comparechartIndexForDimension)
            checkEqualAssert(str(dimensionfrommain), str(dimensionfromcompare), str(selectedQuicklink), "", "Verify dimension on Main and Compare Chart")

        measureFromCompare = TMScreenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(getHandle(setup, MRXConstants.TMSCREEN,"trend-compare"), random.randint(0, len(mes) - 1), index=i,parent="trend-compare")
        measureFrommain = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"), index=0, parent="trend-header")
        checkEqualAssert(measureFromCompare,measureFrommain,selectedQuicklink,message="Verfiy measure on main chart after change from compare chart")

        TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex, getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()