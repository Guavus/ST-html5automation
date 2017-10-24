from Utils.SetUp import *
from classes.Pages.MRXScreens.ComparativeClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from classes.Components.WorkflowStartComponent import *
from MRXUtils import CBHelper
from MRXUtils import SegmentHelper
from MRXUtils import UDHelper

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    exploreScreenInstance.exploreList.launchModule(exploreHandle, "WORKFLOWS")
    cbScreenInstance =ComparativeClass(setup.d)

    cbScreenInstance.wfstart.launchScreen("Comparative", getHandle(setup, MRXConstants.WFSCREEN))

    ###################################### Available filter dimension ##################################################

    UDHelper.clearFilter(setup, MRXConstants.COMPARATIVESCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.COMPARATIVESCREEN, 'nofilterIcon')

    handle = getHandle(setup, MRXConstants.AvailableFilterList)
    availableFilter = []
    for dim in handle['filterTab']['dimension']:
        availableFilter.append(str(dim.text))
    checkEqualAssert(MRXConstants.ExpectedFilterOption, availableFilter,message="Verify that all the filters have the dimensions that is same to UDR screen",testcase_id='MKR-3538')
    cbScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    for i in range(0, MRXConstants.NUMBEROFFILTERSCENARIOFORCB):
        try:
            measureBeforeApplyFilter = ''
            timeRangeFromScreen, dimBeforeApplyFilter, measureBeforeApplyFilter, breakDownBeforeApplyFilter = CBHelper.setQuickLink_Compare_Measure_BreakDown(setup,cbScreenInstance,str(i))

            UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
            SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

            ### get table name form XML
            quicklink = setup.cM.getNodeElements("udpScreenFilters", 'quicklink')

            expected = {}
            expected = UDHelper.setUDPFilters(cbScreenInstance, setup, str(i),screen=MRXConstants.COMPARATIVESCREEN)
            isError(setup)
            actualtoggleState = UDHelper.getToggleStateForFilters(cbScreenInstance, setup, str(i),screen=MRXConstants.COMPARATIVESCREEN)

            popUpTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDPPOPUP, setup)
            # for k in MRXConstants.ListOfFilterContainingTree:
            #     if expected[k] != []:
            #         checkEqualAssert(expected[k], popUpTooltipData[k],message='Verify Tree selection on UI ( it should be like level 1 > level 2 > level 3 and soon',testcase_id='MKR-3198')

            checkEqualDict(expected, popUpTooltipData,message="Verify Filters Selections On UDP Popup (Functional)",testcase_id='', doSortingBeforeCheck=True)

            # apply global filters
            cbScreenInstance.clickButton("Apply",getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
            response = isError(setup)
            if response[0]:
                continue
            sleep(MRXConstants.SleepForComparativeScreen)
            screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)

            compareDimFromScreen = cbScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"),index=0)
            compareMesFromScreen = cbScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), index=1)
            breakDownFromScreen = cbScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), index=2)

            checkEqualAssert(dimBeforeApplyFilter, compareDimFromScreen,message="Verify Compare Value on Screen after apply filter")
            checkEqualAssert(measureBeforeApplyFilter, compareMesFromScreen,message="Verify Measure Value on Screen after apply filter")
            checkEqualAssert(breakDownBeforeApplyFilter, breakDownFromScreen,message="Verify Broke down Value on Screen after apply filter")

            checkEqualDict(expected, screenTooltipData,message="Verify Filters Selections:: After clicking on Apply button the selected filter gets applied (Functional)",doSortingBeforeCheck=True, testcase_id='')

            # filterFromScreenForDV = UDHelper.mapToggleStateWithSelectedFilter(screenTooltipData, actualtoggleState)

            queryFromUI = {}
            m_data = []
            d_data = []

            # queryFromUI = measureAndDimensionAfterMapping(timeRangeFromScreen, measureBeforeApplyFilter,filterFromScreenForDV)

            tableHandle = getHandle(setup, MRXConstants.COMPARATIVESCREEN, "table")

            if tableHandle['table']['ROWS'] == []:
                msg1 = CBHelper.getNoDataMsg(setup, MRXConstants.COMPARATIVESCREEN, child='msgOnLegend')
                checkEqualAssert(MRXConstants.NODATAMSG, msg1,measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='')

                r = "issue_" + str(random.randint(0, 9999999)) + ".png"
                setup.d.save_screenshot(r)
                logger.debug("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)
                resultlogger.info("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)

            else:
                tableData = cbScreenInstance.table.getTableData1WithColumnHavingColor(tableHandle)
                chartHandle = getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main')
                chartData = cbScreenInstance.trend.hoverOverTicksGetMainHorizontalBarChartText(setup, chartHandle,MRXConstants.COMPARATIVESCREEN)

                CBHelper.validateSortingInTable(cbScreenInstance, tableData, "", compareMesFromScreen)
                color_List=cbScreenInstance.trend.getAllColorOnHorizontalBar_DCT(setup,chartHandle)
                yAxisPointList = CBHelper.getAxisPoint(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main'), child='yaxis')
                barColorDict = CBHelper.map_YAxisWithColorList(yAxisPointList,color_List)
                flag=CBHelper.validateColorSequence(barColorDict,tableData)
                checkEqualAssert(True,flag,message="Verify the colour sequence of the table and bar",testcase_id="MKR-3563")
                flag=CBHelper.validateColorOnTooltipWithBar(chartData,barColorDict)

        except Exception as e:
            isError(setup)
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.error("Got Exception : %s", str(e))
            logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
            resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
            continue

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()

    # for cd in range(len(compareDimList)):
    #     selectedCompareDim = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(compareDimList[cd]), index=0, parent="allselects")
    #     for cm in range(len(compareMesList)):
    #         selectedCompareMes = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(compareMesList[cm]), index=1,parent="allselects")
    #         for bd in range(len(brokendownDimList)):
    #             selectedBrokenDown = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(brokendownDimList[bd]), index=2,parent="allselects")
    #             sleep(10)
    #             load_Flag = CBHelper.expandMoreOnCB(setup, MRXConstants.COMPARATIVESCREEN, child="load_more")
    #             tableData=cbScreenInstance.table.getTableData1WithColumnHavingColor(getHandle(setup, MRXConstants.COMPARATIVESCREEN,'table'))
    #             chartHandle = getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main')
    #             chartData = cbScreenInstance.trend.hoverOverTicksGetMainHorizontalBarChartText(setup, chartHandle,MRXConstants.COMPARATIVESCREEN)
    #
    #             if tableData['rows']!=Constants.NODATA and chartData!={}:
    #                 CBHelper.validateSortingInTable(cbScreenInstance,tableData,"",selectedCompareMes)
    #                 color_List=cbScreenInstance.trend.getAllColorOnHorizontalBar_DCT(setup,chartHandle)
    #                 yAxisPointList = CBHelper.getAxisPoint(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main'), child='yaxis')
    #                 barColorDict = CBHelper.map_YAxisWithColorList(yAxisPointList,color_List)
    #                 flag=CBHelper.validateColorSequence(barColorDict,tableData)
    #                 checkEqualAssert(True,flag,message="Verify the colour sequence of the table and bar",testcase_id="MKR-3563")
    #                 flag=CBHelper.validateColorOnTooltipWithBar(chartData,barColorDict)

    # setup.d.close()


