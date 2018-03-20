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
    udr_query = UDHelper.UDRQuery(query)
    dump_query = {}
    dump_query['data'] = data
    dump_query['testcase'] = testcase
    dump_query['query'] = udr_query
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
    wfstart = WorkflowStartComponentClass()
    wfstart.launchScreen("Distribution", getHandle(setup, MRXConstants.WFSCREEN))
    time.sleep(5)

    i='performanceScenario'

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
    isError(setup)

    screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)
    #For focus out hover form screen
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "WORKFLOWS")


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
            checkEqualAssert(MRXConstants.NODATAMSG,msg,message='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='MKR-3094')
        else:
            checkEqualAssert(MRXConstants.NODATAMSG,'',message='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='MKR-3094')
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
    setup.d.close()

