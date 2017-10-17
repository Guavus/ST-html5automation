from MuralUtils.ContentHelper import *
from MRXUtils import MRX_UMHelper
from classes.Pages.MuralScreens.UserMangementScreen import *
from classes.Pages.ExplorePageClass import *
from MRXUtils.MRXConstants import *

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    exploreScreenInstance.exploreList.switchApp(exploreHandle)
    userScreenInstance = UserManagementScreenClass(setup.d)
    result = exploreScreenInstance.exploreList.launchapp(getHandle(setup, "explore_Screen"), 1)
    checkEqualAssert(True, result, message="Checking the launching of User Management")
    isError(setup)
    setup.d.switch_to.window(setup.d.window_handles[1])

    usersDetails = setup.cM.getNodeElements("userdetail", "user")
    tableHandle = getHandle(setup, MRXConstants.MRXUMSCREEN, 'table')
    tableMap = userScreenInstance.table.getTableDataMap(tableHandle, driver=setup,colIndex=1)
    setup.d.close()
    setup.d.switch_to.window(setup.d.window_handles[0])

    clickOnProfileIconFlag=True
    for k, usersDetail in usersDetails.iteritems():
        if tableMap['rows'].has_key(usersDetail['username']):
            logger.info("Going to login with User :: %s",str(usersDetail['username']))

            if clickOnProfileIconFlag:
                exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup,MRXConstants.ExploreScreen,'appHeader'), icon='profile')
                clickFlag=exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen,'appHeader'),MuralConstants.Logout)

            login(setup, usersDetail['username'], usersDetail['password'])
            flag, msg = isError(setup)
            if usersDetail['enabled']=="0":
                logger.debug("User is not enabled so not able to login")
                checkEqualAssert(MRXConstants.Accese_Denied_Msg,str(msg).strip(),"Verify Disabled user can't login and also verify Msg on Error Popup",testcase_id="MKR-3492")
                clickOnProfileIconFlag=False
                continue
            else:
                if not flag:
                    currentLoginUser=exploreScreenInstance.exploreList.getUserNameFromHeader(getHandle(setup, MRXConstants.ExploreScreen,'appHeader'))
                    expectedUser=usersDetail['firstname']+" "+usersDetail['lastname']
                    checkEqualAssert(expectedUser,currentLoginUser,message="Verify New User login successfully")
                    if k=='admin':
                        switchFlag,screen_module=MRX_UMHelper.checkUMSwitchForUser(setup,exploreScreenInstance,wfstart,True)
                        checkEqualAssert(True,switchFlag,message="Verify that only the admin user can go to the User Management screen from all the screens",testcase_id="MKR-3475")
                    elif k in ['appuser','segmentmanager']:
                        switchFlag, screen_module = MRX_UMHelper.checkUMSwitchForUser(setup,exploreScreenInstance,wfstart,False)
                        checkEqualAssert(True,switchFlag,message="Verify that for the segment manager and standard user user management tab is disable",testcase_id="MKR-3476")
                        if k=='appuser':
                            checkEqualAssert(True, switchFlag,message="Verify that for the standard user 'User management' tab is disable",testcase_id="MKR-3495")
                            exploreScreenInstance.exploreList.launchModule(getHandle(setup, MRXConstants.ExploreScreen),"SEGMENTS")
                            button_status = userScreenInstance.cm.isButtonEnabled('Import',getHandle(setup,MRXConstants.SEGMENTSCREEN,"allbuttons"))
                            checkEqualAssert(False,button_status,message="Verify that standard user cannot be able to import any segment",testcase_id="MKR-3496")
                            button_status = userScreenInstance.cm.isButtonEnabled('Export', getHandle(setup,MRXConstants.SEGMENTSCREEN,"allbuttons"))
                            checkEqualAssert(False,button_status,message="Verify that standard user cannot be able to export any segment",testcase_id="MKR-3496")
                        else:
                            checkEqualAssert(True, switchFlag,message="Verify that for the segment manager 'User management' tab is disable",testcase_id="MKR-3494")

                        try:
                            setup.d.execute_script('window.open("about:blank", "_blank");')
                            setup.d.switch_to.window(setup.d.window_handles[1])
                            setup.d.get(Constants.MRX_UM_URL)
                            errFlag, errMsg = isError(setup)

                            if k=='segmentmanager':
                                checkEqualAssert(True, errFlag,message="URL of User management not open with that current session for Segment Manager",testcase_id="MKR-3477,MKR-3494")
                            else:
                                checkEqualAssert(True, errFlag,message="URL of User management not open with that current session for App User :: Userrole ="+str(k),testcase_id="MKR-3495")

                            if errFlag:
                                checkEqualAssert(MRXConstants.Accese_Denied_Msg,errMsg,message="Verify Access denied Msg on Popup")
                            setup.d.close()
                            setup.d.switch_to.window(setup.d.window_handles[0])

                        except Exception as e:
                            logger.error("************Not able to open new tab********* Skipping last step for testcase (MKR-3494,MKR-3495,MKR-3477) :: URL of User management not open with that current session for user other then admin ")
                            resultlogger.error("************Not able to open new tab********* Skipping last step for testcase (MKR-3494,MKR-3495,MKR-3477) :: URL of User management not open with that current session for user other then admin <br>")
                            if len(setup.d.window_handles)>1:
                                setup.d.close()
                                setup.d.switch_to.window(setup.d.window_handles[0])
                    clickOnProfileIconFlag=True
                else:
                    logger.error("************User is not able to login :: Check Manually**********************")
                    resultlogger.error("**************************User is not able to login :: Check Manually **************************<br>")
                    clickOnProfileIconFlag = False

        else:
            if usersDetail['button']!="Cancel":
                logger.debug("User = %s not exist in Table :: Check Manually",str(usersDetail['username']))

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()

