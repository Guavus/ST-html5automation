from Utils.utility import *
from MRXConstants import *
from classes.Components.TimeRangeComponentClass import *
from selenium.webdriver import ActionChains
from MRXUtils import UDHelper
import json

def getNoDataMsg(setup,screen,parent='cb_no_data_msg',child='msgOnChart'):
    logger.info("Method Called : getNoDataMsg")
    h=getHandle(setup,screen,parent)
    if len(h[parent][child])>0:
        return str(h[parent][child][0].text)
    else:
        return "Text not found for No Data"


def getHeader(setup,screen,parent='cb_chart_header',child='text'):
    logger.info("Method Called : getHeader")
    h=getHandle(setup,screen,parent)
    if len(h[parent][child])>0:
        return str(h[parent][child][0].text)
    else:
        return "Header Text Not Found"



def getAxisPoint(h,parent='trend-main',child='xaxis'):
    logger.info("Method Called : getAxisPoint")
    point=[]
    if len(h[parent][child])>0:
        for ele in h[parent][child][0].find_elements_by_class_name('tick'):
            point.append(str(ele.text).strip())
    return point

def map_YAxisWithColorList(yAxisPointList,color_List):
    logger.info("Method Called : map_YAxisWithColorList")
    barColorDict={}
    if len(yAxisPointList) == len(color_List):
        for index in range(len(yAxisPointList)):
            barColorDict[yAxisPointList[index]] = color_List[index]

        logger.info("Bar Color List With Y axis Point =%s", str(barColorDict))
    else:
        logger.error("Mismatch in Color List and Y axis point : check manually")

    return barColorDict


def validateSortingInTable(cbScreenInstance,data,selectedQuicklink, selectedMeasure):
    index = cbScreenInstance.table.getIndexForValueInArray(data['header'], selectedMeasure)

    # for i in range(data['rows']):
    #     if 'Others' in data['rows'][i][1]:
    #         data['rows'] = data['rows'][:-1]
    tmp_List=[]
    for key in data['rows']:
        print key
        if 'Others' in key[1]:
            print True
            tmp_List = data['rows'][:-1]

    # if 'Others' in data['rows']:
    #     data['rows'] = data['rows'][:-1]
    selectedMeasure_value_list = [element[index] for element in tmp_List]

    unitFlagForSession = False
    if 'Session' in selectedMeasure:
        for i in range(len(selectedMeasure_value_list)):
            if len(re.findall(r'[a-zA-Z]+', selectedMeasure_value_list[i])) != 0 and selectedMeasure_value_list[i]!="NA":
                unitFlagForSession = True
                break
        checkEqualAssert(False, unitFlagForSession, selectedQuicklink, selectedMeasure,message='Validate that no unit is seen for the session(Table View)', testcase_id='MKR-3092')

    l = []
    for i in range(len(selectedMeasure_value_list)):
        if str(selectedMeasure_value_list[i]).strip()!='' and str(selectedMeasure_value_list[i]).strip()!='NA':
            l.append(UnitSystem().getRawValueFromUI(selectedMeasure_value_list[i]))

    sorting_Flag = verifySortingWithSomeDifference(l)
    checkEqualAssert(True,sorting_Flag,selectedQuicklink,selectedMeasure,message='Verify that table data order must be highest to lowest wrt selected measure :: Value_List ='+str(selectedMeasure_value_list),testcase_id='MKR-3561')
    return

def validateColorSequence(barColorDict,data,coloumIndexOfColor=0):
    colorSequenceFromTable=[]
    colorSequenceFlag = True

    if data['rows']!=Constants.NODATA:
        for row in data['rows']:
            colorSequenceFromTable.append(row[coloumIndexOfColor])

        logger.info('Got color list from table = %s',str(colorSequenceFromTable))

        if barColorDict!={} and colorSequenceFromTable!=[]:
            for key in barColorDict.keys():
                colorIndexList=[]
                for color in barColorDict[key]:
                    try:
                        colorIndexList.append(colorSequenceFromTable.index(color))
                    except Exception as e:
                        logger.error("Color on bar not found in Table : Bar color = %s Color List From table = %s",str(color),str(colorSequenceFromTable))
                        return False

                if colorIndexList!=sorted(colorIndexList):
                    colorSequenceFlag=False
                    break
    else:
        logger.error("Table Not Found hence can't verify color sequence")

    return colorSequenceFlag


def validateColorOnTooltipWithBar(toolTipData,barColorDict):
    logger.info("Method called : validateColorOnTooltipWithBar")
    try:
        checkEqualAssert(len(barColorDict.keys()), len(toolTipData.keys()),message="Verify hover on each bar",testcase_id="MKR-3564")
        if len(barColorDict.keys())!=0:
            for key in barColorDict.keys():
                logger.info("Going to validate tooltip for %s",str(key))
                toolTipColor=[]
                percentageOnTooltip=[]
                checkEqualAssert(len(barColorDict[key.strip()]),len(toolTipData[key.strip()]),message="Verify equal number of color on bar and tooltip")
                for row in toolTipData[key.strip()]:
                    toolTipColor.append(row[0])
                    percentageOnTooltip.append(float(row[1].split('(')[1].split('%')[0].strip()))

                checkEqualAssert(barColorDict[key.strip()],toolTipColor,message="Verify Color on tooltip with bar for "+str(key))
                if toolTipColor!=[]:
                    checkEqualAssert(100.0,round(sum(percentageOnTooltip),2),message="Verify total percantage on toolTip for "+str(key))
        else:
            logger.info("Bar not found : check manually")

    except Exception as e:
        logger.error("Got Exception during validating tootTip with bar =%s",str(e))


def expandMoreOnCB(setup,screenInstance,screenname,parent='expand_more',child='load_more',barParent='trend-main',checkLoadMore=True):
    ################## return False in this method ===> Pass scenarios are being hit
    if checkLoadMore:
        logger.info("Method called : expandMoreOnCB")
        numberOfBarBeforeClick,barHandles=screenInstance.trend.getAllBar_DCT(getHandle(setup,screenname,barParent))
        h=getHandle(setup,screenname,parent)
        if len(h[parent][child])!=0:
            try:
                h[parent][child][0].click()
                sleep(MRXConstants.SleepForComparativeScreen)
                numberOfBarAfterClick, barHandles = screenInstance.trend.getAllBar_DCT(getHandle(setup, screenname, barParent))

                if numberOfBarAfterClick-numberOfBarBeforeClick == 10:
                    checkEqualAssert(True, numberOfBarAfterClick - numberOfBarBeforeClick == 10,message='Verify the functionality of the ' + str(child) + ' link',testcase_id='MKR-3574')
                    return False

                elif numberOfBarAfterClick-numberOfBarBeforeClick < 10:
                    h = getHandle(setup, screenname, parent)
                    if len(h[parent][child]) != 0:
                        checkEqualAssert(True, numberOfBarAfterClick - numberOfBarBeforeClick == 10,message='Verify the functionality of the ' + str(child) + ' link',testcase_id='MKR-3574')
                        return True
                    else:
                        checkEqualAssert(True, numberOfBarAfterClick - numberOfBarBeforeClick < 10, message='Verify the functionality of the ' + str(child) + ' link',testcase_id='MKR-3574')
                        return False

                elif numberOfBarAfterClick-numberOfBarBeforeClick > 10:
                    checkEqualAssert(True, numberOfBarAfterClick - numberOfBarBeforeClick <= 10,message='Verify the functionality of the ' + str(child) + ' link',testcase_id='MKR-3574')
                    return True

            except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                return e
        else:
            return True
    else:
        return False




def expandMoreOnCBTable(setup,screenInstance,screenname,parent='expand_more',child='show_other',tableParent='table',checkShowOther=True):
    ################## return False in this method ===> Pass scenarios are being hit
    if checkShowOther:
        logger.info("Method called : expandMoreOnCBTable")

        tableData_beforeClick = screenInstance.table.getTableData1WithColumnHavingColor(getHandle(setup, MRXConstants.COMPARATIVESCREEN, tableParent),length=30)
        numberOfRows_beforeClick = len(tableData_beforeClick['rows'])
        logger.info("No of Rows inside table before clicking Show others = " + str(numberOfRows_beforeClick))

        column1_list = [row[1] for row in tableData_beforeClick['rows']]
        if  "Others" in  column1_list:
            logger.info("Data for Others present inside table")
            if numberOfRows_beforeClick == 11:
                colorForOthers = tableData_beforeClick['rows'][column1_list.index("Others")][0]
                numberOfRowsWithOthers_beforeClick = len([row for row in tableData_beforeClick['rows'] if row[0] == colorForOthers and row[1] != "Others"])
                h = getHandle(setup, screenname, parent)
                if len(h[parent][child]) != 0:
                    try:
                        h[parent][child][0].click()
                        sleep(MRXConstants.SleepForComparativeScreen)
                        tableData_afterClick = screenInstance.table.getTableData1WithColumnHavingColor(getHandle(setup, MRXConstants.COMPARATIVESCREEN, tableParent),length=30)
                        numberOfRowsWithOthers_AfterClick = len([row for row in tableData_afterClick['rows'] if row[0] == colorForOthers and row[1] != "Others"])

                        if numberOfRowsWithOthers_AfterClick - numberOfRowsWithOthers_beforeClick == 10:
                            checkEqualAssert(True,numberOfRowsWithOthers_AfterClick - numberOfRowsWithOthers_beforeClick == 10,message='Verify the functionality of the ' + str(child) + ' link',testcase_id='MKR-3577')
                            return False

                        elif numberOfRowsWithOthers_AfterClick - numberOfRowsWithOthers_beforeClick < 10:
                            h = getHandle(setup, screenname, parent)
                            if len(h[parent][child]) != 0:
                                checkEqualAssert(True,numberOfRowsWithOthers_AfterClick - numberOfRowsWithOthers_beforeClick == 10,message='Verify the functionality of the ' + str(child) + ' link',testcase_id='MKR-3577')
                                return True
                            else:
                                checkEqualAssert(True,numberOfRowsWithOthers_AfterClick - numberOfRowsWithOthers_beforeClick < 10,message='Verify the functionality of the ' + str(child) + ' link',testcase_id='MKR-3577')
                                return False

                        elif numberOfRowsWithOthers_AfterClick - numberOfRowsWithOthers_beforeClick > 10:
                            checkEqualAssert(True, numberOfRowsWithOthers_AfterClick - numberOfRowsWithOthers_beforeClick <= 10,message='Verify the functionality of the ' + str(child) + ' link',testcase_id='MKR-3577')
                            return True

                    except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                        return e

            else:
                logger.info("Table is containing data for 'Others' though the Number of Rows %s being displayed is (< or >) than top 10 rows " %str(numberOfRows_beforeClick))
                if numberOfRows_beforeClick < 11:
                    checkEqualAssert(False, numberOfRows_beforeClick < 11 ,message="Verify data for 'Others' group does not exist if Number of rows inside table is <10" )
                elif numberOfRows_beforeClick > 11:
                    checkEqualAssert(False, numberOfRows_beforeClick > 11,message="Verify that only 10 rows are displayed inside the table in addition to the row for 'Others'")
                    return True

        else:
            h = getHandle(setup, screenname, parent)
            checkEqualAssert(0, len(h[parent][child]) ,message="Verify that Show Others link is not visible if table does not contain data for Others")
            return True
    else:
        return False



def setQuickLink_Compare_Measure_BreakDown(setup,cbScreenInstance,k='0'):

    quicklink = setup.cM.getNodeElements("cbScreenFilters", 'quicklink')
    CompareDim = setup.cM.getNodeElements("cbScreenFilters", 'compareDim')[str(k)]['locatorText']
    CompareMes = setup.cM.getNodeElements("cbScreenFilters", 'measure')[str(k)]['locatorText']
    BrokenDown = setup.cM.getNodeElements("cbScreenFilters", 'breakDown')[str(k)]['locatorText']

    selectedCompareDim = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(CompareDim), index=0, parent="allselects")
    selectedCompareMes = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(CompareMes), index=1, parent="allselects")
    selectedBrokenDown = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(BrokenDown), index=2, parent="allselects")

    logger.info("Going to Select Compare =%s, By =%s, Brokendown  =%s",str(CompareDim),str(CompareMes),str(BrokenDown))

    if quicklink[str(k)]['locatorText'] == 'CustomClick':
        selectedQuicklink=quicklink[str(k)]['locatorText']
        calHandler = getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs")
        logger.info("Launching Calendar from UDP Popup")
        calHandler['ktrs']['datepicker'][0].click()
        logger.info("Calendar picker is clicked")

        ################################### For test Calender Scenario #################################################

        if k=='testCalender':
            [year, month, day, hour, min] = str(quicklink[str(k)]['startTime']).split(' ')
            setCalendar(year, month, day, hour, min, cbScreenInstance, setup, page=Constants.CALENDERPOPUP,parent="leftcalendar")

            [et_year, et_month, et_day, et_hour, et_min] = str(quicklink[str(k)]['endTime']).split(' ')
            setCalendar(et_year, et_month, et_day, et_hour, et_min, cbScreenInstance, setup, Constants.CALENDERPOPUP,"rightcalendar")

            valueFromCalender1 = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()

            #stepoch,etepoch=parseTimeRange1(valueFromCalender1,timezone=MRXConstants.TIMEZONEOFFSET,pattern="%d %b %Y")
            stepoch, etepoch = parseTimeRange1(valueFromCalender1, timezone=MRXConstants.TIMEZONEOFFSET,pattern=MRXConstants.TIMEPATTERN)
            try:
                if etepoch-stepoch < 0:
                    UDHelper.button_Status(False,"Start Time > End Time ==> Selected Time Range ="+valueFromCalender1, cbScreenInstance, setup,Constants.CALENDERPOPUP, "Apply",testcase_id='3559')
                else:
                    checkEqualAssert(True,etepoch-stepoch>=0,"Verify that StartTime > EndTime is not allowed to choose ",testcase_id='MKR-3559')
            except:
                logger.info("Skipping TestCase =")

            monthListFormLeftCalender=getAvailableMonthList(setup,parent='leftcalendar')
            checkEqualAssert(MRXConstants.MONTHLIST,monthListFormLeftCalender,message='Verify that all the months should be there in the custom calendar (Left Calender)',testcase_id='3559')

            monthListFormRightCalender = getAvailableMonthList(setup, parent='rightcalendar')
            checkEqualAssert(MRXConstants.MONTHLIST, monthListFormRightCalender,message='Verify that all the months should be there in the custom calendar (Right Calender)',testcase_id='3559')

            cbScreenInstance.clickButton("Cancel", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))

            return valueFromCalender1,selectedCompareDim, selectedCompareMes, selectedBrokenDown
        ################################################################################################################


        [year, month, day, hour, min] = str(quicklink[str(k)]['startTime']).split(' ')
        setCalendar(year, month, day, hour, min, cbScreenInstance, setup, page=Constants.CALENDERPOPUP,parent="leftcalendar")

        [et_year, et_month, et_day, et_hour, et_min] = str(quicklink[str(k)]['endTime']).split(' ')
        setCalendar(et_year, et_month, et_day, et_hour, et_min, cbScreenInstance, setup,Constants.CALENDERPOPUP, "rightcalendar")

        valueFromCalender=str(getHandle(setup,Constants.CALENDERPOPUP,'allspans')['allspans']['span'][0].text).strip()
        # Closing Calendar Pop Up
        cbScreenInstance.clickButton("Apply",getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))
        logger.info("Calendar Selection done at Filter Popup = %s ", valueFromCalender)
        t1 = cbScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.UDSCREEN, "ktrs"))
        checkEqualAssert(valueFromCalender, t1, selectedQuicklink,message="verify quicklink label")

    else:
        cbScreenInstance.timeBar.setQuickLink(quicklink[str(k)]['locatorText'], getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))
        isError(setup)
        selectedQuicklink = cbScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))
        t = TimeRangeComponentClass().get_Label(str(quicklink[str(k)]['locatorText']).replace(' ','').lower())
        t1 = cbScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))
        checkEqualAssert(t[1], t1, selectedQuicklink,message="verify quicklink label")



    timeRangeFromPopup = str(t1)

    return timeRangeFromPopup,selectedCompareDim, selectedCompareMes, selectedBrokenDown



def setQuickLink_Compare_Measure_BreakDown_forDV(setup, screenInstance, quicklink, compareDim, measure, breakdownDim):
    logger.info("Selecting Quicklink on screen: " +  str(quicklink))
    try:
        screenInstance.timeBar.setQuickLink(quicklink, getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))
        isError(setup)
        logger.info("Quicklink selected: " +str(quicklink))
        # selectedQuicklink = cbScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))
        t1 = screenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))
        timeRangeFromScreen = str(t1)
    except Exception as e:
        logger.info("Exception on selecting quicklink" +str(e))


    logger.info("Selecting Compare: %s, Measure: %s, Breakdown: %s on screen: " %(compareDim,measure,breakdownDim))
    try:
        selectedCompareDim = screenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), compareDim, index=0, parent="allselects")
    except Exception as e:
        logger.info("Exception on selecting Compare" + str(e))
    try:
        selectedCompareMes = screenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), measure, index=1, parent="allselects")
    except Exception as e:
        logger.info("Exception on selecting Measure" + str(e))
    try:
        selectedBrokenDown = screenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), breakdownDim, index=2, parent="allselects")
    except Exception as e:
        logger.info("Exception on selecting BreakDown" + str(e))


    return  timeRangeFromScreen, selectedCompareDim, selectedCompareMes, selectedBrokenDown

def getChartLegendheaders(h,parent='chart_legend_headers',child='text_over_chart'):
    logger.info("Method Called : getChartLegendheaders")

    if len(h[parent][child]) > 0:
        headerText = str(h[parent][child][0].text)
        logger.info("Text returned: " +headerText)
        return headerText
    else:
        logger.info("No element found for Child: " + child + " and Parent: " + parent)


def getMsgOnNoData(h,parent='cb_no_data_msg',child='msgOnChart'):
    logger.info("Method Called : getMsgOnNoData")

    if len(h[parent][child]) > 0:
        msgDisplayed = str(h[parent][child][0].text)
        logger.info("Text returned: " + msgDisplayed)
        return msgDisplayed
    else:
        logger.info("No element found for Child: " + child + " and Parent: " + parent)


