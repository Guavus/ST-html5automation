from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper
from Utils.AvailableMethod import *
import json

def measureAndDimensionAfterMapping(timeRangeFromScreen,measureFromScreen,screenTooltipData):
    query={}
    query['measure']=[]
    measures = ConfigManager().getNodeElements("measure_Mapping", "measure")
    for k, measure in measures.iteritems():
        if str(k)==str(measureFromScreen):
            query['measure'].append(measure['backEnd_ID'])


    filters = ConfigManager().getNodeElements("filter_Mapping", "filter")
    for k, filter in filters.iteritems():
        if str(k) in screenTooltipData.keys() and screenTooltipData[k] !=[] and str(screenTooltipData[k][0]).lower() != 'ALL'.lower():
            if str(k) in MRXConstants.ListOfFilterContainingTree:
                dictForTree={}
                dictForTree['table_header']=str(filter['backEnd_ID']).split(',')
                dictForTree['data']=[]
                for value in screenTooltipData[k]:
                    dictForTree['data'].append(value.split('/'))
                query[filter['tree_Dimension']] = dictForTree
            else:
                query[filter['backEnd_ID']]=screenTooltipData[k]

    # timeRange=timeRangeFromScreen.split(Constants.TimeRangeSpliter)
    #
    # if len(timeRange)==1:
    #     startTime=str(str(timeRange[0]).strip().split('(')[0]).strip()+" 00:00"
    #     query['starttime']=str(getepoch(startTime,tOffset=MRXConstants.TIMEZONEOFFSET))
    #     query['endtime'] =str(getepoch(startTime,tOffset=MRXConstants.TIMEZONEOFFSET)+86400)
    # else:
    #
    #     if len(str(timeRange[0]).strip().split(' '))==3:
    #         query['starttime'] =str(getepoch(str(timeRange[0]).strip()+" 00:00",tOffset=MRXConstants.TIMEZONEOFFSET))
    #     else:
    #         query['starttime'] = str(getepoch(str(timeRange[0]).strip(), tOffset=MRXConstants.TIMEZONEOFFSET))
    #
    #     if len(str(str(timeRange[1]).strip().split('(')[0]).strip().split(' ')) == 3:
    #         query['endtime'] = str(getepoch(str(str(timeRange[1]).strip().split('(')[0]).strip() + " 00:00", tOffset=MRXConstants.TIMEZONEOFFSET)+86400)
    #     else:
    #         query['endtime'] =str(getepoch(str(str(timeRange[1]).strip().split('(')[0]).strip(),tOffset=MRXConstants.TIMEZONEOFFSET))

    startTimeEpoch, endTimeEpoch = dumpTimeForBackEndValidation(timeRangeFromScreen, MRXConstants.TIMEZONEOFFSET)
    query['starttime'] = str(startTimeEpoch)
    query['endtime'] = str(endTimeEpoch)

    query['dimension']=['subscriberid']
    return query


def fireBV(query,method,table_name,data,testcase=''):
    sleep(1)
    query['method']=method
    query['table_name']=table_name
    query['data']=data
    query['testcase']=testcase
    import time
    query['id']=str(time.time()).split('.')[0]

    udr_query =UDHelper.UDRQuery(query)
    dump_query={}
    dump_query['data'] = data
    dump_query['testcase'] = testcase
    dump_query['query']=udr_query
    dump_query['id'] = query['id']
    logger.info("Going to dump info from UI for Backend Data validation ::" + str(dump_query))
    with open("UDRDumpFile.txt",mode='a') as fs:
        fs.write(json.dumps(dump_query))
        fs.write(" __DONE__" + "\n")

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "WORKFLOWS")
    udScreenInstance.wfstart.launchScreen("Distribution", getHandle(setup, MRXConstants.WFSCREEN))
    time.sleep(5)

    actualAvailableQuickLinkList=UDHelper.availableQuickLink(setup,MRXConstants.UDSCREEN)
    checkEqualAssert(MRXConstants.ExpectedQuickLinkList,actualAvailableQuickLinkList,message='Verify that a user is able to select filter time range as "Last 30 days", "Last 7 Days", "Yesterday", "Last 24 Hours", "Last 4 Hours"," Today" or, from calendar',testcase_id='MKR-1762')

    actualAvailableMeasureList=UDHelper.availableMeasure(setup,MRXConstants.UDSCREEN,index=0)
    checkEqualAssert(MRXConstants.ExpectedMeasure,actualAvailableMeasureList,message='Verify that a user is able to select available Measure',testcase_id='MKR-1763')

    UDHelper.setQuickLink_Measure(setup, udScreenInstance, str('testCalender')) # Check Calender Scenario (Start Time > End Time)

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    udpHandle = getHandle(setup, MRXConstants.AvailableFilterList)
    availableFilter = []
    for dim in udpHandle['filterTab']['dimension']:
        availableFilter.append(str(dim.text))
    checkEqualAssert(MRXConstants.ExpectedFilterOption, availableFilter,message="Verify that on clicking Filter icon User Distribution Parameters window appears with all the possible fields on which filter can be applied",testcase_id='MKR-1759')

    ################################# Validating Select/Deselect Scenario ##############################################

    expected = {}
    UDHelper.setUDPFilters(udScreenInstance, setup,'selectDeselectScenario')
    expected = UDHelper.setUDPFilters(udScreenInstance, setup, 'selectDeselectScenario')
    isError(setup)
    udpFilterFromPopup = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDPPOPUP, setup)
    checkEqualAssert(MRXConstants.NO_FILTER_ON_POPUP, str(udpFilterFromPopup),message="Verify filter text after Deselect Selected filter value")
    udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))


    ################################# Validating Cancel Button Functionality ###########################################

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    expected = {}
    expected = UDHelper.setUDPFilters(udScreenInstance, setup, str(0))
    isError(setup)
    udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
    udpFilterFromScreen= UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER,udpFilterFromScreen, message="Verify that on pressing Cancel button the selections made on User Distribution Parameters, selected filters do not get applied and the page",testcase_id='MKR-1761')

    ################################# Validating Cross (X) Button Functionality ########################################

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    expected = {}
    expected = UDHelper.setUDPFilters(udScreenInstance, setup, str(0))
    isError(setup)
    udScreenInstance.clickIcon(getHandle(setup, MRXConstants.UDPPOPUP,'icons'),setup.d,child='closePopupIcon')
    udpFilterFromScreen = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER, udpFilterFromScreen,message="Verify that on pressing X button the selections made on User Distribution Parameters, selected filters do not get applied and the page",testcase_id='MKR-1761')

    ################################# Validating Input Field (Web Domain) Functionality ################################

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    expected = {}
    UDHelper.setUDPFilters(udScreenInstance, setup, str('web_domain1'))
    expected = UDHelper.setUDPFilters(udScreenInstance, setup, str('web_domain2'))
    isError(setup)
    udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
    udpFilterFromScreen= UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER,str(udpFilterFromScreen),message="Verify filter after removing web domain value")

    ################################# Validating Filter Text Without Filter ############################################

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    expected = {}
    expected = UDHelper.setUDPFilters(udScreenInstance, setup, str('web_domain2'))
    udpFilterFromPopup = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDPPOPUP, setup)
    checkEqualAssert(MRXConstants.NO_FILTER_ON_POPUP, str(udpFilterFromPopup),message="Verify filter text without filter on Popup")
    udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    ############################################# For Toggle State ########################################################

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
    expectedtoggleState = {}
    expectedtoggleState = UDHelper.setUDPFilters(udScreenInstance, setup, 'toggle_NotEqual',toggleStateFlag=True)
    isError(setup)
    click_Status=udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    if click_Status:
        SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'filterIcon')
        actualtoggleState = UDHelper.getToggleStateForFilters(udScreenInstance, setup, 'toggle_NotEqual',validateSearch=True)
        isError(setup)

        for k,v in actualtoggleState.iteritems():
            if str(v)!='':
                checkEqualAssert('Equal',str(v),message='Verify that toggle button state should be Equal for Select ALL case :: filter = '+str(k),testcase_id='')
        udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    # UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    # SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
    # expectedtoggleState = {}
    # expectedtoggleState = UDHelper.setUDPFilters(udScreenInstance, setup, 'toggle_Equal',toggleStateFlag=True)
    # isError(setup)
    # click_Status=udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
    #
    # if click_Status:
    #     SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'filterIcon')
    #     actualtoggleState = UDHelper.getToggleStateForFilters(udScreenInstance, setup, 'toggle_Equal')
    #     isError(setup)
    #     checkEqualDict(expectedtoggleState,actualtoggleState,message='Verify that toggle button should have that same state that you set while applying filters (Select All + Equal)',testcase_id='MKR-3095')
    #     udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    ################################# Validating Special Scenario  #####################################################

    # UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    # SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
    #
    # expected = {}
    # expected = UDHelper.setUDPFilters(udScreenInstance, setup, str("removeFilterScenario"))
    # udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
    # isError(setup)
    # UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    # SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
    # actualtoggleState = UDHelper.getToggleStateForFilters(udScreenInstance, setup,'removeFilterScenario')
    # for k, v in actualtoggleState.iteritems():
    #     if str(v) != '':
    #         checkEqualAssert('Equal', str(v),message='After removing filter from screen, it should be removed from popup also',testcase_id='')
    # udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
    ####################################################################################################################


    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()

    ###################################### Filter Scenario #############################################################

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "WORKFLOWS")
    wfstart = WorkflowStartComponentClass()
    wfstart.launchScreen("Distribution", getHandle(setup, MRXConstants.WFSCREEN))
    time.sleep(5)

    for i in range(0,MRXConstants.NUMBEROFFILTERSCENARIO):
        try:
            udScreenInstance.switcher.measureChangeSwitcher_UD(1, getHandle(setup, MRXConstants.UDSCREEN, "switcher"))
            measureBeforeApplyFilter = ''
            timeRangeFromScreen,measureBeforeApplyFilter = UDHelper.setQuickLink_Measure(setup, udScreenInstance, str(i))

            UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
            SegmentHelper.clickOnfilterIcon(setup,MRXConstants.UDSCREEN,'nofilterIcon')

            ### get table name form XML
            quicklink = setup.cM.getNodeElements("udpScreenFilters", 'quicklink')
            testcase = setup.cM.getNodeElements("udpScreenFilters", "testcase")

            expected={}
            expected = UDHelper.setUDPFilters(udScreenInstance, setup, str(i))
            isError(setup)
            actualtoggleState = UDHelper.getToggleStateForFilters(udScreenInstance, setup, str(i))
            popUpTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDPPOPUP,setup)
            for k in MRXConstants.ListOfFilterContainingTree:
                if expected[k]!=[]:
                    checkEqualAssert(expected[k],popUpTooltipData[k],message='Verify Tree selection on UI ( it should be like level 1 > level 2 > level 3 and soon',testcase_id='MKR-3198')
            checkEqualDict(expected,popUpTooltipData,message="Verify Filters Selections On UDP Popup (Functional)",testcase_id=testcase[str(i)]['value'],doSortingBeforeCheck=True)

            # apply global filters
            udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
            response=isError(setup)
            if response[0]:
                continue

            screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)
            measureFromScreen = udScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.UDSCREEN, "allselects"))
            checkEqualAssert(measureBeforeApplyFilter,measureFromScreen,message="Verify Filter Selection on Screen after apply filter")
            checkEqualDict(expected, screenTooltipData,message="Verify Filters Selections:: After clicking on Apply button the selected filter gets applied (Functional)", doSortingBeforeCheck=True,testcase_id='MKR-1760'+testcase[str(i)]['value'])

            filterFromScreenForDV=UDHelper.mapToggleStateWithSelectedFilter(screenTooltipData,actualtoggleState)

            queryFromUI = {}
            m_data = []
            d_data = []

            queryFromUI = measureAndDimensionAfterMapping(timeRangeFromScreen, measureBeforeApplyFilter, filterFromScreenForDV)

            tableHandle = getHandle(setup, MRXConstants.UDSCREEN, "table")

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
                udScreenInstance.table.setSpecialSelection(setup.d, [1, 20], Keys.SHIFT, tableHandle)
                data = udScreenInstance.table.getSelectedRowWithScroll(setup, MRXConstants.UDSCREEN)
                columnIndex = udScreenInstance.table.getIndexForValueInArray(data['header'],str(measureBeforeApplyFilter).strip())
                if columnIndex !=-1:
                    listOfValueForSelectedMeasure = []
                    for rows in data['rows']:
                        listOfValueForSelectedMeasure.append(rows[columnIndex].strip())

                    m_data.append(str(udScreenInstance.table.getValueFromTable(listOfValueForSelectedMeasure,'sum')))


                    actualSegmentDetail,textFromSummary=UDHelper.getSummaryDetailAndValidatePresenceOfValidationBox(setup,MRXConstants.UDSCREEN)
                    if len(actualSegmentDetail)==3:
                        d_data.append(str(actualSegmentDetail[1]))

            fireBV(queryFromUI, AvailableMethod.Aggr_Measure, quicklink[str(i)]['table'], m_data, testcase[str(i)]['value'])
            fireBV(queryFromUI, AvailableMethod.Distinct_Dimension, quicklink[str(i)]['table'], d_data,testcase[str(i)]['value'])

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

