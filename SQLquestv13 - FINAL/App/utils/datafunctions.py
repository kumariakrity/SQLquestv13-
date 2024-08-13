import mysql.connector as m
connection = m.connect(host='localhost',user='root',password='root@123',database='sqlquest5')
cursor = connection.cursor()

def OnSignUP_AddDataToUsersTable(username,email,password):
    add_user = f"INSERT INTO users (Username, Email, Password) VALUES ('{username}', '{email}', '{password}')"
    try:
        result = cursor.execute(add_user)
        print("Execution Result:", result)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error occurred while adding user: {e}")
        return False

def OnSignIN_CheckForValidUserPassword(username, password):
    try:
        query = f"SELECT * FROM users WHERE Username = '{username}' AND Password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return user[0]
        else:
            return 0
    except Exception as e:
        print(f"Error occurred while checking user credentials: {e}")
        return 0

def On_LoginLogout_AddDataToLogsTable(userid, logValue):
    try:
        cursor.callproc("InsertLoginLogoutLog", [userid, logValue])
        connection.commit()
        print("Stored procedure called successfully")
    except m.Error as error:
        print(f"Error calling stored procedure: {error}")
        connection.rollback()
    
def GetUserTotalModuleProgressDetails(userID):
    query = f"select sum(CompletedQuestions) as TotalCompletedQuestions,sum(TotalQuestions) as OverallTotalQuestions,(sum(CompletedQuestions)/sum(TotalQuestions))*100 as OverallProgress from usermoduleprogress where UserID = {userID}"
    cursor.execute(query)
    result = cursor.fetchall()
    # Convert list of tuples to list of dictionaries
    columns = [col[0] for col in cursor.description]  # Get column names
    data = dict(zip(columns,result[0])) if result else {}
    """
    #This is how the "data" looks after getting from database
        data= {'TotalCompletedQuestions': <sum(CompletedQuestions)>,
               'OverallTotalQuestions': <sum(TotalQuestions)>,
               'OverallProgress': <Overall_percentage_progress>}
    """
    return data

def GetUserEachModuleProgressDetails(userID):
    query= f"select A.ModuleID,A.Description,B.CompletedQuestions,B.TotalQuestions,B.ProgressPercentage from modules A,usermoduleprogress B where A.ModuleID = B.ModuleID and UserID = {userID}"
    cursor.execute(query)
    result = cursor.fetchall()
    # Convert list of tuples to list of dictionaries
    columns = [col[0] for col in cursor.description]  # Get column names
    alldata = [dict(zip(columns, row)) for row in result]
    return alldata
    """
    #This is how the "alldata" looks after getting from database
        alldata = [
                    {
                        'ModuleID': <value_of_ModuleID_1>,
                        'Description': <value_of_Description_1>,
                        'CompletedQuestions': <value_of_CompletedQuestions_1>,
                        'TotalQuestions': <value_of_TotalQuestions_1>,
                        'ProgressPercentage': <value_of_ProgressPercentage_1>
                    },
                    {
                        'ModuleID': <value_of_ModuleID_2>,
                        'Description': <value_of_Description_2>,
                        'CompletedQuestions': <value_of_CompletedQuestions_2>,
                        'TotalQuestions': <value_of_TotalQuestions_2>,
                        'ProgressPercentage': <value_of_ProgressPercentage_2>
                    },
                    # and so on for each module
                ]
    """

def GetAllModuleInto():
    query="select * from modules;"
    cursor.execute(query)
    result=cursor.fetchall()
    columns = [col[0] for col in cursor.description]  # Get column names
    moduleinfo= [dict(zip(columns, row)) for row in result]
    return moduleinfo
    
def GetAllQuestionsDetailsOfUser(userid):
    # Define the SQL query
    getSideBarInfoOfUser = f"SELECT u.ModuleID, m.Description, u.QuestionID, u.IsCorrect FROM modules m, usertotalprogress u WHERE m.ModuleID = u.ModuleID AND u.UserID = {userid};"
    
    # Execute the query
    cursor.execute(getSideBarInfoOfUser)
    result = cursor.fetchall()

    # Convert list of tuples to list of dictionaries
    columns = [col[0] for col in cursor.description]  # Get column names
    sideBarInfoDict = [dict(zip(columns, row)) for row in result]
    
    return sideBarInfoDict
    # Initialize a dictionary to group by ModuleID and Description
def GetQuestionID_fromModuleID(moduleid):
    GetQuestionIDFromSelectedModule=f"select questionid from questions where moduleid={moduleid} limit 1"
    cursor.execute(GetQuestionIDFromSelectedModule)
    questionID = cursor.fetchone()[0]
    return questionID
def GetSelectedQuestionDetails(questionID,userID,moduleid):
  if(not questionID):
    GetQuestionIDFromSelectedModule=f"select questionid from questions where moduleid={moduleid} limit 1"
    cursor.execute(GetQuestionIDFromSelectedModule)
    questionID = cursor.fetchone()[0]
 
  getQuestionInfo = f"select A.Description,B.CompletedQuestions,B.TotalQuestions,B.ProgressPercentage,C.QuestionID,C.QuestionText,C.CorrectAnswer from modules A, usermoduleprogress B, questions C where A.ModuleID = B.ModuleID and A.ModuleID = C.ModuleID and B.UserID = {userID} and C.QuestionId = {questionID}"
  
  cursor.execute(getQuestionInfo)
  result = cursor.fetchall()

  # Convert list of tuples to single dictionary
  columns = [col[0] for col in cursor.description]  # Get column names
  questionInfoDict = dict(zip(columns,result[0])) if result else {}

  return questionInfoDict

def CheckSyntaxErrorInUserQuery(userquery):
    obj_data_query={'Check':False,'ErroMsg':"None"}
    try:
        cursor.execute(userquery)
        cursor.fetchall()
        obj_data_query['Check']=True
    except m.Error as e:
        print("user query error",e)
        obj_data_query['ErroMsg']=e
    return obj_data_query

def CheckCorrectnessOfUserQuery(userquery,user_id,question_id):
    myquery = f"SELECT ModuleID, CorrectAnswer FROM Questions WHERE QuestionID = {question_id}"
    cursor.execute(myquery)
    result = cursor.fetchone()
    module_id, answerquery = result
    
    try:
        # Execute the user query
        cursor.execute(userquery)
        result1 = cursor.fetchall()
    except m.Error as e:
        print(f"Error executing user queries: {e}")
        result1=[]

    # Execute the answer query 
    cursor.execute(answerquery)
    result2 = cursor.fetchall()
    # Check if the result sets are the same
    if result1 == result2:
        print("Results are the same")
        is_correct = True
    else:
        print("Results are different")
        is_correct = False

    # Insert a new entry into QuestionAttemptLogs
    insert_query = "INSERT INTO QuestionAttemptLogs (UserID, QuestionID,ModuleID,IsCorrect,User_Answer) VALUES (%s,%s, %s, %s, %s)"
    cursor.execute(insert_query, (user_id, question_id,module_id,is_correct,userquery))
    connection.commit()  # Commit the transaction
    print("New entry inserted into QuestionAttemptLogs successfully")

    if(is_correct):
        return True
    else:
        return False
def GetUserAnswer(userid,questionid):
    if userid is None or questionid is None:
        return None 
    query=f"select User_Answer from usertotalprogress where userid={userid} and questionid={questionid};"
    cursor.execute(query)
    result=cursor.fetchall()
    user_answer = result[0][0].strip()
    return user_answer

def get_data_fromQuery(user_Query):
    Data_dit={"TableColumnHeadings":[],"TableRowData":[]}
    data=[]
    cursor.execute(user_Query)
    column_headings = [col[0] for col in cursor.description]
    for i in cursor:
        data.append(list(i))
    Data_dit["TableColumnHeadings"]=column_headings
    Data_dit["TableRowData"]=data
    return Data_dit