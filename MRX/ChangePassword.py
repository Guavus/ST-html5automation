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
    userScreenInstance = UserManagementScreenClass(setup.d)

    usersDetails = setup.cM.getNodeElements("changePasswordScenario", "user")
    clickOnProfileIconFlag = True
    checkCancelOnChangePopup=True

    for k, usersDetail in usersDetails.iteritems():
        if usersDetail['enabled'] != "0" and usersDetail['button']=='Create':
            currentLoginUser = ''
            expectedUser = usersDetail['firstname'] + " " + usersDetail['lastname']

            if clickOnProfileIconFlag:
                exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),icon='profile')
                clickFlag = exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'), MuralConstants.Logout)

            login(setup, usersDetail['username'], usersDetail['password'])
            flag,msg=isError(setup)
            if flag:
                logger.error("Not able to login :: hence skipping TestCase for Change Password")
                resultlogger.error("Not able to login :: hence skipping TestCase for Change Password <br>")
                continue

            exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),icon='profile')
            exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'), MRXConstants.ChangePassword)
            change_password_screen_handle = getHandle(setup, MRXConstants.ChangePasswordScreen)

            if checkCancelOnChangePopup:
                MRX_UMHelper.ChangePassword(setup, userScreenInstance,MRXConstants.ChangePasswordScreen,change_password_screen_handle, usersDetail,button="Cancel")
                exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),icon='profile')
                exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'), MuralConstants.Logout)
                login(setup, usersDetail['username'], usersDetail['password'])
                errFlag,errMsg=isError(setup)
                if not errFlag:
                    currentLoginUser = exploreScreenInstance.exploreList.getUserNameFromHeader(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'))
                    checkEqualAssert(expectedUser,currentLoginUser,message="Verfiy Cancel button functionality on Change Password Popup (by login with old password)")
                    clickOnProfileIconFlag = True
                else:
                    logger.error("Not able to login with user credential = %s / %s", str(usersDetail['username']),str(usersDetail['password']))
                    resultlogger.error("Not able to login with user credential = %s / %s <br>", str(usersDetail['username']),str(usersDetail['password']))
                    clickOnProfileIconFlag = False
                    continue

                exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),icon='profile')
                exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'), MRXConstants.ChangePassword)
                change_password_screen_handle = getHandle(setup, MRXConstants.ChangePasswordScreen)
                checkCancelOnChangePopup=False

            errorMsg, flag = MRX_UMHelper.ChangePassword(setup, userScreenInstance, MRXConstants.ChangePasswordScreen,change_password_screen_handle,usersDetail, button="Change")

            if flag:
                login(setup, usersDetail['username'], usersDetail['newcpassword'])
                errFlag,msg=isError(setup)
                if not errFlag:
                    currentLoginUser = exploreScreenInstance.exploreList.getUserNameFromHeader(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'))
                    checkEqualAssert(expectedUser, currentLoginUser,message="Verfiy user login with new password (Change Password Functionality)")
                    clickOnProfileIconFlag=True
                else:
                    checkEqualAssert(expectedUser, currentLoginUser,message="Verfiy user login with new password (Change Password Functionality)")
                    logger.error("Not able to login with user credential = %s / %s", str(usersDetail['username']),str(usersDetail['newcpassword']))
                    clickOnProfileIconFlag = False
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()