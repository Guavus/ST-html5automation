from MuralUtils.ContentHelper import *
from UMUtils import UMHelper
from classes.Pages.MuralScreens.RoleManagementScreen import *
from classes.Pages.ExplorePageClass import *
#from MRXUtils.MRXConstants import *
from UMUtils.UMConstants import *
from classes.Pages.MuralScreens.UserMangementScreen import UserManagementScreenClass

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    isError(setup)
    wfstart = WorkflowStartComponentClass()
    userScreenInstance = UserManagementScreenClass(setup.d)
    roleScreenInstance=RoleManagementScreenClass(setup.d)




    manageRoles_NegativeScenariosDict = setup.cM.getNodeElements("manageRoleScenarios_Negative", "scenario")
    manageRoles_NegativeScenariosDict_intKeys = {int(key): value for key, value in manageRoles_NegativeScenariosDict.items()}
    userLoginDetailsForManageRolesDict = setup.cM.getNodeElements("umUserLoginDetailsForManageRoles", "user")
    for k, manageRolesNegativeScenario in sorted(manageRoles_NegativeScenariosDict_intKeys.iteritems()):
        #k = "0"  #****************** To be removed
        #manageRolesNegativeScenario = manageRoles_NegativeScenariosDict[str(k)]  #****************** To be removed


        logger.info("Executing Scenario id ---> " + str(k))
        actionUser = manageRoles_NegativeScenariosDict[str(k)]['actionuser']
        actionUser_Name = userLoginDetailsForManageRolesDict[actionUser]['name']
        actionUser_Username = userLoginDetailsForManageRolesDict[actionUser]['username']
        actionUser_Password = userLoginDetailsForManageRolesDict[actionUser]['password']
        handle = getHandle(setup, "explore_Screen", "alllinks")
        if len(handle['alllinks']['a']) > 0:
            parentLoggedInUser_Name = str(handle['alllinks']['a'][0].text)

            if actionUser_Name != parentLoggedInUser_Name:
                userScreenInstance.click(handle['alllinks']['a'][0])  ## Click on Profile link
                handle = getHandle(setup, "explore_Screen", "alllinks")
                userScreenInstance.click(handle['alllinks']['a'][2])  ## Click on Logout
                time.sleep(5)
                username = actionUser_Username
                password = actionUser_Password
                if actionUser == 'superadmin':
                    logger.info("Logging in with superadmin user : '" + actionUser_Name)
                    login(setup, username, password)
                    parentLoggedInUser_Name = actionUser_Name
                elif "adminuser" in actionUser:
                    logger.info("Logging in with some admin user : '" + actionUser_Name)
                    login(setup, username, password)
                    parentLoggedInUser_Name = actionUser_Name
                elif "normaluser" in actionUser:
                    logger.info("Logging in with some normal user : '" + actionUser_Name)
                    login(setup, username, password)
                    erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR, parent='ErrorMsg',child='msg')
                    if erroFlag:
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'allbuttons')
                        roleScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                        time.sleep(5)
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
                    parentLoggedInUser_Name = ""

        else:
            logger.info("Logging in with user : '" + actionUser_Name)
            login(setup, actionUser_Username, actionUser_Password)



        if parentLoggedInUser_Name != "":

            if manageRoles_NegativeScenariosDict[str(k)]['operation'] == "multiple_loggedIn_tabs" :
                handle = getHandle(setup, "explore_Screen", "alllabels")
                userScreenInstance.click(handle['alllabels']['label'][1])

                setup.d.execute_script("window.open('"+Constants.URL+"','_blank');")
                setup.d.switch_to.window(setup.d.window_handles[1])
                handle = getHandle(setup, "explore_Screen", "alllinks")
                userScreenInstance.click(handle['alllinks']['a'][0])  ## Click on Profile link
                handle = getHandle(setup, "explore_Screen", "alllinks")
                userScreenInstance.click(handle['alllinks']['a'][2])  ## Click on Logout
                time.sleep(5)
                setup.d.execute_script("window.close()")

                setup.d.switch_to.window(setup.d.window_handles[0])
                handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
                click_status = UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES,parent='newRoleIcon', child='icon')

                erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR, parent='ErrorMsg', child='msg')
                checkEqualAssert(UMConstants.SESSION_EXPIRED_MSG, msgFromUI,message=" Verify that a session expire msg appears on all other windows when same user is logged in multiple windows of the same browser  and suddenly user logs out from one of the windows.",testcase_id='Reflex-UM-199')

                if erroFlag:
                    handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'allbuttons')
                    roleScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                    time.sleep(5)
                    handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
                    loginHandle = getHandle(setup,Constants.LOGINSCREEN)
                    checkEqualAssert(str([0,True]), str([len(handle['ErrorMsg']['msg']), len(loginHandle['username']['username']) > 0]),message="Verify that on clicking on 'Ok' button, Session Expire Error Popup disappears and login page is rendered again",testcase_id='Reflex-UM-199')










            ################### Verify that a valid error popup appears on session timeout
            if manageRoles_NegativeScenariosDict[str(k)]['operation'] == "session_timeout":
                handle = getHandle(setup, "explore_Screen", "alllabels")
                userScreenInstance.click(handle['alllabels']['label'][1])

                time.sleep(Constants.SESSION_TIMEOUT)

                handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
                click_status = UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES,parent='newRoleIcon', child='icon')

                erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR, parent='ErrorMsg',child='msg')
                checkEqualAssert(UMConstants.SESSION_EXPIRED_MSG, msgFromUI,message="Verify that a valid error popup appears on session timeout ",testcase_id='Reflex-UM-198')

                if erroFlag:
                    handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'allbuttons')
                    roleScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                    time.sleep(5)
                    handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
                    loginHandle = getHandle(setup, Constants.LOGINSCREEN)
                    checkEqualAssert(str([0, True]),str([len(handle['ErrorMsg']['msg']), len(loginHandle['username']['username']) > 0]),message="Verify that on clicking on 'Ok' button, Session Expire Error Popup disappears and login page is rendered again",testcase_id='Reflex-UM-198')














            ################### Verify handling for disabled Edit icon under Manage Users table
            if manageRoles_NegativeScenariosDict[str(k)]['operation'] == "enable_disabled_userEdit":
                handle = getHandle(setup, "explore_Screen", "alllabels")
                userScreenInstance.click(handle['alllabels']['label'][0])

                targetUser_Username = userLoginDetailsForManageRolesDict['superadmin']['username']
                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEUSERS, 'table')

                elem_edit = UMHelper.enable_DisabledIcons(setup=setup, tableHandle=tableHandle, screenInstance=userScreenInstance, valueUnderAction=targetUser_Username,tableHeader_text="Edit",colIndex=1)
                edit_click_status = userScreenInstance.click(elem_edit)

                if edit_click_status == True:
                    handle = getHandle(setup, UMConstants.UMPOPUP_ADDUSER, 'allinputs')
                    if handle['allinputs']['input'][1].is_enabled():
                        userScreenInstance.cm.sendkeys_input(manageRolesNegativeScenario['firstname'], handle, 1)

                        updatePassword_elem = getHandle(setup, UMConstants.UMPOPUP_ADDUSER, 'allinputs')['allinputs']['updatePwd'][0]
                        if "disable" in updatePassword_elem.get_attribute('class').lower():
                            setup.d.execute_script("arguments[0].classList.remove('disabledElement');", updatePassword_elem)
                            userScreenInstance.click(updatePassword_elem)
                            handle = getHandle(setup, UMConstants.UMPOPUP_ADDUSER, 'allinputs')
                            if handle['allinputs']['password'][0].is_enabled():
                                newPassword = str(userScreenInstance.cm.sendkeys_input(manageRolesNegativeScenario['newpassword'], handle, 0,child='password'))
                            if handle['allinputs']['password'][1].is_enabled():
                                newCpassword = str(userScreenInstance.cm.sendkeys_input(manageRolesNegativeScenario['newcpassword'],handle, 1, child='password'))






                    updateBtn_status = UMHelper.dumpResultForButton(True, "Edit user '" + str(targetUser_Username) + "' after enabling disabled edit button under manage users table", button_label="Update", screenInstance=userScreenInstance,setup=setup, screen=UMConstants.UMPOPUP_ADDUSER, testcase_id='')

                    erroFlag = False
                    if updateBtn_status:
                        userScreenInstance.hoverAndClickButton(setup, "Update", getHandle(setup, UMConstants.UMPOPUP_ADDUSER, 'allbuttons'))
                        erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR, parent='ErrorMsg',child='msg')
                    checkEqualAssert(UMConstants.MALACIOUS_USER_ERROR_MSG, str(msgFromUI),message="Verify that user '" +str(actionUser_Username)+"' gets an error popup on trying  updating his own details (Firstname , Password) by falsely enabling the disbaled user edit button under manage users table",testcase_id='Reflex-UM-254')

                    if erroFlag:
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, "allbuttons")
                        userScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                        time.sleep(5)
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
                        checkEqualAssert(0, len(handle['ErrorMsg']['msg']),message="Verify that on clicking on 'Ok' button,  Error Popup disappears",testcase_id='Reflex-UM-254')


                else:
                    logger.info("Could not click on edit icon against user '"+ str(targetUser_Username)+ "' under manage users table")
                    logger.info("Not run Tcs: Reflex-UM-254 ")










            ################### Verify handling for disabled Delete icon under Manage Users table
            if manageRoles_NegativeScenariosDict[str(k)]['operation'] == "enable_disabled_userDelete":
                handle = getHandle(setup, "explore_Screen", "alllabels")
                userScreenInstance.click(handle['alllabels']['label'][0])

                targetUser_Username = userLoginDetailsForManageRolesDict['adminuser_neg_1']['username']
                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEUSERS, 'table')

                elem_delete = UMHelper.enable_DisabledIcons(setup=setup, tableHandle=tableHandle,screenInstance=userScreenInstance,valueUnderAction=targetUser_Username,tableHeader_text="Delete", colIndex=1)
                delete_click_status = userScreenInstance.click(elem_delete)

                if delete_click_status == True:
                    handle = getHandle(setup, UMConstants.UMPOPUP_CONFIRM_DELETEROLE, 'allbuttons')
                    logger.debug("Going to click on 'Ok' buttton on delete user popup ")
                    click_status_fromDelPopup = userScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                    erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR, parent='ErrorMsg',child='msg')
                    checkEqualAssert(UMConstants.MALACIOUS_USER_ERROR_MSG, str(msgFromUI),message="Verify that user '" + str(actionUser_Username) + "' gets an error popup on trying  deleting himself by falsely enabling the disbaled user delete button under manage users table",testcase_id='Reflex-UM-263')

                    if erroFlag:
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, "allbuttons")
                        userScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                        time.sleep(5)
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
                        checkEqualAssert(0, len(handle['ErrorMsg']['msg']),message="Verify that on clicking on 'Ok' button,  Error Popup disappears",testcase_id='Reflex-UM-263')


                else:
                    logger.info("Could not click on delete icon against user '" + str(targetUser_Username) + "' under manage users table")
                    logger.info("Not run Tcs: Reflex-UM-263 ")








            ################### Verify handling for disabled Role Edit icon under Manage Roles table
            if manageRoles_NegativeScenariosDict[str(k)]['operation'] == "enable_disabled_roleEdit":
                handle = getHandle(setup, "explore_Screen", "alllabels")
                userScreenInstance.click(handle['alllabels']['label'][1])

                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                rolenamevalue_tobe_edited = manageRolesNegativeScenario['rolenamevalue_tobe_edited']

                elem_edit = UMHelper.enable_DisabledIcons(setup=setup, tableHandle=tableHandle,screenInstance=roleScreenInstance,valueUnderAction=str(rolenamevalue_tobe_edited), tableHeader_text="Edit",colIndex=0)
                edit_click_status = userScreenInstance.click(elem_edit)

                if edit_click_status == True:
                    handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'allinputs')
                    if handle['allinputs']['input'][0].is_enabled():
                        roleScreenInstance.cm.sendkeys_input(manageRolesNegativeScenario['rolenamevalue_tobe_edited'], handle, 0)

                    updateBtn_status = UMHelper.dumpResultForButton(True, "Edit role '" + str(rolenamevalue_tobe_edited) + "' after enabling disabled edit button under manage roles table",button_label="Update",screenInstance=roleScreenInstance, setup=setup,screen=UMConstants.UMPOPUP_ADDROLE, testcase_id='')

                    erroFlag = False
                    if updateBtn_status:
                        roleScreenInstance.hoverAndClickButton(setup, "Update",getHandle(setup, UMConstants.UMPOPUP_ADDROLE,'allbuttons'))
                        erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR,parent='ErrorMsg', child='msg')
                    checkEqualAssert(UMConstants.MALACIOUS_USER_ERROR_MSG, str(msgFromUI),message="Verify that user '" + str(actionUser_Username) + "' gets an error popup on trying  updating his own role by falsely enabling the disbaled role edit button under manage roles table",testcase_id='Reflex-UM-262')

                    if erroFlag:
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, "allbuttons")
                        userScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                        time.sleep(5)
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
                        checkEqualAssert(0, len(handle['ErrorMsg']['msg']),message="Verify that on clicking on 'Ok' button,  Error Popup disappears",testcase_id='Reflex-UM-262')


                else:
                    logger.info("Could not click on edit icon against role'" + str(rolenamevalue_tobe_edited) + "' under manage roles table")
                    logger.info("Not run Tcs: Reflex-UM-262 ")










            ################### Verify handling for disabled Role Delete icon under Manage Roles table
            if manageRoles_NegativeScenariosDict[str(k)]['operation'] == "enable_disabled_roleDelete":
                handle = getHandle(setup, "explore_Screen", "alllabels")
                userScreenInstance.click(handle['alllabels']['label'][1])

                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                rolenamevalue_tobe_deleted = manageRolesNegativeScenario['rolenamevalue_tobe_deleted']

                elem_delete = UMHelper.enable_DisabledIcons(setup=setup, tableHandle=tableHandle,screenInstance=roleScreenInstance,valueUnderAction=rolenamevalue_tobe_deleted, tableHeader_text="Delete",colIndex=0)
                delete_click_status = userScreenInstance.click(elem_delete)

                if delete_click_status == True:
                    handle = getHandle(setup, UMConstants.UMPOPUP_CONFIRM_DELETEROLE, 'allbuttons')
                    logger.debug("Going to click on 'Ok' buttton on delete user popup ")
                    click_status_fromDelPopup = userScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                    erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR, parent='ErrorMsg',child='msg')
                    checkEqualAssert(UMConstants.MALACIOUS_USER_ERROR_MSG, str(msgFromUI),message="Verify that user '" + str(actionUser_Username) + "' gets an error popup on trying  deleting his own role by falsely enabling the disbaled role delete button under manage roles table",testcase_id='Reflex-UM-260')

                    if erroFlag:
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, "allbuttons")
                        userScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                        time.sleep(5)
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
                        checkEqualAssert(0, len(handle['ErrorMsg']['msg']),message="Verify that on clicking on 'Ok' button,  Error Popup disappears",testcase_id='Reflex-UM-260')


                else:
                    logger.info("Could not click on delete icon against role '" + str(rolenamevalue_tobe_deleted) + "' under manage users table")
                    logger.info("Not run Tcs: Reflex-UM-260 ")








            ################## Verify the behaviour when superadmin tries to edit a role which has already been deleted by another admin user in the same login session.
            if manageRoles_NegativeScenariosDict[str(k)]['operation'] == "edit_deletedRole":
                handle = getHandle(setup, "explore_Screen", "alllabels")
                roleScreenInstance.click(handle['alllabels']['label'][1])

                setup1 = SetUp()
                actionuser2 = manageRolesNegativeScenario['actionuser2']
                login(setup1,userLoginDetailsForManageRolesDict[actionuser2]['username'] , userLoginDetailsForManageRolesDict[actionuser2]['password'])
                handle = getHandle(setup1, "explore_Screen", "alllabels")
                roleScreenInstance.click(handle['alllabels']['label'][1])
                tableHandle = getHandle(setup1, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                column_ValuesFromTable = roleScreenInstance.table.getColumnValueFromTable(0, tableHandle)
                rolenamevalue_tobe_deleted = manageRolesNegativeScenario['rolenamevalue_tobe_deleted']

                logger.info("Deleting Role : " + str(rolenamevalue_tobe_deleted))
                try:
                    click_status, delete_status, click_status_fromDelPopup, popup_disappear_status = UMHelper.deleteRole(setup=setup1, tableHandle=tableHandle,screenInstance=roleScreenInstance,columnValueInRowToBeDeleted=str(rolenamevalue_tobe_deleted),parentScreen=UMConstants.UMSCREEN_MANAGEROLES,screen=UMConstants.UMPOPUP_CONFIRM_DELETEROLE,colIndex=0)
                except Exception as e:
                    logger.info("Got Exception on deleting role : " + str(rolenamevalue_tobe_deleted) + "  " + str(e))
                    click_status, delete_status, click_status_fromDelPopup, popup_disappear_status = "", "", "", ""
                setup1.d.close()

                if popup_disappear_status == True:
                    rolenamevalue_tobe_edited = manageRolesNegativeScenario['rolenamevalue_tobe_edited']
                    logger.info("Updating already deleted role : " + str(rolenamevalue_tobe_edited))
                    tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')

                    try:
                        click_status, expectedRoleName, expectedCheckedCheckBoxesList, roleNameFromUI, checkedCheckBoxesListFromUI, updateBtnStatus = UMHelper.editRole(setup=setup, tableHandle=tableHandle,screenInstance=roleScreenInstance, columnValueInRowToBeEdited=str(rolenamevalue_tobe_edited),roleDetail=manageRolesNegativeScenario,parentscreen=UMConstants.UMSCREEN_MANAGEROLES,screen=UMConstants.UMPOPUP_ADDROLE,k='0', colIndex=0)
                    except Exception as e:
                        logger.info("Got Exception on updating role : " + str(rolenamevalue_tobe_edited) + "  " + str(e))
                        click_status, expectedRoleName, expectedCheckedCheckBoxesList, roleNameFromUI, checkedCheckBoxesListFromUI, updateBtnStatus = "","","","","",""

                if updateBtnStatus == True:
                    handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, "allbuttons")
                    roleScreenInstance.click(handle['allbuttons']['button'][0])
                    erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR, parent='ErrorMsg', child='msg')
                    checkEqualAssert(UMConstants.ROLE_EXPIRED_MSG,str(msgFromUI),message="Verify that valid error messages appears when one admin user tries to edit another user that has been deleted by other admin user in the same login session.",testcase_id='Reflex-UM-204')

                    if erroFlag:
                        handle = getHandle(setup,UMConstants.UMPOPUP_ERROR,"allbuttons")
                        roleScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                        time.sleep(5)
                        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
                        checkEqualAssert(0,len(handle['ErrorMsg']['msg']),message="Verify that on clicking on 'Ok' button,  Error Popup disappears",testcase_id='Reflex-UM-204')




    setup.d.close()



except Exception as e:
    logger.debug("Exception Occurred: "+ str(e))
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()


