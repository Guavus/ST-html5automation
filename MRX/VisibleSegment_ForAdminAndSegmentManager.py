from MuralUtils.ContentHelper import *
from MRXUtils import SegmentHelper
from classes.Pages.MuralScreens.UserMangementScreen import *
from classes.Pages.MRXScreens.SegmentScreenClass import *
from classes.Pages.ExplorePageClass import *
from MRXUtils.MRXConstants import *


################################# Importing Segment with different user credentials ####################################
try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    exploreScreenInstance = ExplorePageClass(setup.d)
    segmentScreenInstance = SegmentScreenClass(setup.d)
    userScreenInstance = UserManagementScreenClass(setup.d)

    usersDetails = setup.cM.getNodeElements("userdetail", "user")
    segmentDetails = setup.cM.getNodeElements("importSegmentDetailsForUM", "segment")

    for k, usersDetail in usersDetails.iteritems():
        if k in ['admin','segmentmanager']:
            exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),icon='profile')
            clickFlag = exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'), MuralConstants.Logout)
            login(setup, usersDetail['username'], usersDetail['password'])
            flag, msg = isError(setup)

            if k == 'admin' and usersDetail['enabled']!="0":
                exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
                exploreScreenInstance.exploreList.switchApp(exploreHandle)
                exploreScreenInstance.exploreList.launchapp(getHandle(setup, "explore_Screen"), 1)
                isError(setup)
                setup.d.switch_to.window(setup.d.window_handles[1])

                tableHandle = getHandle(setup, MRXConstants.MRXUMSCREEN, 'table')
                tableMap = userScreenInstance.table.getTableDataMap(tableHandle, driver=setup, colIndex=1)

                allUserVisibleToAdmin=True
                for key, checkusers in usersDetails.iteritems():
                    if checkusers['button'] == "Create":
                        if not tableMap['rows'].has_key(checkusers['username']):
                            allUserVisibleToAdmin=False
                            break
                checkEqualAssert(True,allUserVisibleToAdmin,message="Verify that admin user can list all the users.",testcase_id="MKR-3489")
                setup.d.close()
                setup.d.switch_to.window(setup.d.window_handles[0])

            exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
            exploreScreenInstance.exploreList.launchModule(exploreHandle,"SEGMENTS")
            for key in segmentDetails.keys():
                if k in key:
                    userScreenInstance.cm.clickButton("Import", getHandle(setup, MRXConstants.SEGMENTSCREEN, 'allbuttons'))
                    segmentDetailFromUIPopup = SegmentHelper.importSegment(setup,segmentScreenInstance,segmentDetails[key])

    setup.d.close()

################################# Checking Visible Segment with different user credentials #############################

    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    exploreScreenInstance = ExplorePageClass(setup.d)
    segmentScreenInstance = SegmentScreenClass(setup.d)
    userScreenInstance = UserManagementScreenClass(setup.d)

    usersDetails = setup.cM.getNodeElements("userdetail", "user")
    segmentDetails = setup.cM.getNodeElements("importSegmentDetailsForUM", "segment")

    for k, usersDetail in usersDetails.iteritems():
        if k in ['admin', 'segmentmanager']:
            exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),icon='profile')
            clickFlag = exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'), MuralConstants.Logout)
            login(setup, usersDetail['username'], usersDetail['password'])
            flag, msg = isError(setup)

            exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
            exploreScreenInstance.exploreList.launchModule(exploreHandle,"SEGMENTS")
            tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
            tableMap = segmentScreenInstance.table.getTableDataMap(tableHandle, driver=setup)

            for key in segmentDetails.keys():
                if k in key or 'Shared' in key:
                    checkEqualAssert(True,tableMap['rows'].has_key(segmentDetails[key]['segmentname']),message="Login User can see own segment as well as shared segment from other user :: Segment Name="+str(segmentDetails[key]['segmentname']),testcase_id='MKR-3526')
                elif (not k in key) and ("Private" in key):
                    checkEqualAssert(False, tableMap['rows'].has_key(segmentDetails[key]['segmentname']),message="Login User can't see  Private segment of other user :: Segment Name=" + str(segmentDetails[key]['segmentname']), testcase_id='MKR-3526')

    setup.d.close()

################################# Deleting Segments ####################################################################

    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    exploreScreenInstance = ExplorePageClass(setup.d)
    segmentScreenInstance = SegmentScreenClass(setup.d)
    userScreenInstance = UserManagementScreenClass(setup.d)

    usersDetails = setup.cM.getNodeElements("userdetail", "user")
    segmentDetails = setup.cM.getNodeElements("importSegmentDetailsForUM", "segment")

    for k, usersDetail in usersDetails.iteritems():
        if k in ['admin', 'segmentmanager']:
            exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),icon='profile')
            clickFlag = exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'), MuralConstants.Logout)
            login(setup, usersDetail['username'], usersDetail['password'])
            flag, msg = isError(setup)

            exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
            exploreScreenInstance.exploreList.launchModule(exploreHandle,"SEGMENTS")

            for key in segmentDetails.keys():
                tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
                tableMap = segmentScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
                if k in key and tableMap['rows'].has_key(segmentDetails[key]['segmentname']):
                    deleteFlag = segmentScreenInstance.table.clickIconOnTableThroughTableHandle(tableHandle,setup.d,str(segmentDetails[key]['segmentname']))
                    if deleteFlag:
                        confirmPopup = confirm_Popup(setup, str(segmentDetails[key]['segmentname']))
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved <br>", r)
    setup.d.close()
