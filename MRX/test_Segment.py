import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MRXScreens.SegmentScreenClass import *
from MRXUtils.MRXConstants import *
from MRXUtils import SegmentHelper
import os

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    segmentScreenInstance = SegmentScreenClass(setup.d)
    segmentScreenHandle = getHandle(setup,MRXConstants.SEGMENTSCREEN,'allbuttons')
    segmentDetails=setup.cM.getNodeElements("segmentDetails","segment")

    ##################################### Blank Segment Name scenario ##################################################
    segmentScreenInstance.cm.clickButton("Import", segmentScreenHandle)
    popUpHandle = getHandle(setup, MRXConstants.POPUPSCREEN)
    segmentScreenInstance.cm.sendkeys_input(' ', popUpHandle, 0)
    fileDir = find_realPath('segment_sample.csv')
    popUpHandle['browsebuttons']['browsebutton'][0].find_elements_by_xpath('./*/*')[0].send_keys(str(fileDir))
    button_Status=segmentScreenInstance.cm.isButtonEnabled('Import', getHandle(setup, MRXConstants.POPUPSCREEN, "allbuttons"))
    checkEqualAssert(False,button_Status,message='Verify that a user is not allowed to enter an empty segment name',testcase_id='MKR-1696')
    segmentScreenInstance.cm.clickButton('Cancel', popUpHandle)
    ###################################### Error out segment can not be used ###########################################
    segmentScreenInstance.cm.clickButton("Import", segmentScreenHandle)
    popUpHandle1 = getHandle(setup, MRXConstants.POPUPSCREEN)
    segmentScreenInstance.cm.sendkeys_input('MKR1740', popUpHandle1, 0)
    fileDir1 = find_realPath('abc.pdf')
    popUpHandle1['browsebuttons']['browsebutton'][0].find_elements_by_xpath('./*/*')[0].send_keys(str(fileDir1))
    checkEqualAssert(True, 'Incorrect file selected' in str(popUpHandle1['footerText']['text'][0].text),message=" An error out segment can not be used",testcase_id='MKR-1740')
    button_Status = segmentScreenInstance.cm.isButtonEnabled('Import',getHandle(setup, MRXConstants.POPUPSCREEN, "allbuttons"))
    checkEqualAssert(False, button_Status, message='An error out segment can not be used (Import Button should be disable)',testcase_id='MKR-1740')
    segmentScreenInstance.cm.clickButton('Cancel', popUpHandle1)

    ########################################For same Segment Name Functionality ########################################
    segmentScreenInstance.cm.clickButton("Import", segmentScreenHandle)
    popUpHandle = getHandle(setup, MRXConstants.POPUPSCREEN)
    segmentScreenInstance.cm.sendkeys_input('autoSegment', popUpHandle, 0)
    fileDir = find_realPath('segment_sample.csv')
    popUpHandle['browsebuttons']['browsebutton'][0].find_elements_by_xpath('./*/*')[0].send_keys(str(fileDir))
    button_Status = segmentScreenInstance.cm.isButtonEnabled('Import',getHandle(setup, MRXConstants.POPUPSCREEN, "allbuttons"))
    if button_Status:
        segmentScreenInstance.cm.clickButton('Import', getHandle(setup, MRXConstants.POPUPSCREEN, "allbuttons"))
        segmentScreenInstance.cm.clickButton("Import", segmentScreenHandle)
        popUpHandle = getHandle(setup, MRXConstants.POPUPSCREEN)
        segmentScreenInstance.cm.sendkeys_input('autoSegment', popUpHandle, 0)
        fileDir = find_realPath('segment_sample.csv')
        popUpHandle['browsebuttons']['browsebutton'][0].find_elements_by_xpath('./*/*')[0].send_keys(str(fileDir))
        button_Status = segmentScreenInstance.cm.isButtonEnabled('Import',getHandle(setup, MRXConstants.POPUPSCREEN, "allbuttons"))
        if button_Status:
            msg=''
            segmentScreenInstance.cm.clickButton('Import', popUpHandle)
            popUpHandle = getHandle(setup, MRXConstants.POPUPSCREEN)
            for ele in popUpHandle['allspans']['span']:
                if 'red' in str(ele.get_attribute('style')).lower():
                    msg=str(ele.text)
                    break
            button_Status = segmentScreenInstance.cm.isButtonEnabled('Import',getHandle(setup, MRXConstants.POPUPSCREEN,"allbuttons"))
            checkEqualAssert(False,button_Status,message="Segment with same name can't Import")
            checkEqualAssert(MRXConstants.MSGFORSAMESEGMENT.strip(),msg.strip(),message="Verify Message during import Segment with same name")
        segmentScreenInstance.cm.clickButton('Cancel', getHandle(setup, MRXConstants.POPUPSCREEN, "allbuttons"))
    else:
        segmentScreenInstance.cm.clickButton('Cancel', getHandle(setup, MRXConstants.POPUPSCREEN, "allbuttons"))

    setup.d.close()

    import MRX.DeleteSegment

    ####################################################################################################################

    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    segmentScreenInstance = SegmentScreenClass(setup.d)
    segmentScreenHandle = getHandle(setup,MRXConstants.SEGMENTSCREEN,'allbuttons')
    segmentDetails=setup.cM.getNodeElements("segmentDetails","segment")

    flag_Top_segment=True
    for k, segmentDetail in segmentDetails.iteritems():
        segmentScreenInstance.cm.clickButton("Import", segmentScreenHandle)
        try:
            segmentDetailFromUIPopup=SegmentHelper.importSegment(setup,segmentScreenInstance,segmentDetail)
            SegmentHelper.refreshSegmentScreen(segmentScreenInstance,setup)
            if flag_Top_segment:
                tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN,'table')
                data2 = segmentScreenInstance.table.getTableData1(tableHandle)
                checkEqualAssert(segmentDetail['segmentname'],str(data2['rows'][0][0]),message='Verify New added segment at Top when table sorted on \'Created on\' Column (Default)',testcase_id='MKR-1665')
                flag_Top_segment=False

        except:
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.debug("Got Exception because of invalid entry for Segment :: Screenshot with name = %s is saved", r)
            resultlogger.debug("Got Exception because of invalid entry for Segment:: Screenshot with name = %s is saved", r)
            getHandle(setup, MRXConstants.POPUPSCREEN,'icons')['icons']['closePopupIcon'][0].click()
            continue

        tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN,'table')
        tableMap = segmentScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
        if segmentDetail['button'] == 'Cancel':
            checkEqualAssert(False,tableMap['rows'].has_key(segmentDetail['segmentname']),"","","Verify that if cancel button is pressed then the segment does not get created",testcase_id='MKR-1704')
        if segmentDetail['button']=='Import' and len(segmentDetailFromUIPopup)>0:
            checkEqualAssert(True,tableMap['rows'].has_key(segmentDetail['segmentname']),"","","Verify Segment added Successfully With Detail= "+str(segmentDetailFromUIPopup),testcase_id='MKR-1703')
            tableMap['rows'][segmentDetail['segmentname']].pop()
            tableMap['rows'][segmentDetail['segmentname']].pop()

            createdon_from_table=tableMap['rows'][segmentDetail['segmentname']].pop()
            createdon_from_UI=segmentDetailFromUIPopup.pop()
            checkEqualAssert(str(createdon_from_UI.split(":")[0]).strip(),str(createdon_from_table.split(':')[0]).strip(),'','','Verify Created on from UI..... Expected ='+createdon_from_UI+' Actual ='+createdon_from_table,testcase_id='MKR-1703')

            checkEqualAssert(tableMap['rows'][segmentDetail['segmentname']], segmentDetailFromUIPopup, "", "","Verify Segment Detail From table (if Status is Running, check manually (We already wait for 10 sec)), Details ="+str(segmentDetailFromUIPopup),testcase_id='MKR-1661,1663,1671')

    # Basic Table Functionality

    SegmentHelper.VerifyBasicTableFuncationality(setup,segmentScreenInstance)
    setup.d.close()

    import MRX.EditSegment
    import MRX.SegmentFilter
    import MRX.Filterscenario
    #import MRX.DeleteSegment
    import MRX.MultiWindowFunctionality


except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()


