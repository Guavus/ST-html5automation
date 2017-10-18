from Utils.utility import *
from MRXUtils.MRXConstants import *





def VerifyBasicTableFuncationality(setup,screenInstance,ScreenTableHeaderList=MRXConstants.SegmentScreenTableHeaderList,parent='table'):
    columns = setup.cM.getNodeElements("reportsorttablecolumn", "column")
    column_names = []
    for k, column in columns.iteritems():
        column_names.append(column['locatorText'])

    tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, parent)
    tableMap = screenInstance.table.getTableDataMap(tableHandle,driver=setup,colIndex=-1)
    checkEqualAssert(ScreenTableHeaderList,tableMap['header'],'','','Verify Table Header on Screen',testcase_id='MKR-1658')

    if tableMap['rows'] == Constants.NODATA:
        logger.info("*********Table Data Not Present************")
        return

    for columnname in column_names:
        sortedData = sortTable(setup, screenInstance, columnName=columnname)
        resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnname)

        for k, v in sortedData.iteritems():
            if tableMap['rows'].has_key(k):
                checkEqualAssert(tableMap['rows'][k], sortedData[k],"", "","verify sorted Table rows present in table with key : " + k)
            else:
                logger.info("********table not contain row with key********* : " + k)
def sortTable(setup,insatnce,columnName="Name"):
    tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, "table")
    insatnce.table.sortTable1(tableHandle, columnName)
    tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, "table")

    data2 = insatnce.table.getTableData1(tableHandle)
    columnIndex = insatnce.table.getIndexForValueInArray(data2['header'], columnName)

    col = []
    for i in range(len(data2['rows'])):
        col.append(data2['rows'][i][columnIndex])

    checkEqualAssert(sorted(col, reverse=True), col, "", "", "Verify Sorting For ColumnName ="+columnName,testcase_id='MKR-1691')


    logger.info("Sorted")
    cdata2 = insatnce.table.convertDataToDictWithKeyAsRow(data2)
    return cdata2


def clickOnfilterIcon(setup,screen,filterIcon,parent='filterArea'):
    logger.info("Clicking on FilterIcon")
    h=getHandle(setup,screen,parent)
    try:
        h[parent][filterIcon][0].click()
    except:
        logger.info('Not able to click on = %s',filterIcon)
        resultlogger.info('Not able to click on = %s', filterIcon)
        return False
    return True


def createFilterMap(filters,keys):
    return dict(zip(keys,filters))


def findPropertyColor(screenInstance,h,property,parent="allinputs",child="input",index=0):
    propertycolor=str(h[parent][child][index].value_of_css_property(property))
    return screenInstance.cm.rgb_to_hex(propertycolor)


def checkSlider(screenInstance,h,index=0):
    colorOfEnabled = findPropertyColor(screenInstance, h, property=Constants.BACKGROUNDCOLOR, parent='allsliders',child='slider', index=index)
    if str(colorOfEnabled) != MRXConstants.WHITECOLOR:
        return False
    else:
        return True


def setSlider(screenInstance,h,index=0):
    if not checkSlider(screenInstance,h,index=index):
        try:
            screenInstance.cm.click(h['allsliders']['slider'][index])
            time.sleep(2)
            return checkSlider(screenInstance,h,index=index)
        except:
            logger.debug("Not able to Click on Slider")
            return False


def dumpResultForButton(condition,request,screenInstance,setup,screen=MRXConstants.POPUPSCREEN,button_label="Import"):
    button_status=screenInstance.cm.isButtonEnabled(button_label,getHandle(setup, screen,"allbuttons"))
    if screen==MRXConstants.FILTERSCREEN:
        checkEqualAssert(condition,button_status,"","","Checking State of "+button_label+" button for Fields entered : "+str(request),testcase_id='MKR-1680')

    checkEqualAssert(condition, button_status, "", "","Checking State of " + button_label + " button for Fields entered : " + str(request))
    return button_status


def setInputFilter(setup,screenInstance,h,global_filter,index,input_index,tab_name,k=0):
    selectedFilter_list = []
    if str(global_filter[str(k)][tab_name]) != ' ':
        if setSlider(screenInstance, h, int(index)):
            selectedFilter_list.append(str(screenInstance.cm.sendkeys_input(str(global_filter[str(k)][tab_name]), h, input_index)))
            dumpResultForButton(True, tab_name, screenInstance, setup, screen=MRXConstants.FILTERSCREEN,button_label="Apply Filters")
    return selectedFilter_list



def setFilters(setup,screenInstance,h,k=0):
    selected_filter = []
    global_filter = setup.cM.getNodeElements("reportFilter", "filter")

    ##########  set Report Name ################
    filter_reportName = setInputFilter(setup, screenInstance, h, global_filter, 0, 0, 'reportname', k)
    selected_filter.append(filter_reportName)


    ########### set Report Type
    filter_reportType = setInputFilter(setup, screenInstance, h, global_filter, 1, 1, 'reporttype', k)
    selected_filter.append(filter_reportType)


    ########## set Delivered On
    selectedFilter_listforDelieveredOn = []
    if str(global_filter[str(k)]['deliveredon']).split('::')[0] != ' ' and \
                    str(global_filter[str(k)]['deliveredon']).split('::')[1] != ' ':
        if setSlider(screenInstance, h, 2):
            select = screenInstance.picker.domultipleSelectionWithIndex(getHandle(setup, MRXConstants.FILTERSCREEN, "allDropDown"), [int(str(global_filter[str(k)]['deliveredon']).split('::')[0].strip(''))], index=0, parent="allDropDown")
            if select == ['']:
                select = screenInstance.picker.getSingleSelectionFromMultiDropDown(getHandle(setup, MRXConstants.FILTERSCREEN, "allDropDown"), index=0, parent="allDropDown")

            dumpResultForButton(False, "Delivered on without Date", screenInstance, setup,
                                screen=MRXConstants.FILTERSCREEN, button_label="Apply Filters")
            try:
                te = setup.d.execute_script("return document.getElementsByClassName('datePickerIcon')")
                setup.d.execute_script("arguments[0].click()", te[0])
                [year, month, day, hour, min] = str(global_filter[str(k)]['deliveredon']).split('::')[1].split(' ')
                setCalendar(year, month, day, hour, min, screenInstance, setup, page=Constants.CALENDERPOPUP,
                            parent="leftcalendar")
                screenInstance.cm.clickButton("Apply", getHandle(setup, Constants.CALENDERPOPUP, "allbuttons"))
                choosedate = screenInstance.cm.getValue_input(h, 2)
                selectedFilter_listforDelieveredOn.append(str(select) + " " + str(choosedate))
                dumpResultForButton(True, "Delivered on with Date", screenInstance, setup,
                                    screen=MRXConstants.FILTERSCREEN, button_label="Apply Filters")
            except:
                logger.debug('Not able to click on DatePickerIcon')
                screenInstance.cm.click(h['allsliders']['slider'][2])
                time.sleep(2)
    selected_filter.append(selectedFilter_listforDelieveredOn)



    ########## set Report period Start Date and End Date

    selectedFilter_listForPeriod = []
    if str(global_filter[str(k)]['reportperiod']).split('::')[0] != ' ' and \
                    str(global_filter[str(k)]['reportperiod']).split('::')[1] != ' ':
        if setSlider(screenInstance, h, 3):
            try:
                te = setup.d.execute_script("return document.getElementsByClassName('datePickerIcon')")
                setup.d.execute_script("arguments[0].click()", te[1])

                [year, month, day, hour, min] = str(global_filter[str(k)]['reportperiod']).split('::')[0].split(' ')
                setCalendar(year, month, day, hour, min, screenInstance, setup, page=Constants.CALENDERPOPUP,
                            parent="leftcalendar")
                screenInstance.cm.clickButton("Apply", getHandle(setup, Constants.CALENDERPOPUP, "allbuttons"))
                chooseStartDate = screenInstance.cm.getValue_input(h, 3)
                dumpResultForButton(True, " Report Period with Start date and without End Date", screenInstance, setup,
                                    screen=MRXConstants.FILTERSCREEN, button_label="Apply Filters")


                te = setup.d.execute_script("return document.getElementsByClassName('datePickerIcon')")
                setup.d.execute_script("arguments[0].click()", te[2])
                [year, month, day, hour, min] = str(global_filter[str(k)]['reportperiod']).split('::')[1].split(' ')
                setCalendar(year, month, day, hour, min, screenInstance, setup, page=Constants.CALENDERPOPUP,
                            parent="leftcalendar")
                screenInstance.cm.clickButton("Apply", getHandle(setup, Constants.CALENDERPOPUP, "allbuttons"))
                chooseEndDate = screenInstance.cm.getValue_input(h, 4)
                selectedFilter_listForPeriod.append(str(chooseStartDate) + " - " + str(chooseEndDate))

                dumpResultForButton(True, " Report Period with Start and End Date ", screenInstance, setup,
                                    screen=MRXConstants.FILTERSCREEN, button_label="Apply Filters")
            except:
                logger.debug('Not able to click on DatePickerIcon')
                screenInstance.cm.click(h['allsliders']['slider'][3])
                time.sleep(2)
    selected_filter.append(selectedFilter_listForPeriod)

    return selected_filter



def setReportFilter(setup,screenInstance,k='0'):
    Expectedfilter=[]
    handle=getHandle(setup,MRXConstants.FILTERSCREEN)
    Keys = setup.cM.getAllNodeElements("report_Filters", "filter")
    Expectedfilter = createFilterMap(setFilters(setup,screenInstance,handle,k=k),Keys)
    return Expectedfilter


def getGlobalFiltersFromScreen(screenName,screenInstance, setup,flag=True):
    Keys = setup.cM.getAllNodeElements("report_Filters", "filter")
    actualFilters = insertKeys(screenInstance.globalfilter.getAllSelectedFilters(getHandle(setup,screenName,"filterArea"),flag=flag),Keys)
    return actualFilters


def getGlobalFiltersToolTipData(screenName,filterScreenInstance,setup,flag=True):
    Keys = setup.cM.getAllNodeElements("report_Filters", "filter")
    actualFilters = insertKeys(filterScreenInstance.globalfilter.getToolTipData(setup,getHandle(setup,screenName),screenName=MRXConstants.REPORTSCREEN,flag=flag),Keys)
    return actualFilters



def setReportFilter(setup,screenInstance,k='0'):
    Expectedfilter=[]
    handle=getHandle(setup,MRXConstants.FILTERSCREEN)
    Keys = setup.cM.getAllNodeElements("report_Filters", "filter")
    Expectedfilter = createFilterMap(setFilters(setup,screenInstance,handle,k=k),Keys)
    return Expectedfilter


def getInputFilter(screenInstance,h,index,input_index):
    selectedFilter_list = []
    if checkSlider(screenInstance, h, int(index)):
        selectedFilter_list.append(str(screenInstance.cm.getValue_input(h,input_index)))
    return selectedFilter_list


def getMultiDropDownFilter(screenInstance,h,index,multi_index,max_selection_option):
    selectedFilter_list = []
    if checkSlider(screenInstance, h, int(index)):
        selected_list = screenInstance.picker.getSelection(h,int(multi_index),parent="allDropDown")
        if len(selected_list) == int(max_selection_option):
            selectedFilter_list.append(MRXConstants.ALL)
        else:
            selectedFilter_list.append(str(' , '.join(selected_list)))
    return selectedFilter_list


def getFilters(setup,screenInstance,h):

    selected_filter=[]

    ##  get Report Name
    filter_reporttName = getInputFilter(screenInstance, h, 0, 0)
    selected_filter.append(filter_reporttName)


    ##  get Report Type
    filter_reporttName = getInputFilter(screenInstance, h, 1, 1)
    selected_filter.append(filter_reporttName)


    ##  get Delivered On
    selectedFilter_listforDeliveredOn = []
    if checkSlider(screenInstance, h, 2):
        select = screenInstance.picker.getSingleSelectionFromMultiDropDown(getHandle(setup, MRXConstants.FILTERSCREEN, "allDropDown"),index=0,parent="allDropDown")

        choosedate = screenInstance.cm.getValue_input(h, 2)
        selectedFilter_listforDeliveredOn.append(str(select) + " " + str(choosedate))
    selected_filter.append(selectedFilter_listforDeliveredOn)


    ##  get Report Period
    selectedFilter_listforPeriod = []
    if checkSlider(screenInstance, h, 3):
        chooseStartDate = screenInstance.cm.getValue_input(h, 3)
        chooseEndDate = screenInstance.cm.getValue_input(h, 4)

        selectedFilter_listforPeriod.append(str(chooseStartDate) + " - " + str(chooseEndDate))
    selected_filter.append(selectedFilter_listforPeriod)


    return selected_filter




def getReportFilter(setup,screenInstance):
    Expectedfilter=[]
    handle=getHandle(setup,MRXConstants.FILTERSCREEN)
    Keys = setup.cM.getAllNodeElements("report_Filters", "filter")
    Expectedfilter = createFilterMap(getFilters(setup,screenInstance,handle),Keys)
    return Expectedfilter




def insertKeys(dictionary,keys):
    if type(dictionary) == dict:
        for k in keys:
            if k not in dictionary.keys():
                dictionary[k] = []
        return dictionary
    else:
        return dictionary
