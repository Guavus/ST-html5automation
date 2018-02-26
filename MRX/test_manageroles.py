from MuralUtils.ContentHelper import *
from Utils import UMHelper
from classes.Pages.MuralScreens.RoleManagementScreen import *
from classes.Pages.ExplorePageClass import *
#from MRXUtils.MRXConstants import *
from Utils.UMConstants import *
from classes.Pages.MuralScreens.UserMangementScreen import UserManagementScreenClass

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    isError(setup)
    wfstart = WorkflowStartComponentClass()
    userScreenInstance = UserManagementScreenClass(setup.d)
    handle = getHandle(setup, "explore_Screen","alllabels")
    roleScreenInstance=RoleManagementScreenClass(setup.d)
    roleScreenInstance.click(handle['alllabels']['label'][1])



    ################### Verify New Role label on UM Role Management screen
    tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
    actualHeader=roleScreenInstance.table.getIterfaceHeaders(tableHandle['table'])
    checkEqualAssert(UMConstants.UMSCREENTABLEHEADERLIST_MANAGEROLES,actualHeader,message="Verify table header on UM Screen for Manage roles",testcase_id="Reflex-UM-188")
    newRoleLabel=roleScreenInstance.getScreenNameFromUI(getHandle(setup,UMConstants.UMSCREEN_MANAGEROLES,'alllabels'))
    checkEqualAssert(UMConstants.NEWROLE,newRoleLabel,message="Verify New Role label on UM Role Management screen",testcase_id="Reflex-UM-189")

    ############## Verify searchbox UM Role Management screen does a valid search on rolenames
    #tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
    column_ValuesFromTable_withoutSearch = roleScreenInstance.table.getColumnValueFromTable(0, tableHandle)
    searchValue = column_ValuesFromTable_withoutSearch[0][:3]
    expectedSearchList = []
    for colValue in column_ValuesFromTable_withoutSearch:
        if searchValue.lower() in colValue.lower():
            expectedSearchList += [colValue]
    handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'allinputs')
    searchValueFromUI = str(roleScreenInstance.cm.sendkeys_input(searchValue, handle, index=0))
    tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
    column_ValuesFromTable_withSearch = roleScreenInstance.table.getColumnValueFromTable(0, tableHandle)
    checkEqualAssert(str([searchValue] + expectedSearchList),str([searchValueFromUI] + column_ValuesFromTable_withSearch),message="Verify that user is able to search a rolename using searcbox on manage roles table",testcase_id="Reflex-UM-187")
    roleScreenInstance.cm.sendkeys_input("", handle, index=0)


    ############### Verify that table on manage roles screen can be sorted on columns rolename and default privileges
    UMHelper.verifySortingOnTable(setup, roleScreenInstance, screenName=UMConstants.UMSCREEN_MANAGEROLES, parent='table', sortTableColumnTag='rolesorttablecolumn',sortTableColumnInnerTag='column',testcase_id="Reflex-UM-181")




    ############## Verify field options given in add role popup
    handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
    click_status = UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES, parent='newRoleIcon',child='icon')
    handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'alllabels')
    checkEqualAssert(str([True,True]), str([click_status,len(handle['alllabels']['label']) > 0]), message="Verify the  New application role icon '+' is clickable on the manage roles screen and a popup comes up when it is clicked.",testcase_id='Reflex-UM-244')

    expectedOptionFieldsOnAddRolePopup = UMConstants.EXPECTEDOPTIONFIELDS_ON_ADDROLEPOPUP
    fieldsOnAddRolePopupFromUI = roleScreenInstance.getAllTitle(handle, parent='alllabels', child='label')
    actualFieldsOnAddRolePopupFromUI = fieldsOnAddRolePopupFromUI[:2]
    checkEqualAssert(expectedOptionFieldsOnAddRolePopup, actualFieldsOnAddRolePopupFromUI,message='Verify the field options given in the new role dialog box', testcase_id='Reflex-UM-193')




    ############# Verify list of available privileges on add role popup
    expectedPrivilegesList = UMConstants.AVAILABLE_PRIVILEGES
    handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'tree')
    actualPrivilegesListFromUI = []
    for chechbox_elem in handle['tree']['checkboxes']:
        actualPrivilegesListFromUI += [str(chechbox_elem.find_element_by_xpath("..").text)]
    checkEqualAssert(expectedPrivilegesList, actualPrivilegesListFromUI,message='Verify the avalibale options for privileges under Application privileges on add role popup',testcase_id='Reflex-UM-10')




    ############# Verify the required Fields label on add role popup
    expectedRequiredFieldsLabel = UMConstants.REQUIREDFIELDSLABEL
    handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'content')
    reqiredLabelFromUI = ""
    if len(handle['content']['requiredFieldLabel']) > 0:
        reqiredLabelFromUI = str(handle['content']['requiredFieldLabel'][0].text)
    else:
        logger.debug("Required fields label could not be fetched from UI")
    checkEqualAssert(expectedRequiredFieldsLabel, reqiredLabelFromUI,message="Verify requiredFields label on UM add role popup", testcase_id="Reflex-UM-154")

    handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'allbuttons')
    logger.info("Exiting from Add role popup by clicking on 'Cancel' button")
    roleScreenInstance.hoverAndClickButton(setup, "Cancel", handle)







    ################# Verify manage roles operations
    manageRolesScenariosDict = setup.cM.getNodeElements("manageRoleScenarios", "scenario")
    userLoginDetailsForManageRolesDict = setup.cM.getNodeElements("umUserLoginDetailsForManageRoles", "user")
    for k,manageRolesScenario in sorted(manageRolesScenariosDict.iteritems()):
        k = "29"    #************** to be removed
        manageRolesScenario = manageRolesScenariosDict[k] #******************* to be removed

        actionUser = manageRolesScenariosDict[k]['actionuser']
        actionUser_Name = userLoginDetailsForManageRolesDict[actionUser]['name']
        actionUser_Username = userLoginDetailsForManageRolesDict[actionUser]['username']
        actionUser_Password = userLoginDetailsForManageRolesDict[actionUser]['password']
        handle = getHandle(setup, "explore_Screen", "alllinks")
        parentLoggedInUser_Name = str(handle['alllinks']['a'][0].text)
        #parentLoggedInUser_Name = "abc xyz"   #************ To be removed
        if actionUser_Name != parentLoggedInUser_Name:
            roleScreenInstance.click(handle['alllinks']['a'][0])  ## Click on Profile link
            handle = getHandle(setup, "explore_Screen", "alllinks")
            roleScreenInstance.click(handle['alllinks']['a'][2])  ## Click on Logout
            time.sleep(5)
            username = actionUser_Username
            password = actionUser_Password
            if "adminuser" in actionUser:
                logger.info("Logging in with some admin user : '" + actionUser_Name)
                login(setup,username,password)
                parentLoggedInUser_Name = actionUser_Name
            elif "normaluser" in actionUser:
                logger.info("Logging in with some normal user : '" +actionUser_Name)
                login(setup, username, password)
                erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup,UMConstants.UMPOPUP_ERRORLOGIN,parent='loginErrorMsgContainer',child='msg')
                checkEqualAssert(str([True,UMConstants.LOGIN_ACCESSDENIED_MSG]),str([erroFlag,msgFromUI]),message="Verify that an Access Denied Error Popup appears when a normal user tries to login in User Management App",testcase_id='Reflex-UM-231')
                handle = getHandle(setup,UMConstants.UMPOPUP_ERRORLOGIN,'allbuttons')
                roleScreenInstance.hoverAndClickButton(setup, "Ok", handle)
                time.sleep(5)
                handle = getHandle(setup,UMConstants.UMPOPUP_ERRORLOGIN,'loginErrorMsgContainer')
                checkEqualAssert(0,len(handle),message="Verify that on clicking on 'Ok' button, Access Denied Error Popup disappears",testcase_id='Reflex-UM-231')
                parentLoggedInUser_Name = ""






        if parentLoggedInUser_Name != "":
            if manageRolesScenariosDict[k]['operation'] == "role_create" :
                handle = getHandle(setup, "explore_Screen", "alllabels")
                roleScreenInstance.click(handle['alllabels']['label'][1])
                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                tableData_beforeCreateRole = roleScreenInstance.table.getTableData1(tableHandle)

                handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
                click_status = UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES, parent='newRoleIcon',child='icon')
                try:
                    expectedRoleName, expectedCheckedCheckBoxesList, roleNameFromUI, checkedCheckBoxesListFromUI, createBtnStatus = UMHelper.setRoleDetails(roleScreenInstance, setup, str(k), screen=UMConstants.UMPOPUP_ADDROLE, roleDetail=manageRolesScenario)
                    logger.debug("Control came out from setRoleDetails method")
                except Exception as e:
                    logger.info("Got Exception on creating a role when executed scenario" + str(k) + " : " + str(e))
                    expectedRoleName, expectedCheckedCheckBoxesList, roleNameFromUI, checkedCheckBoxesListFromUI, createBtnStatus = str(manageRolesScenario['rolename']), [int(index.strip()) for index in manageRolesScenario['applicationprivileges'].split(",")] ,"", "", False
                #checkEqualAssert(expectedRoleName, roleNameFromUI, message="Verify te format of Entered Role Name",testcase_id='Reflex-UM-194')
                if tableData_beforeCreateRole['rows'] != Constants.NODATA:
                    numberOfRows_beforeCreateRole = len(tableData_beforeCreateRole['rows'])
                else:
                    logger.debug("Manage Roles table contains no data before a Role is created")
                    numberOfRows_beforeCreateRole = 0
                expected_RoleEntry_forTable = [expectedRoleName] + expectedCheckedCheckBoxesList + ['', '']
                handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'allbuttons')
                if createBtnStatus:
                    logger.debug("Going to click on 'Create' buttton on add role popup ")
                    roleScreenInstance.hoverAndClickButton(setup, "Create", handle)
                    if manageRolesScenariosDict[k]['roleExists'] == 'Yes':
                        logger.debug("Fetching Role already exists label from add role popup ")
                        handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'roleErrorMsgContainer')
                        roleExistsLabelFromUI = ""
                        if len(handle['roleErrorMsgContainer']['msg']) > 0:
                            roleExistsLabelFromUI = str(handle['roleErrorMsgContainer']['msg'][0].text)
                            logger.debug("Exiting from popup screen through Cancel' button ")
                            handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'allbuttons')
                            roleScreenInstance.hoverAndClickButton(setup, "Cancel", handle)
                        else:
                            logger.debug("Role already exists label cound not be fetched from add role popup ")
                        checkEqualAssert(UMConstants.ROLE_EXISTS_ERROR_MSG, roleExistsLabelFromUI,message="Verify that user '" + parentLoggedInUser_Name + "' can not create role with a role name that already exists.",testcase_id='Reflex-UM-184')
                        roleScreenInstance.hoverAndClickButton(setup, "Cancel", handle)
                        continue
                else:
                    logger.debug(" 'Create' button on add role popup is not enabled. Hence exiting from popup screen through Cancel' button ")
                    roleScreenInstance.hoverAndClickButton(setup, "Cancel", handle)
                logger.debug("Getting table handle after Creating a new role")
                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                tableData_afterCreateRole = roleScreenInstance.table.getTableData1(tableHandle)
                if tableData_afterCreateRole['rows'] != Constants.NODATA:
                    numberOfRows_afterCreateRole = len(tableData_afterCreateRole['rows'])
                    roleEntry_forTableFromUI = []
                    rolenameFoundFlag = False
                    for row in tableData_afterCreateRole['rows']:
                        if str(row[0]) == expectedRoleName:
                            logger.debug("Rolename for newly created role found in the first column of the table")
                            roleEntry_forTableFromUI = [str(row[0])] + row[1].replace(', ', ',').split(',') + [row[2]] + [row[3]]
                            rolenameFoundFlag = True
                            break
                    if not rolenameFoundFlag:
                        logger.debug("Rolename for newly created role not found in the first column of the table")
                else:
                    logger.debug("Manage Roles table contains no data even after a Role is created")
                    numberOfRows_afterCreateRole = 0
                    roleEntry_forTableFromUI = []

                checkEqualAssert(str([True] + sorted(expected_RoleEntry_forTable)), str([click_status] + sorted(roleEntry_forTableFromUI)),message="Verify a new role can be successfuly created by user " +parentLoggedInUser_Name ,testcase_id='Reflex-UM-200,Reflex-UM-226,Reflex-UM-244,Reflex-UM-245')
                checkEqualAssert(numberOfRows_beforeCreateRole + 1, numberOfRows_afterCreateRole,message="Verify the count of rows under manage roles table when a new role is created by the user " +parentLoggedInUser_Name,testcase_id='Reflex-UM-200,Reflex-UM-226')










            elif manageRolesScenariosDict[k]['operation'] == "role_edit" :
                handle = getHandle(setup, "explore_Screen", "alllabels")
                roleScreenInstance.click(handle['alllabels']['label'][1])
                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                tableData_beforeUpdateRole = roleScreenInstance.table.getTableData1(tableHandle)
                if tableData_beforeUpdateRole['rows'] != Constants.NODATA:
                    numberOfRows_beforeUpdateRole = len(tableData_beforeUpdateRole['rows'])
                    columnValueInRowToBeEdited = manageRolesScenariosDict[k]['rolenamevalue_tobe_edited']
                    try:
                        click_status, expectedRoleName, expectedCheckedCheckBoxesList, roleNameFromUI, checkedCheckBoxesListFromUI, updateBtnStatus = UMHelper.editRole(setup=setup,tableHandle=tableHandle,screenInstance=roleScreenInstance,parentscreen=UMConstants.UMSCREEN_MANAGEROLES,columnValueInRowToBeEdited=columnValueInRowToBeEdited,screen=UMConstants.UMPOPUP_ADDROLE,k=str(k),roleDetail=manageRolesScenario,colIndex=0)
                        logger.debug("Control came out from editRole method")
                    except Exception as e:
                        logger.info("Got Exception on editing a role when executed scenario" + str(k) + " : " + str(e))
                        click_status, expectedRoleName, expectedCheckedCheckBoxesList, roleNameFromUI, checkedCheckBoxesListFromUI, updateBtnStatus = False, str(manageRolesScenario['rolename']), [int(index.strip()) for index in manageRolesScenario['applicationprivileges'].split(",")], "", "", False

                    handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'allbuttons')
                    if updateBtnStatus:
                        logger.debug("Going to click on 'Update' buttton on add role popup ")
                        roleScreenInstance.hoverAndClickButton(setup, "Update", handle)
                    else:
                        logger.debug(" 'Update' button on add role popup is not enabled. Hence exiting from popup screen through Cancel' button ")
                        roleScreenInstance.hoverAndClickButton(setup, "Cancel", handle)
                    expected_RoleEntry_forTable = [expectedRoleName] + expectedCheckedCheckBoxesList + ['', '']
                    logger.debug("Getting table handle after Updating an existing role")
                    tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                    tableData_afterUpdateRole = roleScreenInstance.table.getTableData1(tableHandle)
                    if tableData_afterUpdateRole['rows'] != Constants.NODATA:
                        numberOfRows_afterUpdateRole = len(tableData_afterUpdateRole['rows'])
                        roleEntry_forTableFromUI = []
                        rolenameFoundFlag = False
                        for row in tableData_afterUpdateRole['rows']:
                            if str(row[0]) == expectedRoleName:
                                logger.debug("Updated Rolename found in the first column of the table")
                                roleEntry_forTableFromUI = [str(row[0])] + row[1].replace(', ', ',').split(',') + [row[2]] + [row[3]]
                                rolenameFoundFlag = True
                                break

                        if not rolenameFoundFlag:
                            logger.debug(" Updated Rolename could not be found in the first column of the table")
                    else:
                        numberOfRows_afterUpdateRole = 0
                        roleEntry_forTableFromUI = []
                else:
                    numberOfRows_beforeUpdateRole = -1
                    expected_RoleEntry_forTable = []

                if (actionUser == "superadmin" or "adminuser" in actionUser) and manageRolesScenariosDict[k]['rolenamevalue_tobe_edited'] != 'Admin':
                    expectedEditClick_status = True
                    checkEqualAssert(expectedEditClick_status, click_status,message="Verify that user " + parentLoggedInUser_Name + " is able to edit another(non-admin) role ",testcase_id='Reflex-UM-235,Reflex-UM-237')
                    checkEqualAssert(str(sorted(expected_RoleEntry_forTable)), str(sorted(roleEntry_forTableFromUI)),message="Verify an existing row is successfully updated in manage roles table  by user " + parentLoggedInUser_Name,testcase_id='Reflex-UM-235,Reflex-UM-237')
                    checkEqualAssert(numberOfRows_beforeUpdateRole, numberOfRows_afterUpdateRole,message="Verify the count of rows after a role is updated in manage roles table by user " + parentLoggedInUser_Name,testcase_id='Reflex-UM-235,Reflex-UM-237')
                else:
                    expectedEditClick_status = False
                    checkEqualAssert(expectedEditClick_status, click_status,message="Verify that user " + parentLoggedInUser_Name  + " is not able to edit Admin(own) role ",testcase_id='Reflex-UM-239,Reflex-UM-241')








            elif manageRolesScenariosDict[k]['operation'] == "role_delete" :
                handle = getHandle(setup, "explore_Screen", "alllabels")
                roleScreenInstance.click(handle['alllabels']['label'][1])
                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                tableData_beforeDeleteRole = roleScreenInstance.table.getTableData1(tableHandle)
                if tableData_beforeDeleteRole['rows'] != Constants.NODATA:
                    numberOfRows_beforeDeleteRole = len(tableData_beforeDeleteRole['rows'])
                    columnValueInRowToBeDeleted = manageRolesScenariosDict[k]['rolenamevalue_tobe_deleted']
                    try:
                        click_status, delete_status, click_status_fromDelPopup, popup_disappear_status = UMHelper.deleteRole(setup=setup, tableHandle=tableHandle, screenInstance=roleScreenInstance,parentScreen=UMConstants.UMSCREEN_MANAGEROLES,screen=UMConstants.UMPOPUP_CONFIRM_DELETEROLE,columnValueInRowToBeDeleted=columnValueInRowToBeDeleted, colIndex=0)
                        logger.debug("Control came out from deleteRole method")
                    except Exception as e:
                        logger.info("Got Exception on deleting a role when executed scenario" + str(k) + " : " + str(e))
                        click_status, delete_status, click_status_fromDelPopup, popup_disappear_status= "","","",""
                    tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
                    tableData_afterDeleteRole = roleScreenInstance.table.getTableData1(tableHandle)
                    if tableData_afterDeleteRole['rows'] != Constants.NODATA:
                        numberOfRows_afterDeleteRole = len(tableData_afterDeleteRole['rows'])
                    else:
                        numberOfRows_afterDeleteRole = 0
                else:
                    numberOfRows_beforeDeleteRole = -1

                if (actionUser == "superadmin" or "adminuser" in actionUser) and manageRolesScenariosDict[k]['rolenamevalue_tobe_deleted'] != 'Admin':
                    expectedDeleteClick_status = True
                    checkEqualAssert(expectedDeleteClick_status, click_status,message="Verify that user " + parentLoggedInUser_Name + " is able to delete another(non-admin) role ",testcase_id='Reflex-UM-232,Reflex-UM-233')
                    checkEqualAssert(str([True,True,True,True]), str([click_status, delete_status, click_status_fromDelPopup, popup_disappear_status]), message="Verify that role got deleted successfully",testcase_id='Reflex-UM-232,Reflex-UM-233')
                    checkEqualAssert(numberOfRows_beforeDeleteRole - 1, numberOfRows_afterDeleteRole,message="Verify the count of rows after deleting a role from manage roles table",testcase_id='Reflex-UM-232,Reflex-UM-233')
                else:
                    expectedDeleteClick_status = False
                    checkEqualAssert(expectedDeleteClick_status, click_status,message="Verify that user " + parentLoggedInUser_Name + " is not able to delete Admin(own) role ",testcase_id='Reflex-UM-205,Reflex-UM-212')








            elif manageRolesScenariosDict[k]['operation'] == "user_create_assign_role" :
                handle = getHandle(setup, "explore_Screen", "alllabels")
                roleScreenInstance.click(handle['alllabels']['label'][0])
                handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEUSERS, 'newUserIcon')
                UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES, parent='newUserIcon',child='icon')
                try:
                    userDetailsDictFromUI, userCreated_RoleAssigned_Status = UMHelper.setUserDetail(setup, userScreenInstance, UMConstants.UMPOPUP_ADDUSER, userDetail=manageRolesScenario,button="Create", checkComplusoryFieldFlag=False)
                    logger.debug("Control came out from setUserDetail method when performing operation user_create_assign_role")
                except Exception as e:
                    logger.info("Got Exception on creating a user when executed scenario" + str(k) + " : " + str(e))
                    userDetailsDictFromUI, userCreated_RoleAssigned_Status = {}, False

                loggedInUser_Name = ""
                if userCreated_RoleAssigned_Status:
                    actionUser_Name = userDetailsDictFromUI['name']
                    actionUser_Username = userDetailsDictFromUI['username']
                    actionUser_Password = userDetailsDictFromUI['password']
                    handle = getHandle(setup, "explore_Screen", "alllinks")
                    roleScreenInstance.click(handle['alllinks']['a'][0])  ## Click on Profile link
                    handle = getHandle(setup, "explore_Screen", "alllinks")
                    roleScreenInstance.click(handle['alllinks']['a'][2])  ## Click on Logout
                    time.sleep(5)
                    login(setup, actionUser_Username, actionUser_Password)
                    handle = getHandle(setup, "explore_Screen", "alllinks")
                    if len(handle['alllinks']['a']) > 0:
                         loggedInUser_Name = str(handle['alllinks']['a'][0].text)


                if userDetailsDictFromUI != {}:
                    if userDetailsDictFromUI['userrole'] == "Admin" :
                        checkEqualAssert(str([True,True]), str([userCreated_RoleAssigned_Status,loggedInUser_Name == actionUser_Name]), message="Verify that '" + parentLoggedInUser_Name + "' user can create a new user and assign admin role to him and that user is able to login successfully",testcase_id='Reflex-UM-201,Reflex-UM-234')
                    else:
                        checkEqualAssert(str([True,False]), str([userCreated_RoleAssigned_Status,loggedInUser_Name == actionUser_Name]),message="Verify that '" + parentLoggedInUser_Name + "' user can create a new user and assign any other normal role to him and that user is not able to login in User Management app",testcase_id='Reflex-UM-202,Reflex-UM-207')

                else:
                    logger.error("Not Run TCs: Reflex-UM-201,Reflex-UM-202")
                    resultlogger.error("Not Run TCs: Reflex-UM-201,Reflex-UM-202")
                    roleScreenInstance.hoverAndClickButton(setup, "Cancel", getHandle(setup, UMConstants.UMPOPUP_ADDUSER, 'allbuttons'))









            elif manageRolesScenariosDict[k]['operation'] == "user_edit":
                handle = getHandle(setup, "explore_Screen", "alllabels")
                roleScreenInstance.click(handle['alllabels']['label'][0])
                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEUSERS, 'table')
                tableData_beforeEditUser = roleScreenInstance.table.getTableData1(tableHandle)
                targetUser = manageRolesScenariosDict[k]['targetuser']
                targetUser_Username = userLoginDetailsForManageRolesDict[targetUser]['username']
                try:
                    click_status, modifiableFieldsDictFromUI,updateBtn_status = UMHelper.editUser(setup,tableHandle=tableHandle,screenInstance=roleScreenInstance,userDetail=manageRolesScenario,k=str(k),targetUser_Username=targetUser_Username,parentscreen=UMConstants.UMSCREEN_MANAGEUSERS,screen=UMConstants.UMPOPUP_ADDUSER,colIndex=1)
                except Exception as e:
                    logger.info("Got Exception on editing a user when executed scenario" + str(k) + " : " + str(e))
                    click_status, modifiableFieldsDictFromUI,updateBtn_status = "", {}, False


                if actionUser == "superadmin" and targetUser == 'superadmin':
                    checkEqualAssert(False, click_status,message="Verify that user'" + parentLoggedInUser_Name + "'  cannot edit user '" + targetUser + "'",testcase_id='Reflex-UM-206')


                elif actionUser == "superadmin" and "adminuser" in targetUser:
                    expected_modifiableFieldsDict = sorted(UMConstants.MODIFIABLE_FIELDS_ALL.iteritems())
                    checkEqualAssert(str([True,expected_modifiableFieldsDict, True]), str([click_status,modifiableFieldsDictFromUI, updateBtn_status]),message="Verify that user '" + parentLoggedInUser_Name + "' can edit user '" + targetUser + "'",testcase_id='Reflex-UM-225')


                elif actionUser == "superadmin" and "normaluser" in targetUser:
                    expected_modifiableFieldsDict = sorted(UMConstants.MODIFIABLE_FIELDS_ALL.iteritems())
                    checkEqualAssert(str([True,expected_modifiableFieldsDict, True]), str([click_status,modifiableFieldsDictFromUI, updateBtn_status]),message="Verify that user '" + parentLoggedInUser_Name + "' can edit user '" + targetUser + "'",testcase_id='Reflex-UM-224')


                elif "adminuser" in actionUser and targetUser == "superadmin":
                    checkEqualAssert(False, click_status,message="Verify that user'" + parentLoggedInUser_Name + "'  cannot edit user '" + targetUser + "'",testcase_id='Reflex-UM-210')


                elif "adminuser" in actionUser and "adminuser" in targetUser and actionUser == targetUser:
                    expected_modifiableFieldsDict = sorted(UMConstants.MODIFIABLE_FIELDS_NO_PASS_ROLECHANGE_DISABLE.iteritems())
                    checkEqualAssert(str([True,expected_modifiableFieldsDict, True]), str([click_status,modifiableFieldsDictFromUI, updateBtn_status]),message="Verify that user '" + parentLoggedInUser_Name + "' can edit user '" + targetUser + "'",testcase_id='Reflex-UM-211')


                elif "adminuser" in actionUser and "adminuser" in targetUser and actionUser != targetUser:
                    expected_modifiableFieldsDict = sorted(UMConstants.MODIFIABLE_FIELDS_ALL.iteritems())
                    checkEqualAssert(str([True,expected_modifiableFieldsDict, True]), str([click_status,modifiableFieldsDictFromUI, updateBtn_status]),message="Verify that user '" + parentLoggedInUser_Name + "' can edit user '" + targetUser + "'",testcase_id='Reflex-UM-209')


                elif "adminuser" in actionUser and "normaluser" in targetUser:
                    expected_modifiableFieldsDict = sorted(UMConstants.MODIFIABLE_FIELDS_ALL.iteritems())
                    checkEqualAssert(str([True,expected_modifiableFieldsDict, True]), str([click_status,modifiableFieldsDictFromUI, updateBtn_status]),message="Verify that user '" + parentLoggedInUser_Name + "' can edit user '" + targetUser + "'",testcase_id='Reflex-UM-208')











            elif manageRolesScenariosDict[k]['operation'] == "user_delete":
                handle = getHandle(setup, "explore_Screen", "alllabels")
                roleScreenInstance.click(handle['alllabels']['label'][0])
                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEUSERS, 'table')
                tableData_beforeEditUser = roleScreenInstance.table.getTableData1(tableHandle)
                targetUser = manageRolesScenariosDict[k]['targetuser']
                targetUser_Username = userLoginDetailsForManageRolesDict[targetUser]['username']

                try:
                    click_status, delete_status,click_status_fromDelPopup,popup_disappear_status = UMHelper.deleteUser(setup=setup, tableHandle=tableHandle, screenInstance=roleScreenInstance, k=k, targetUser_Username=targetUser_Username,screen=UMConstants.UMSCREEN_MANAGEUSERS, colIndex=1)
                except Exception as e:
                    logger.info("Got Exception on deleting a user when executed scenario " + str(k) + " : " + str(e))
                    click_status, delete_status, click_status_fromDelPopup, popup_disappear_status = "","","",""

                tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEUSERS, 'table')
                tableData_afterEditUser = roleScreenInstance.table.getTableData1(tableHandle)

                if actionUser == "superadmin" and targetUser == 'superadmin':
                    checkEqualAssert(False, click_status,message="Verify that user'" + parentLoggedInUser_Name + "'  cannot delete user '" + targetUser + "'",testcase_id='Reflex-UM-246')

                elif actionUser == "superadmin" and "adminuser" in targetUser:
                    checkEqualAssert(str([True,True,True,True,len(tableData_beforeEditUser)-1]), str([click_status,delete_status,click_status_fromDelPopup,popup_disappear_status,len(tableData_afterEditUser)]),message="Verify that user '" + parentLoggedInUser_Name + "' can delete user '" + targetUser + "'",testcase_id='Reflex-UM-248')

                elif actionUser == "superadmin" and "normaluser" in targetUser:
                    checkEqualAssert(str([True,True,True,True,len(tableData_beforeEditUser)-1]), str([click_status,delete_status,click_status_fromDelPopup,popup_disappear_status,len(tableData_afterEditUser)]),message="Verify that user '" + parentLoggedInUser_Name + "' can delete user '" + targetUser + "'",testcase_id='Reflex-UM-249')

                elif "adminuser" in actionUser and targetUser == "superadmin":
                    checkEqualAssert(False, click_status,message="Verify that user'" + parentLoggedInUser_Name + "'  cannot delete user '" + targetUser + "'",testcase_id='Reflex-UM-252')

                elif "adminuser" in actionUser and "adminuser" in targetUser and actionUser == targetUser:
                    checkEqualAssert(False, click_status,message="Verify that user '" + parentLoggedInUser_Name + "' cannot delete user '" + targetUser + "'",testcase_id='Reflex-UM-253')

                elif "adminuser" in actionUser and "adminuser" in targetUser and actionUser != targetUser:
                    checkEqualAssert(str([True,True,True,True,len(tableData_beforeEditUser)-1]), str([click_status,delete_status,click_status_fromDelPopup,popup_disappear_status,len(tableData_afterEditUser)]),message="Verify that user '" + parentLoggedInUser_Name + "' can delete user '" + targetUser + "'",testcase_id='Reflex-UM-251')

                elif "adminuser" in actionUser and "normaluser" in targetUser:
                    checkEqualAssert(str([True,True,True,True,len(tableData_beforeEditUser)-1]), str([click_status,delete_status,click_status_fromDelPopup,popup_disappear_status,len(tableData_afterEditUser)]),message="Verify that user '" + parentLoggedInUser_Name + "' can delete user '" + targetUser + "'",testcase_id='Reflex-UM-250')




    

    ############## Verify help/close(X) icon on add role popup
    handle = getHandle(setup, "explore_Screen", "alllabels")
    roleScreenInstance.click(handle['alllabels']['label'][1])
    handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
    UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES, parent='newRoleIcon',child='icon')

    handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'popupIcons')
    click_status = UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMPOPUP_ADDROLE,parent='popupIcons', child='closeIcon')
    checkEqualAssert(True, click_status, message='Verify Close icon on Add Role Popup is clickable',testcase_id="Reflex-UM-190")

    if click_status == True:
        handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
        UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES, parent='newRoleIcon',child='icon')
        handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, 'popupIcons')

    click_status = UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMPOPUP_ADDROLE,parent='popupIcons', child='helpIcon')
    checkEqualAssert(True, click_status, message='Verify Help icon on Add Role Popup is clickable',testcase_id="Reflex-UM-191")


    setup.d.close()


except Exception as e:
    logger.debug("Exception Occurred: "+ str(e))
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()


