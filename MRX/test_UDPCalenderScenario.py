from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from Utils.SetUp import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper
import random

def launchCalendar(setup,Page,parent='ktrs',child='datepicker',index=0):
    calHandler = getHandle(setup, Page,parent)
    logger.info("Launching Calendar: ")
    calHandler[parent][child][index].click()
    logger.info("Calendar picker is clicked")

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "WORKFLOWS")
    udScreenInstance.wfstart.launchScreen("Distribution", getHandle(setup, MRXConstants.WFSCREEN))
    time.sleep(5)

    launchCalendar(setup, MRXConstants.UDSCREEN)

    st = ConfigManager().getNodeElements("availabletimerange", "starttime")[str(0)]
    et = ConfigManager().getNodeElements("availabletimerange", "endtime")[str(0)]

    stime = Time(st['year'], st['month'], st['day'], st['hour'], st['min'])
    etime = Time(et['year'], et['month'], et['day'], et['hour'], et['min'])

    stepoch = getepoch(stime.datestring, MRXConstants.TIMEZONEOFFSET, "%Y-%m-%d %H:%M")
    etepoch = getepoch(etime.datestring, MRXConstants.TIMEZONEOFFSET, "%Y-%m-%d %H:%M")

    dateStringStart = getDateString(stepoch-86400, tOffset=MRXConstants.TIMEZONEOFFSET,tPattern='%Y %B %d %H %M').split(' ')
    Flag=isDateDisabled(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4],udScreenInstance, setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

    checkEqualAssert(True,Flag,message='Verify Past date disable on Calendar',testcase_id='MKR-3190')

    dateStringStart = getDateString(etepoch + 86400, tOffset=MRXConstants.TIMEZONEOFFSET,tPattern='%Y %B %d %H %M').split(' ')
    Flag_1=isDateDisabled(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4],udScreenInstance, setup, page=Constants.CALENDERPOPUP, parent="rightcalendar")

    checkEqualAssert(True,Flag_1, message='Verify Future date disable on Calendar',testcase_id='MKR-3190')

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()