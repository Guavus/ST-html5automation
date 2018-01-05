from Utils.utility import *
from MRXConstants import *
from classes.Components.TimeRangeComponentClass import *
from selenium.webdriver import ActionChains
from MRXUtils import UDHelper
from dateutil.parser import parse
import json


def measureAndDimensionAfterMapping(timeRangeFromScreen, measureFromScreen, breakDownFromScreen, screenTooltipData,tableMap):
    query = {}
    count = 0
    query['table_header'] = tableMap['header']
    query['data'] = []

    if tableMap['rows'] != Constants.NODATA:
        for row_value in tableMap['rows']:
            query['data'].append(tableMap['rows'][row_value])
            count = count + 1

    query['count'] = count
    query['measure'] = []
    query['dimension'] = []

    measures = ConfigManager().getNodeElements("measure_Mapping", "measure")
    dimensions = ConfigManager().getNodeElements("brokendown_Dimension_Mapping", "dimension")

    for k, measure in measures.iteritems():
        if str(k) == str(measureFromScreen):
            query['measure'].append(measure['backEnd_ID'])

    for k, dimension in dimensions.iteritems():
        if str(k) == str(breakDownFromScreen):
            query['dimension'].append(dimension['backEnd_ID'])

    filters = ConfigManager().getNodeElements("filter_Mapping", "filter")
    for k, filter in filters.iteritems():
        if str(k) in screenTooltipData.keys() and screenTooltipData[k] != [] and str(
                screenTooltipData[k][0]).lower() != 'ALL'.lower():
            query[filter['backEnd_ID']] = screenTooltipData[k]

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

    return query


def fireBV(query, method, table_name, testcase=''):
    sleep(1)
    query['method'] = method
    query['table_name'] = table_name
    query['testcase'] = testcase
    import time
    query['id'] = str(time.time()).split('.')[0]

    logger.info("Going to dump info from UI for Backend Data validation ::" + str(query))
    with open("TNMDumpFile.txt", mode='a') as fs:
        fs.write(json.dumps(query))
        fs.write(" __DONE__" + "\n")

def button_Status(condition,request,screenInstance,setup,screen=MRXConstants.POPUPSCREEN,button_label="OK",testcase_id=''):
    logger.info("Method Called :button_Status ")
    button_status=screenInstance.cm.isButtonEnabled(button_label,getHandle(setup, screen,"allbuttons"))
    checkEqualAssert(condition,button_status,message="Checking State of "+button_label+ " button ::" +request,testcase_id=testcase_id)
    return button_status


def getNoDataMsg(setup,screen,parent='tm_no_data_msg',child='msgOnChart'):
    logger.info("Method Called : getNoDataMsg")
    h=getHandle(setup,screen,parent)
    if len(h[parent][child])>0:
        return str(h[parent][child][0].text)
    else:
        return "Text not found for No Data"

def getTotalActiveLegendValue(list, iscount='sum'):
    active_legend_value = []
    for i in range(len(list)):
        if list[i]['state'] == True:
            active_legend_value.append(UnitSystem().getRawValueFromUI(str(list[i]['value']).split('\n')[1].strip()))
    if iscount == 'sum':
        return (str(sum(active_legend_value)))
    elif iscount == 'avg':
        return str(sum(active_legend_value) / float(len(active_legend_value)))
    else:
        return " "


def verifySynchBetweenTablaAndChart(tableData, legends, chartData, screenInstance, selectedMeasure, chart='Line'):
    logger.info("Method Called :: verfiySynchBetweenTablaAndChart")
    try:
        for timestamp_key in legends:
            Year_From_Legends=datetime.datetime.fromtimestamp(long(timestamp_key)).strftime('%Y')
            KEYFLAG = False
            for key_table in tableData['rows']:
                Year_From_Tables = parse(str(key_table).strip()).strftime("%Y")

                if Year_From_Legends.strip()!=Year_From_Tables.strip() and Year_From_Tables.strip()==time.strftime("%Y"):
                    key_table_list=str(key_table).split(' ')
                    if len(key_table_list)==2:
                        key_table_list.append(Year_From_Legends.strip())
                    elif len(key_table_list)==3:
                        key_table_list.insert(2,Year_From_Legends.strip())

                    key_table_with_year=' '.join(key_table_list)
                else:
                    key_table_with_year = key_table

                if str(parse(str(key_table_with_year).strip()).strftime("%s")).strip() == str(timestamp_key).strip():
                    KEYFLAG = True
                    for key in legends[timestamp_key]:
                        colIndex=screenInstance.table.getIndexForValueInArray(tableData['header'],key)
                        if tableData['rows'][key_table][colIndex]!= legends[timestamp_key][key]:
                            logger.info("Mismatch Found between table and %s chart :: tableValue = %s chartValue =%s",chart,tableData['rows'][key_table][colIndex],chartData[timestamp_key][key])
                            return False
            if not KEYFLAG :
                logger.info("Row in table not found for timestamp = %s",str(getDateString(long(timestamp_key),5.5)))
                return False

    except Exception as e:
        logger.info("Exception Found :: %s",str(e))
        return False

    return True

def verifyTotalOnTable(screenInstance,tableData,selectedMeasure):
    logger.info("Method Called :: verifyTotalOnTable")
    try:
        if not (selectedMeasure in MRXConstants.Non_Aggregable_Measure):
            colIndex=screenInstance.table.getIndexForValueInArray(tableData['header'],selectedMeasure)
            for key in tableData['rows']:
                rowValue = []
                for value in tableData['rows'][key][1:len(tableData['rows'][key])-1]:
                    rowValue.append(UnitSystem().getRawValueFromUI(str(value).strip()))

                totalValue=sum(rowValue)
                expectedValue=UnitSystem().getRawValueFromUI(str(tableData['rows'][key][colIndex]).strip())
                if not (abs(expectedValue - totalValue)<= (Constants.PercentageAllowedinDiff*expectedValue)):
                    logger.info("Total on table not match :: check manually tableValue = %s",str(tableData['rows'][key]))
                    return False

    except Exception as e:
        logger.info("Exception Found :: %s",str(e))
        return False
    return True


def setCustomQuickLink_Measure_BreakDown(setup,tmScreenInstance,i='0'):
    quicklink = setup.cM.getNodeElements("tmScreenFilters", 'quicklink')
    TM_Measures = setup.cM.getNodeElements("tmScreenFilters", 'measure')[str(i)]['locatorText']
    TM_BrokenDown = setup.cM.getNodeElements("tmScreenFilters", 'breakDown')[str(i)]['locatorText']

    logger.info("Going to Select Measure=%s, By  =%s",str(TM_Measures),str(TM_BrokenDown))

    if quicklink[str(i)]['locatorText'] == 'CustomClick':
        selectedQuicklink=quicklink[str(i)]['locatorText']
        calHandler = getHandle(setup, MRXConstants.TMSCREEN, "ktrs")
        logger.info("Launching Calendar from UDP Popup")
        calHandler['ktrs']['datepicker'][0].click()
        logger.info("Calendar picker is clicked")

        ################################### For test Calender Scenario #################################################

        if i=='testCalender':
            [year, month, day, hour, min] = str(quicklink[str(i)]['startTime']).split(' ')
            setCalendar(year, month, day, hour, min, tmScreenInstance, setup, page=Constants.CALENDERPOPUP,parent="leftcalendar")

            [et_year, et_month, et_day, et_hour, et_min] = str(quicklink[str(i)]['endTime']).split(' ')
            setCalendar(et_year, et_month, et_day, et_hour, et_min, tmScreenInstance, setup, Constants.CALENDERPOPUP,"rightcalendar")

            valueFromCalender1 = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()

            stepoch,etepoch=parseTimeRange1(valueFromCalender1,timezone=MRXConstants.TIMEZONEOFFSET)
            try:
                if etepoch-stepoch <=0:
                    UDHelper.button_Status(False,"When Start Time > End Time ==> Selected Time Range ="+valueFromCalender1, tmScreenInstance, setup,Constants.CALENDERPOPUP, "Apply",testcase_id='')
                else:
                    checkEqualAssert(True,etepoch-stepoch>=0,"Not allow to choose StartTime > EndTime",testcase_id='MKR-3188')
            except:
                logger.info("Skipping TestCase =")

            monthListFormLeftCalender=getAvailableMonthList(setup,parent='leftcalendar')
            checkEqualAssert(MRXConstants.MONTHLIST,monthListFormLeftCalender,message='Verify that all the months should be there in the custom calendar (Left Calender)',testcase_id='')

            monthListFormRightCalender = getAvailableMonthList(setup, parent='rightcalendar')
            checkEqualAssert(MRXConstants.MONTHLIST, monthListFormRightCalender,message='Verify that all the months should be there in the custom calendar (Right Calender)',testcase_id='')

            tmScreenInstance.clickButton("Cancel", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))

            return
        ################################################################################################################


        [year, month, day, hour, min] = str(quicklink[str(i)]['startTime']).split(' ')
        setCalendar(year, month, day, hour, min, tmScreenInstance, setup, page=Constants.CALENDERPOPUP,parent="leftcalendar")

        [et_year, et_month, et_day, et_hour, et_min] = str(quicklink[str(i)]['endTime']).split(' ')
        setCalendar(et_year, et_month, et_day, et_hour, et_min, tmScreenInstance, setup,Constants.CALENDERPOPUP, "rightcalendar")

        valueFromCalender=str(getHandle(setup,Constants.CALENDERPOPUP,'allspans')['allspans']['span'][0].text).strip()
        # Closing Calendar Pop Up
        tmScreenInstance.clickButton("Apply",getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))
        logger.info("Calendar Selection done at Filter Popup = %s ", valueFromCalender)
        t1 = tmScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.UDSCREEN, "ktrs"))
        checkEqualAssert(valueFromCalender, t1, selectedQuicklink,message="Verify the functionality of the custom calendar",testcase_id="MKR-3774")

    else:
        tmScreenInstance.timeBar.setQuickLink(quicklink[str(i)]['locatorText'], getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))
        isError(setup)
        selectedQuicklink = tmScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))
        t = TimeRangeComponentClass().get_Label(str(quicklink[str(i)]['locatorText']).replace(' ','').lower())
        t1 = tmScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))
        checkEqualAssert(t[1], t1, selectedQuicklink,message="verify quicklink label")


    selectedMeasure = tmScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"), str(TM_Measures), index=0,parent="trend-header")
    selectedTM_BrokenDown = tmScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"), str(TM_BrokenDown), index=1,parent="trend-header")
    timeRangeFromPopup = str(t1)

    return timeRangeFromPopup,selectedMeasure,selectedTM_BrokenDown



def setQuickLink_Measure_BreakDown(setup,tmScreenInstance,quicklink,measure,brokenDown,quickLinkLableFlag=False):

    qs0 = ConfigManager().getNodeElements("wizardquicklinks1", "wizardquicklink")
    qs1 = ConfigManager().getNodeElements("wizardquicklinks1", "customquicklink")
    qs=merge_dictionaries(qs0,qs1)

    if 'custom' in str(quicklink).lower():
        calHandler = getHandle(setup, MRXConstants.TMSCREEN, "ktrs")
        logger.info("Launching Calendar from UDP Popup")
        calHandler['ktrs']['datepicker'][0].click()
        logger.info("Calendar picker is clicked")

        [year, month, day, hour, min] = str(qs[str(quicklink).replace(' ','').lower()]['startTime']).split(' ')
        setCalendar(year, month, day, hour, min, tmScreenInstance, setup, page=Constants.CALENDERPOPUP,parent="leftcalendar")

        [et_year, et_month, et_day, et_hour, et_min] = str(qs[str(quicklink).replace(' ','').lower()]['endTime']).split(' ')
        setCalendar(et_year, et_month, et_day, et_hour, et_min, tmScreenInstance, setup, Constants.CALENDERPOPUP,"rightcalendar")

        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()

        # Closing Calendar Pop Up
        tmScreenInstance.clickButton("Apply", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))
        logger.info("Calendar Selection done at Filter Popup = %s ", valueFromCalender)
        t1 = tmScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.UDSCREEN, "ktrs"))
        checkEqualAssert(valueFromCalender, t1,message="Verify the functionality of the custom calendar", testcase_id="MKR-3774")

    else:
        tmScreenInstance.timeBar.setQuickLink(quicklink, getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))
        isError(setup)
        selectedQuicklink = tmScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))
        t1 = tmScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.TMSCREEN, "ktrs"))
        if quickLinkLableFlag:
            t = TimeRangeComponentClass().get_Label(str(quicklink).replace(' ', '').lower())
            checkEqualAssert(t[1], t1, selectedQuicklink, message="verify quicklink label",testcase_id="MKR-3771")


    logger.info("Going to Select Measure=%s, and By  =%s",str(measure),str(brokenDown))
    selectedMeasure = tmScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"), str(measure).strip(), index=0,parent="trend-header")
    selectedTM_BrokenDown = tmScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.TMSCREEN, "trend-header"), str(brokenDown).strip(), index=1,parent="trend-header")
    timeRangeFromPopup = str(t1)

    return timeRangeFromPopup,selectedMeasure,selectedTM_BrokenDown

def getTestCase(selectedMeasure,seletedBrokenDown):
    measureTestCase= ConfigManager().getNodeElements("compare_mes_testCaseMapping", "measure")
    brokendownTestCase= ConfigManager().getNodeElements("brokendown_dim_testCaseMapping", "dimension")
    testcase=[]
    if selectedMeasure in measureTestCase.keys():
        testcase.append(str(measureTestCase[str(selectedMeasure)]['testcase']))

    if seletedBrokenDown in brokendownTestCase.keys():
        testcase.append(str(brokendownTestCase[str(seletedBrokenDown)]['testcase']))

    return ','.join(testcase)


def pivotToScreen(setup,screenName,screenInstance,selectedTimeRange,selectedMeasure,drillIndex=0,checkHeader=False,button="OK"):
    h=getHandle(setup,screenName)
    if checkHeader:
        checkEqualAssert(str(MRXConstants.PivotPopupHeader).strip(),str(h['allspans']['span'][0].text).strip(),message='Verify Pivot Popup Header')
        availableScreenOnPivotPopup=screenInstance.multiDropdown.getAllRadiosText(h,"label")
        checkEqualAssert(MRXConstants.AvailableOptionOnPivotPopup,availableScreenOnPivotPopup,message='Verify that user should be able to pivot to two landing screens :- Comparative Breakdown User Distribution',testcase_id="MKR-3780")
    timeRangeOnPopup=''
    measureOnPopup=''
    try:
        for i,span in enumerate(h['allspans']['span']):
            if 'Time' in str(span.text):
                timeRangeOnPopup=str(h['allspans']['span'][i+1].text).strip("|").strip()
            if 'Measure' in str(span.text):
                measureOnPopup = str(h['allspans']['span'][i+1].text).strip("|").strip()
    except:
        pass

    checkEqualAssert(selectedTimeRange,timeRangeOnPopup,message="Verify timerange on Pivot Popup")
    checkEqualAssert(selectedMeasure, measureOnPopup, message="Verify measure on Pivot Popup")


    if screenInstance.multiDropdown.getSelectedRadioButtonText(h)==False:
        button_Status(False,"Without selection on radio button",screenInstance,setup,screen=screenName,button_label='OK')
        button_Status(True,"Without selection on radio button",screenInstance,setup,screen=screenName,button_label='Cancel')

    logger.info('Pivot to : =%s', str(drillIndex))
    selectedScreenOnPivotPopup=screenInstance.multiDropdown.selectRadioButtonByIndex(drillIndex,h,"label")
    okButtonStatusAfterSelection=button_Status(True,"With selection on radio button",screenInstance,setup,screen=screenName,button_label='OK')


    logger.info('Going to Click on %s Button ', str(button))
    if button == 'OK' and okButtonStatusAfterSelection :
        screenInstance.cm.clickButton(str(button),h)
        return True,selectedScreenOnPivotPopup

    elif button == 'Cancel':
        screenInstance.cm.clickButton(str(button),h)
        return True,'Cancel'

    elif button=="Cross":
        try:
            h['icons']['closePopupIcon'][0].click()
        except:
            try:
                h['icons']['closePopupIcon'][0].click()
            except:
                pass

        return True,'Cross'

    else:
        try:
            h['icons']['closePopupIcon'][0].click()
        except:
            try:
                h['icons']['closePopupIcon'][0].click()
            except:
                pass

        return False,''