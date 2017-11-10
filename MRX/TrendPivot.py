from Utils.SetUp import *
from classes.Pages.TrendingMonitoringPageClass import *
from classes.Components.WorkflowStartComponent import *
from MRXUtils import SegmentHelper
from MRXUtils.TMHelper import *
from classes.Pages.ExplorePageClass import *

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    tm_Click_Flag=wfstart.launchScreen("Trend",getHandle(setup,MRXConstants.WFSTARTSCREEN))
    sleep(MRXConstants.SleepForTNMScreen)
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)
    exploreScreenInstance = ExplorePageClass(setup.d)

    measures = setup.cM.getNodeElements("compare_mes", "measure")
    mes = []
    for k, measure in measures.iteritems():
        mes.append(measure['locatorText'])

    qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")

    pivotHeaderFlag=True
    for i in range(0,MRXConstants.NUMBEROFFILTERSCENARIOFORTM):
        try:
            TMScreenInstance.switcher.measureChangeSwitcher(MRXConstants.TableViewIndex,getHandle(setup, MRXConstants.TMSCREEN, "trend-main"),parent="trend-main")
            TMScreenInstance.timeBar.setQuickLink(qs[random.choice(quicklink)]['locatorText'],getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))
            selectedMeasure = TMScreenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"), random.randint(0, len(mes) - 1), index=0,parent="trend-header")
            isError(setup)
            selectedTimeRange = TMScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))

            UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
            SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

            expected={}
            expected = UDHelper.setUDPFilters(TMScreenInstance, setup, str(i),screen=MRXConstants.TMSCREEN)
            popUpTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDPPOPUP,setup)

            # apply global filters
            TMScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
            response=isError(setup)
            if response[0]:
                logger.error("Got error after apply filter =%s",str(popUpTooltipData))
                resultlogger.error("Got error after apply filter =%s <br>",str(popUpTooltipData))
                continue

            time.sleep(MRXConstants.SleepForTNMScreen)

            tableHandle = getHandle(setup, MRXConstants.TMSCREEN,"table")
            if tableHandle['table']['ROWS'] == []:
                msg1 = getNoDataMsg(setup, MRXConstants.TMSCREEN)
                checkEqualAssert(Constants.NODATA,msg1,measure='Verify that the meaningful message should be shown on the UI when no data is on screen.',testcase_id='')
                continue

            exploreScreenInstance.cm.activate(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"), parent='trend-header')
            exploreScreenInstance.cm.goto("Apply as filter and pivot",getHandle(setup, MRXConstants.TMSCREEN, "trend-header"),parent='trend-header')

            flag,pivotToScreenName=pivotToScreen(setup,MRXConstants.PIVOTPOPUP,TMScreenInstance,selectedTimeRange,selectedMeasure,random.choice([0,1]),checkHeader=pivotHeaderFlag)

            if flag and pivotToScreenName=="Cancel":
                screenName=TMScreenInstance.cm.getSelectedScreenNameFromBreadCrumb(getHandle(setup,MRXConstants.TMSCREEN,'breadcrumb'))
                checkEqualAssert(MRXConstants.TrendsScreen,screenName.strip(),message="Cancel button functionality on Pivot Popup")
            elif flag and pivotToScreenName == "Cross":
                screenName = TMScreenInstance.cm.getSelectedScreenNameFromBreadCrumb(getHandle(setup, MRXConstants.TMSCREEN, 'breadcrumb'))
                checkEqualAssert(MRXConstants.TrendsScreen,screenName.strip(),message="Cross (X) button functionality on Pivot Popup")

            else:
                if 'Distribution' in pivotToScreenName:
                    screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)
                    selectedMeasureOnPivotScreen=TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.UDSCREEN, "allselects"))
                    selectedTimeRangeOnPivotScreen = TMScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.UDSCREEN, "ktrs"))

                else:
                    screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.COMPARATIVESCREEN, setup)
                    selectedMeasureOnPivotScreen = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"),index=1)
                    selectedTimeRangeOnPivotScreen = TMScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))

                checkEqualDict(popUpTooltipData, screenTooltipData,message="Verify Filters on pivot Screen ="+str(pivotToScreenName),doSortingBeforeCheck=True)
                checkEqualAssert(selectedMeasure, selectedMeasureOnPivotScreen,message="Verify Measure on pivot Screen =" + str(pivotToScreenName))
                checkEqualAssert(selectedTimeRange, selectedMeasureOnPivotScreen,message="Verify Timerange on pivot Screen =" + str(pivotToScreenName))

                getHandle(setup, Constants.VALIDATE_HEADER,'leftHeader')['leftHeader']['project_Name'][0].click()
                exploreScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup, MRXConstants.BREADCRUMB_SCREEN))
                exploreScreenInstance.cm.gotoScreenViaWorkFlowDrop_MRX(setup, str(MRXConstants.TrendsScreen),getHandle(setup, MRXConstants.BREADCRUMB_SCREEN))
                time.sleep(MRXConstants.SleepForTNMScreen)
            pivotHeaderFlag = False

        except Exception as e:
            isError(setup)
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.error("Got Exception : %s", str(e))
            logger.debug("Got Exception from Script Level try catch For filters = %s :: Screenshot with name = %s is saved ",str(expected),r)
            resultlogger.debug("Got Exception from Script Level try catch For filters = %s  :: Screenshot with name = %s is saved <br>",str(expected),r)
            continue

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()

