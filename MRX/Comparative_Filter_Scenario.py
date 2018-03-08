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


    ##########################################  Verify export data functionality ######################################################################

    timeRangeFromScreen, dimBeforeApplyFilter, measureBeforeApplyFilter, breakDownBeforeApplyFilter = CBHelper.setQuickLink_Compare_Measure_BreakDown(
        setup, cbScreenInstance, str(0))
    time.sleep(MRXConstants.SleepForComparativeScreen)

    exportDropDownHandle = getHandle(setup, MRXConstants.COMPARATIVESCREEN,"dropdown_open")
    try:
        setup.d.execute_script("arguments[0].click()", exportDropDownHandle["dropdown_open"]["exportdata"][0])
        time.sleep(2)
        try:
            cbScreenInstance.cm.clickLink("Export data", getHandle(setup, "exportdata_popup"))
        except Exception as e:
            logger.info("Exception on Clicking Export data link:  " + str(e))
    except Exception as e:
        logger.info("Exception on Clicking export data dropdown:  " +str(e))

    time.sleep(MRXConstants.SleepForComparativeScreen)
    num_of_files_downoaded = len([name for name in os.listdir(Constants.firefoxdownloadpath) if not name.startswith('.') and os.path.isfile(os.path.join(Constants.firefoxdownloadpath, name))])
    checkEqualAssert(1, num_of_files_downoaded, message='Verify CSV gets successfully downloaded on clicking Export data',testcase_id='MKR-3557')


    ######################################  Verify filterstab and their dimensions are same as they are in UD screen ##################################################

    UDHelper.clearFilter(setup, MRXConstants.COMPARATIVESCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.COMPARATIVESCREEN, 'nofilterIcon')

    handle = getHandle(setup, MRXConstants.AvailableFilterList)
    availableFilter = []
    for dim in handle['filterTab']['dimension']:
        availableFilter.append(str(dim.text))
    checkEqualAssert(MRXConstants.ExpectedFilterOption, availableFilter,message="Verify that all the filters have the dimensions that is same to UDR screen",testcase_id='MKR-3538')
    cbScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))



    ######################################  Verify Calendar functionality / Quicklink Label /  Different combinations of CB filter and quicklink scenarios  ####################################################

    testcase_IdList = setup.cM.getNodeElements("cbScreenFilters", 'testcase').keys()
    for k in testcase_IdList:
    #for x in range(0, MRXConstants.NUMBEROFFILTERSCENARIOFORCB):
        #k = "testCalender"   tested for time range startTime="2017 March 08 12 00" endTime="2017 March 08 04 00"
        #k= "0"  ## ====> last 7 days  correct behaviour  tested for available time range 2016-01-01 00:00  to 2017-03-15 13:00, Segmentation filter
        #k = "1" ##====> Yesterday     correct behaviour  "   Device filter
        #k = "2" ##====> Today    correct behaviour  " Network filter
        #k ="3" ##====> Last Month  correct behaviour  "  Content filter
        #k = "4"  ###====> last 6 months   correct behaviour  " Usage filter
        #k= "multiFilters"  ###===> combo of all 5 filter categories
        #k="performanceScenario" ### ===> select 'All' and then deselct first element for dropdowns. Input fields  given. Trees not selected.

        try:
            timeRangeFromScreen, dimBeforeApplyFilter, measureBeforeApplyFilter, breakDownBeforeApplyFilter = CBHelper.setQuickLink_Compare_Measure_BreakDown(setup,cbScreenInstance,str(k))

            SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

            expected = {}
            expected = UDHelper.setUDPFilters(cbScreenInstance, setup, str(k),screen=MRXConstants.COMPARATIVESCREEN)
            isError(setup)
            actualtoggleState = UDHelper.getToggleStateForFilters(cbScreenInstance, setup, str(k),screen=MRXConstants.COMPARATIVESCREEN)
            popUpTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDPPOPUP, setup)

            checkEqualDict(expected, popUpTooltipData,message="Verify Filters Selections On CB Filter Popup ",testcase_id='', doSortingBeforeCheck=True)

            cbScreenInstance.clickButton("Apply",getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

            sleep(MRXConstants.SleepForComparativeScreen)
            screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)

            dimAfterApplyFilter = cbScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"),index=0)
            measureAfterApplyFilter = cbScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), index=1)
            breakDownAfterApplyFilter = cbScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), index=2)

            checkEqualAssert(dimBeforeApplyFilter, dimAfterApplyFilter,message="Verify Compare Dimension Value on Screen after applying filter" + "Before Filters: "+str(dimBeforeApplyFilter) + "  After Filters: "+str(dimAfterApplyFilter))
            checkEqualAssert(measureBeforeApplyFilter, measureAfterApplyFilter,message="Verify Compare Measure Value on Screen after applying filter" + "Before Filters: "+str(measureBeforeApplyFilter) + "  After Filters: "+str(measureAfterApplyFilter))
            checkEqualAssert(breakDownBeforeApplyFilter, breakDownAfterApplyFilter,message="Verify Compare BreakDown Value on Screen after applying filter" + "Before Filters: "+str(breakDownBeforeApplyFilter) + "  After Filters: "+str(breakDownAfterApplyFilter))

            checkEqualDict(expected, screenTooltipData,message="Verify Filters Selections on CB Screen after clicking on 'Apply' button",doSortingBeforeCheck=True, testcase_id='')


            tableHandle = getHandle(setup, MRXConstants.COMPARATIVESCREEN, "table")
            if tableHandle['table']['ROWS'] == []:
                msg1 = CBHelper.getNoDataMsg(setup, MRXConstants.COMPARATIVESCREEN, child='msgOnLegend')
                checkEqualAssert(MRXConstants.NODATAMSGCB, msg1,measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='')

                r = "issue_" + str(random.randint(0, 9999999)) + ".png"
                setup.d.save_screenshot(r)
                logger.debug("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)
                resultlogger.info("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)
                UDHelper.clearFilter(setup, MRXConstants.COMPARATIVESCREEN)
            else:
                tableData = cbScreenInstance.table.getTableData1WithColumnHavingColor(tableHandle)
                chartHandle = getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main')
                chartData = cbScreenInstance.trend.hoverOverTicksGetMainHorizontalBarChartText(setup, chartHandle,MRXConstants.COMPARATIVESCREEN)

                CBHelper.validateSortingInTable(cbScreenInstance, tableData, "", measureAfterApplyFilter)
                color_List=cbScreenInstance.trend.getAllColorOnHorizontalBar_DCT(setup,chartHandle)
                yAxisPointList = CBHelper.getAxisPoint(chartHandle, child='yaxis')
                barColorDict = CBHelper.map_YAxisWithColorList(yAxisPointList,color_List)
                flag=CBHelper.validateColorSequence(barColorDict,tableData)
                checkEqualAssert(True,flag,message="Verify the colour sequence of the table and bar post applying filters " +str(expected),testcase_id="MKR-3563")
                flag=CBHelper.validateColorOnTooltipWithBar(chartData,barColorDict)

                UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)

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




