from Utils.utility import *
from MRXConstants import *
from classes.Components.TimeRangeComponentClass import *
from MRXUtils import UDHelper
from selenium.webdriver import ActionChains
import json

Delimiter=' , '
DictContainingTree={}

def getDEPopupHeaderText(setup,screenName,index=0,parent='allspans',child='span'):
    logger.info("Method Called : getDEPopupHeaderText")
    handle = getHandle(setup,screenName,parent)
    if len(handle[parent][child])>0:
        return str(handle[parent][child][index].text)
    else:
        return "Header Text Not Found"


def setQuickLink_Measure_TopRows(setup, deScreenInstance, i='0'):
    quicklink = setup.cM.getNodeElements("deScreenFilters", 'quicklink')
    measure = setup.cM.getNodeElements("deScreenFilters", 'measure')
    toprows=setup.cM.getNodeElements("deScreenFilters",'toprows')

    if quicklink[str(i)]['locatorText'] == 'CustomClick':
        selectedQuicklink=quicklink[str(i)]['locatorText']
        calHandler = getHandle(setup, MRXConstants.DEPOPUP, "ktrs")
        logger.info("Launching Calendar from Filter Popup")
        calHandler['ktrs']['datepicker'][0].click()
        logger.info("Calendar picker is clicked")

        ################################### For test Calender Scenario #################################################

        if i=='testCalender':
            [year, month, day, hour, min] = str(quicklink[str(i)]['startTime']).split(' ')
            setCalendar(year, month, day, hour, min, deScreenInstance, setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

            [et_year, et_month, et_day, et_hour, et_min] = str(quicklink[str(i)]['endTime']).split(' ')
            setCalendar(et_year, et_month, et_day, et_hour, et_min, deScreenInstance, setup, Constants.CALENDERPOPUP, "rightcalendar")

            valueFromCalender1 = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()

            stepoch,etepoch=parseTimeRange1(valueFromCalender1,timezone=MRXConstants.TIMEZONEOFFSET)
            try:
                if etepoch-stepoch <=0:
                    UDHelper.button_Status(False,"When Start Time > End Time ==> Selected Time Range =" + valueFromCalender1, deScreenInstance, setup, Constants.CALENDERPOPUP, "Apply", testcase_id='MKR-3188')
                else:
                    checkEqualAssert(True,etepoch-stepoch>=0,"Not allow to choose StartTime > EndTime",testcase_id='MKR-3188')
            except:
                logger.info("Skipping TestCase = "+ str('MKR-3188'))

            monthListFormLeftCalender=getAvailableMonthList(setup,parent='leftcalendar')
            checkEqualAssert(MRXConstants.MONTHLIST,monthListFormLeftCalender,message='Verify that all the months should be there in the custom calendar (Left Calender)',testcase_id='MKR-3191')

            monthListFormRightCalender = getAvailableMonthList(setup, parent='rightcalendar')
            checkEqualAssert(MRXConstants.MONTHLIST, monthListFormRightCalender,message='Verify that all the months should be there in the custom calendar (Right Calender)',testcase_id='MKR-3191')

            deScreenInstance.clickButton("Cancel", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))

            return
        ################################################################################################################


        [year, month, day, hour, min] = str(quicklink[str(i)]['startTime']).split(' ')
        setCalendar(year, month, day, hour, min, deScreenInstance, setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

        [et_year, et_month, et_day, et_hour, et_min] = str(quicklink[str(i)]['endTime']).split(' ')
        setCalendar(et_year, et_month, et_day, et_hour, et_min, deScreenInstance, setup, Constants.CALENDERPOPUP, "rightcalendar")

        valueFromCalender=str(getHandle(setup,Constants.CALENDERPOPUP,'allspans')['allspans']['span'][0].text).strip()
        # Closing Calendar Pop Up
        deScreenInstance.clickButton("Apply", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))
        logger.info("Calendar Selection done at Filter Popup = %s ", valueFromCalender)
        t1 = deScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.DEPOPUP, "ktrs"))
        checkEqualAssert(valueFromCalender, t1, selectedQuicklink, "", "verify quicklink label")

    else:
        deScreenInstance.timeBar.setQuickLink(quicklink[str(i)]['locatorText'], getHandle(setup, MRXConstants.DEPOPUP, "ktrs"))
        isError(setup)
        selectedQuicklink = deScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.DEPOPUP, "ktrs"))
        t = TimeRangeComponentClass().get_Label(str(quicklink[str(i)]['locatorText']).replace(' ','').lower())
        t1 = deScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.DEPOPUP, "ktrs"))
        checkEqualAssert(t[1], t1, selectedQuicklink, "", "verify quicklink label")

    selectedMeasure = deScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.DEPOPUP, "allselects"), str(measure[str(i)]['locatorText']), index=0, parent="allselects")
    timeRangeFromPopup = str(t1)
    measureFromPopup=str(selectedMeasure).strip()

    toprows=deScreenInstance.cm.sendkeys_input(str(toprows[str(i)]['value']), getHandle(setup, MRXConstants.DEPOPUP, "allinputs"), 0)
    toprowsFromPopup =0

    if str(toprows).strip()=='':
        toprowsFromPopup=MRXConstants.MaximumValueForTopRowInput
    else:
        try:
            toprowsFromPopup=int(toprows)
        except:
            logger.error("Value for top rows is other than int:: check manually")
            resultlogger.error("Value for top rows is other than int:: check manually")

    return timeRangeFromPopup,measureFromPopup,toprowsFromPopup


def del_Key_ForSelectedMethod(keyList,method):
    key_List=deepcopy(keyList)
    method_Index=-1
    if method in keyList:
        method_Index=keyList.index(method)
        key_List.remove(method)
    return key_List,method_Index

def setDEFilters(udpScreenInstance,setup,selectedMethod,k='0',validateAvailableMethod=False,toggleStateFlag=False):
    global DictContainingTree
    DictContainingTree = {}
    segment_Keys =setup.cM.getAllNodeElements("segmenntFilters","filter")
    device_Keys  = setup.cM.getAllNodeElements("deviceFilters","filter")
    network_Keys = setup.cM.getAllNodeElements("networkFilters","filter")
    content_Keys = setup.cM.getAllNodeElements("contentFilters","filter")
    usage_Keys = setup.cM.getAllNodeElements("usageFilters","filter")

    segmentKeys,methodIndexForSegment = del_Key_ForSelectedMethod(segment_Keys,selectedMethod)
    deviceKeys,methodIndexForDevice = del_Key_ForSelectedMethod(device_Keys,selectedMethod)
    networkKeys,methodIndexForNetwork = del_Key_ForSelectedMethod(network_Keys,selectedMethod)
    contentKeys,methodIndexForContent = del_Key_ForSelectedMethod(content_Keys,selectedMethod)
    usageKeys,methodIndexForUsage = del_Key_ForSelectedMethod(usage_Keys,selectedMethod)

    segmentFilters = UDHelper.createFilterMap(setFilters(setup,udpScreenInstance,"segment",methodIndexForSegment,selectedMethod,segmentKeys,segment_Keys,k,validateAvailableMethod,toggleStateFlag),segmentKeys)
    deviceFilters = UDHelper.createFilterMap(setFilters(setup,udpScreenInstance,"device",methodIndexForDevice,selectedMethod,deviceKeys,device_Keys,k,validateAvailableMethod,toggleStateFlag),deviceKeys)
    networkFilters = UDHelper.createFilterMap(setFilters(setup,udpScreenInstance,"network",methodIndexForNetwork,selectedMethod,networkKeys,network_Keys,k,validateAvailableMethod,toggleStateFlag),networkKeys)
    contentFilters = UDHelper.createFilterMap(setFilters(setup,udpScreenInstance,"content",methodIndexForContent,selectedMethod,contentKeys,content_Keys,k,validateAvailableMethod,toggleStateFlag),contentKeys)
    usageFilters = UDHelper.createFilterMap(setFilters(setup,udpScreenInstance,"usage",methodIndexForUsage,selectedMethod,usageKeys,usage_Keys,k,validateAvailableMethod,toggleStateFlag),usageKeys)

    expectedFilters = merge_dictionaries(merge_dictionaries(merge_dictionaries(merge_dictionaries(segmentFilters,deviceFilters),networkFilters),contentFilters),usageFilters)
    if toggleStateFlag:
        logger.info('Selected toggleStateList are =%s', expectedFilters)
        resultlogger.info('Selected toggleStateList are =%s', expectedFilters)
    else:
        logger.info('Selected filter are =%s',expectedFilters)
        resultlogger.info('Selected filter are =%s',expectedFilters)

    return expectedFilters


def getToggleStateForFilters(udpScreenInstance,setup,selectedMethod,k='0',validateSearch=False):
    segment_Keys =setup.cM.getAllNodeElements("segmenntFilters","filter")
    device_Keys  = setup.cM.getAllNodeElements("deviceFilters","filter")
    network_Keys = setup.cM.getAllNodeElements("networkFilters","filter")
    content_Keys = setup.cM.getAllNodeElements("contentFilters","filter")
    usage_Keys = setup.cM.getAllNodeElements("usageFilters","filter")

    segmentKeys,methodIndexForSegment = del_Key_ForSelectedMethod(segment_Keys, selectedMethod)
    deviceKeys,methodIndexForDevice = del_Key_ForSelectedMethod(device_Keys, selectedMethod)
    networkKeys,methodIndexForNetwork = del_Key_ForSelectedMethod(network_Keys, selectedMethod)
    contentKeys,methodIndexForContent = del_Key_ForSelectedMethod(content_Keys, selectedMethod)
    usageKeys,methodIndexForUsage = del_Key_ForSelectedMethod(usage_Keys, selectedMethod)

    segmentFilters = UDHelper.createFilterMap(getToggleState(setup,udpScreenInstance,"segment",methodIndexForSegment,k=k,validateSearch=validateSearch),segmentKeys)
    deviceFilters = UDHelper.createFilterMap(getToggleState(setup,udpScreenInstance,"device",methodIndexForDevice,k=k,validateSearch=validateSearch),deviceKeys)
    networkFilters = UDHelper.createFilterMap(getToggleState(setup,udpScreenInstance,"network",methodIndexForNetwork,k=k,validateSearch=validateSearch),networkKeys)
    contentFilters = UDHelper.createFilterMap(getToggleState(setup,udpScreenInstance,"content",methodIndexForContent,k=k,validateSearch=validateSearch),contentKeys)
    usageFilters = UDHelper.createFilterMap(getToggleState(setup,udpScreenInstance,"usage",methodIndexForUsage,k=k,validateSearch=validateSearch),usageKeys)

    toggleStateForFilters = merge_dictionaries(merge_dictionaries(merge_dictionaries(merge_dictionaries(segmentFilters,deviceFilters),networkFilters),contentFilters),usageFilters)
    return toggleStateForFilters

def getToggleState(setup,udpScreenInstance,tab_name,method_Index,k ="0",validateSearch=False):
    udp_filter= UDHelper.parseFilters(setup.cM.getNodeElements("deScreenFilters",tab_name))
    udpfilters= setup.cM.getNodeElements("udpfilters","filter")
    udpScreenInstance.clickLink(udpfilters[tab_name]['locatorText'], getHandle(setup, MRXConstants.DEPOPUP, MRXConstants.ALLLINKS))

    toggleStateList = []
    treeindex=0
    inputFieldIndex=0
    method_Count = 0

    for i in range(len(udp_filter[k])):
        if i==int(method_Index):
            method_Count=method_Count+1
            continue

        if len(udp_filter[k][i]) == 1 and udp_filter[k][i][0] == ' ':
            toggleStateList.append('')

        elif len(udp_filter[k][i]) ==1 and (udp_filter[k][i][0] == 'Do_Selection_On_Tree' or udp_filter[k][i][0] == 'No_Selection_On_Tree'):
            treeindex=treeindex+1
            toggleStateList.append('')

        elif len(udp_filter[k][i]) ==1 and (udp_filter[k][i][0] == 'Input' or udp_filter[k][i][0] == 'No_Input'):
            inputFieldIndex = inputFieldIndex + 1
            toggleStateList.append('')

        else:
            equalOrNotEqual=udpScreenInstance.multiDropdown.getToggleStateInMultiDropDown(getHandle(setup, MRXConstants.DEPOPUP, "filterPopup"), (i - (method_Count+treeindex+inputFieldIndex)))
            toggleStateList.append(equalOrNotEqual)
            ##############
            if validateSearch:
                #valueBeforeSearch=udpScreenInstance.multiDropdown.doSearch(getHandle(setup,MRXConstants.DEPOPUP,"filterPopup"),'',(i-treeindex-inputFieldIndex))

                valueAfterSearch=udpScreenInstance.multiDropdown.doSearch(getHandle(setup, MRXConstants.DEPOPUP, "filterPopup"), MRXConstants.SearchValue, (i - (method_Count+treeindex+inputFieldIndex)))
                searchFlag=True
                for val in valueAfterSearch:
                   if not ((MRXConstants.SearchValue.lower() in val) or (MRXConstants.SearchValue.upper() in val) or ('All' in val)):
                        searchFlag=False
                        break
                checkEqualAssert(True,searchFlag,message='Validate that search is working fine in the apply filters diloag box on the Data Extraction screen for :' +tab_name+" :: Search Keyword ="+str(MRXConstants.SearchValue)+ " Search result :"+str(valueAfterSearch),testcase_id='')
            ##############

    return toggleStateList



# def createFilterMap(filters,keys):
#     return dict(zip(keys,filters))
#
# def parseFilters(global_filter):
#     filters = {}
#     for id in global_filter.keys():
#         filters[id] = parseFilter(id,global_filter)
#     return filters
#
# def parseFilter(id,global_filter):
#     flist = []
#     for f in global_filter[str(id)]['filters'].split("::"):
#         flist.append(str(f).split(','))
#     return flist


def setFilters(setup,udpScreenInstance,tab_name,method_Index,selectedMethod,methodNeeded,totalMethod,k ="0",validateAvailableMethod=False,toggleStateFlag=False):
    udp_filter= UDHelper.parseFilters(setup.cM.getNodeElements("deScreenFilters",tab_name))
    udpfilters= setup.cM.getNodeElements("udpfilters","filter")
    udpScreenInstance.clickLink(udpfilters[tab_name]['locatorText'], getHandle(setup, MRXConstants.DEPOPUP, MRXConstants.ALLLINKS))

    if validateAvailableMethod:
        availableMethodOnUI=udpScreenInstance.getAllTitle(getHandle(setup, MRXConstants.DEPOPUP,MRXConstants.ALLTITLES))
        checkEqualAssert(methodNeeded,availableMethodOnUI,message="Verify that for a selected method, in the corresponding data extraction window, user gets an option to apply filter on every other method except the selected method :: Selected Method = "+str(selectedMethod),testcase_id='MKR-1963')

    toggleStateList = []
    filterSelected = []
    treeindex=0
    inputFieldIndex=0
    method_Count=0
    global DictContainingTree

    for i in range(len(udp_filter[k])):

        if i==int(method_Index):
            method_Count=method_Count+1
            continue

        if len(udp_filter[k][i]) == 1 and udp_filter[k][i][0] == ' ':
            if toggleStateFlag:
                toggleStateList.append('')
            else:
                filterSelected.append([])

        elif len(udp_filter[k][i]) ==1 and udp_filter[k][i][0] == 'Do_Selection_On_Tree':
            treeHandle=getHandle(setup, MRXConstants.DEPOPUP, 'alltrees')
            udpScreenInstance.tree.expandTree(setup, treeHandle, index=treeindex)
            level_Dict = udpScreenInstance.tree.seprateElementOfTreeByLevel(treeHandle, index=treeindex)
            expectedFromUI, expected, selected = udpScreenInstance.tree.doSelectionOnTree_Random(setup, level_Dict,treeHandle, index=treeindex)
            DictContainingTree[totalMethod[i]]=selected
            checkEqualDict(expected,selected,message='Verify selection on Tree',doSortingBeforeCheck=True)
            treeindex=treeindex+1

            if toggleStateFlag:
                toggleStateList.append('')
            else:
                if expectedFromUI != ['']:
                    filterSelected.append([expectedFromUI])
                else:
                    filterSelected.append([])

        elif len(udp_filter[k][i]) ==1 and udp_filter[k][i][0] == 'No_Selection_On_Tree':
            treeindex = treeindex + 1
            if toggleStateFlag:
                toggleStateList.append('')
            else:
                filterSelected.append([])


        elif len(udp_filter[k][i]) ==1 and udp_filter[k][i][0] == 'Input':
            input_value=setup.cM.getNodeElements("deScreenFilters",tab_name)[k]['inputvalue']
            inputvalue=str(udpScreenInstance.cm.sendkeys_input(input_value, getHandle(setup, MRXConstants.DEPOPUP, 'allinputs'), inputFieldIndex+1))
            inputFieldIndex = inputFieldIndex + 1

            if toggleStateFlag:
                toggleStateList.append('')
            else:
                filterSelected.append(inputvalue.split(','))

        elif len(udp_filter[k][i]) == 1 and udp_filter[k][i][0] == 'No_Input':
            udpScreenInstance.cm.sendkeys_input("", getHandle(setup, MRXConstants.DEPOPUP, 'allinputs'), inputFieldIndex+1)
            inputFieldIndex = inputFieldIndex + 1
            if toggleStateFlag:
                toggleStateList.append('')
            else:
                filterSelected.append([])

        else:
            equalOrNotEqual=udpScreenInstance.multiDropdown.setEqualOrNotEqualIcon(getHandle(setup, MRXConstants.DEPOPUP, "filterPopup"), udp_filter[k][i], (i - (method_Count+treeindex+inputFieldIndex)))

            if 'E' in udp_filter[k][i]:
                checkEqualAssert('Equal',str(equalOrNotEqual),message='Verify selection For equalSign')
            elif 'NE' in udp_filter[k][i]:
                checkEqualAssert('Not Equal', str(equalOrNotEqual),message='Verify selection For equalSign')

            selected  = udpScreenInstance.multiDropdown.domultipleSelectionWithIndex(getHandle(setup, MRXConstants.DEPOPUP, "filterPopup"), udp_filter[k][i], (i - (method_Count+treeindex+inputFieldIndex)))

            if toggleStateFlag:
                toggleStateList.append(equalOrNotEqual)
            else:
                if selected != ['']:
                    filterSelected.append(selected)
                else:
                    filterSelected.append([])

    if toggleStateFlag:
        return toggleStateList
    else:
        return filterSelected


def getUDPFiltersToolTipData(screenName,setup,selectedMethod,parent="filterArea"):
    segment_Keys =setup.cM.getAllNodeElements("segmenntFilters","filter")
    device_Keys  = setup.cM.getAllNodeElements("deviceFilters","filter")
    network_Keys = setup.cM.getAllNodeElements("networkFilters","filter")
    content_Keys = setup.cM.getAllNodeElements("contentFilters","filter")
    usage_Keys = setup.cM.getAllNodeElements("usageFilters","filter")

    segmentKeys, methodIndexForSegment = del_Key_ForSelectedMethod(segment_Keys, selectedMethod)
    deviceKeys, methodIndexForDevice = del_Key_ForSelectedMethod(device_Keys, selectedMethod)
    networkKeys, methodIndexForNetwork = del_Key_ForSelectedMethod(network_Keys, selectedMethod)
    contentKeys, methodIndexForContent = del_Key_ForSelectedMethod(content_Keys, selectedMethod)
    usageKeys, methodIndexForUsage = del_Key_ForSelectedMethod(usage_Keys, selectedMethod)

    handle=getHandle(setup,screenName,parent)
    actualFilters = insertKeys(getToolTipData(setup,handle),segmentKeys+deviceKeys+networkKeys+contentKeys+usageKeys)
    return actualFilters


def insertKeys(dictionary,keys):
    if type(dictionary) == dict:
        for k in keys:
            if k not in dictionary.keys():
                dictionary[k] = []
        return dictionary
    else:
        return dictionary


def getToolTipData(setup, h, parent="filterArea", tooltip_parent = "globalfiltertooltip", child="filterText", screenName=MRXConstants.DEPOPUP, flag=True):
    try:
        logger.info("Performing Hover action on Filter text Area")
        if len(h[parent][child])>0:
            ActionChains(setup.d).move_to_element(h[parent][child][0]).perform()
            tooltipHandle = getHandle(setup,screenName,tooltip_parent)
            filters = getAllSelectedFilters(tooltipHandle,tooltip_parent,child,flag=flag)
            logger.info("Got Tooltip data = %s",str(filters))
            return filters
        else:
            logger.debug("No any Text Found For Hover")
            return {}
    except Exception as e:
        logger.error("Got Exception while getting tooltip data for Global Filters = %s",str(e))
        return e


def getAllSelectedFilters(h,parent="filterArea",child="filterText",flag=True):
    filters = {}
    try:
        if not h[parent][child]:
            filters = str(h[parent]['filter'][0].text)
            logger.info("Got Selected Filters as %s",filters)
        else:
            for ele in h[parent][child]:
                # sleep(2)
                if str(ele.text)!='':
                    if flag==True:
                        temp = []
                        # ele.send_keys(Keys.NULL)
                        uifilter = str(ele.text).split(': ')
                        if len(uifilter)==1:
                            filters[uifilter[0].strip().rstrip(':').strip()] = [str("").strip()]
                        else:
                            if '>' in uifilter[1]:
                                filters[uifilter[0].strip()]=[str(uifilter[1]).strip()]
                            else:
                                for s in uifilter[1].split(Delimiter):
                                    temp.append(s.strip())
                                filters[uifilter[0].strip()] = temp
                            # sleep(2)
                    else:
                        #for handling : and , for MRX Segment filter
                        key_value=(ele.text).split(':', 1)
                        try:
                            filters[str(key_value[0]).strip()] = [str(key_value[1]).strip()]
                        except Exception as e:
                            filters[str(key_value[0]).strip()] = [key_value[1].strip()]
                # sleep(2)
        return filters
    except Exception as e:
        return e


def measureAndDimensionAfterMapping(timeRangeFromScreen, measureFromScreen, selectedMethod, row_Count,screenTooltipData):
    query = {}
    query['measure'] = []
    selectedMethodDimension = ''
    measures = ConfigManager().getNodeElements("measure_Mapping", "measure")
    for k, measure in measures.iteritems():
        if str(k) == str(measureFromScreen):
            query['measure'].append(measure['backEnd_ID'])

    filters = ConfigManager().getNodeElements("filter_Mapping", "filter")
    for k, filter in filters.iteritems():
        if str(k) in screenTooltipData.keys() and screenTooltipData[k] != [] and str(screenTooltipData[k][0]).lower() != 'ALL'.lower():
            if str(k) in DictContainingTree.keys():
                keyList = str(filter['backEnd_ID']).split(',')
                for i in range(len(keyList)):
                    if str(i) in DictContainingTree[k].keys():
                        query[str(keyList[i]).strip()] = DictContainingTree[k][str(i)]
            else:
                query[filter['backEnd_ID']] = screenTooltipData[k]

        if str(k) == selectedMethod:
            selectedMethodDimension = filter['backEnd_ID']

    timeRange = timeRangeFromScreen.split(Constants.TimeRangeSpliter)

    if len(timeRange) == 1:
        startTime = str(str(timeRange[0]).strip().split('(')[0]).strip() + " 00:00"
        query['starttime'] = str(getepoch(startTime, tOffset=MRXConstants.TIMEZONEOFFSET))
        query['endtime'] = str(getepoch(startTime, tOffset=MRXConstants.TIMEZONEOFFSET) + 86400)
    else:

        if len(str(timeRange[0]).strip().split(' ')) == 3:
            query['starttime'] = str(
                getepoch(str(timeRange[0]).strip() + " 00:00", tOffset=MRXConstants.TIMEZONEOFFSET))
        else:
            query['starttime'] = str(getepoch(str(timeRange[0]).strip(), tOffset=MRXConstants.TIMEZONEOFFSET))

        if len(str(str(timeRange[1]).strip().split('(')[0]).strip().split(' ')) == 3:
            query['endtime'] = str(getepoch(str(str(timeRange[1]).strip().split('(')[0]).strip() + " 00:00",tOffset=MRXConstants.TIMEZONEOFFSET) + 86400)
        else:
            query['endtime'] = str(
                getepoch(str(str(timeRange[1]).strip().split('(')[0]).strip(), tOffset=MRXConstants.TIMEZONEOFFSET))

    query['dimension'] = [selectedMethodDimension]
    query['count'] = row_Count
    return query

def mapForTableHeader(header):
    new_Header=deepcopy(header)
    measures = ConfigManager().getNodeElements("measure_Mapping", "measure")
    filters = ConfigManager().getNodeElements("filter_Mapping", "filter")

    for i in range(len(header)):
        if header[i] in filters.keys():
            new_Header[i] = filters[header[i]]['backEnd_ID']

        if header[i] in measures.keys():
            new_Header[i] = measures[header[i]]['backEnd_ID']

    logger.info("Table header before map :: %s ,after map :: %s ",str(header),str(new_Header))
    return new_Header


def fireBV(query,method,table_name,header,data,testcase=''):
    sleep(1)
    dump_header=mapForTableHeader(header)
    query['method']=method
    query['table_name']=table_name
    query['data']=data
    query['testcase']=testcase
    query['table_header']=dump_header
    import time
    query['id']=str(time.time()).split('.')[0]

    logger.info("Going to dump info from UI for Backend Data validation ::" + str(query))
    with open("DE_DumpFile.txt",mode='a') as fs:
        fs.write(json.dumps(query))
        fs.write(" __DONE__" + "\n")




def getCSVData(selectedMethod,testcase=''):
    file=[]
    t=0
    while(t<30):
        file=filesAtGivenPath(Constants.chromdownloadpath)
        if len(file)>0:
            break
        else:
            time.sleep(1)
        t=t+1

    f_data = []
    header = []
    data = []

    checkEqualAssert(1,len(file),message="Verify that data extraction works correctly (Functionally) for  = "+str(selectedMethod),testcase_id=testcase)
    if len(file)==1:
        for f in file:
            with open(f) as fa:
                f_data = fa.readlines()

        for i in range(len(f_data)):
            row_data = []
            if i == 0:
                header = f_data[i].split(',')
                header[len(header) - 1] = str(header[len(header) - 1]).strip('\n')
            else:
                row_data = f_data[i].split(',')
                row_data[len(row_data) - 1] = str(row_data[len(row_data) - 1]).strip('\n')
                data.append(row_data)
    else:
        logger.info('Number of file at given path is more then 1 :: check manually')
    removeFileAtGivenPath(Constants.chromdownloadpath)
    return header,data

# def availableQuickLink(setup,screenName,parent='ktrs',child='a',childForCustomClick='datepicker'):
#     availableQuickLinkList = []
#     h=getHandle(setup, screenName, parent)
#     for ele in h[parent][child]:
#         if not 'disable' in ele.get_attribute('class').lower():
#             availableQuickLinkList.append(str(ele.text))
#     if h[parent][childForCustomClick][0].is_enabled():
#         availableQuickLinkList.append('Calender')
#
#     return availableQuickLinkList
#
#
# def availableMeasure(setup,screenName,index=0,parent='allselects',child='select'):
#     availableMeasureList=[]
#     h=getHandle(setup,screenName,parent)
#     if len(h[parent][child]) > index:
#         for ele in h[parent][child][index].find_elements_by_tag_name('option'):
#             availableMeasureList.append(str(ele.text).strip())
#     return availableMeasureList


