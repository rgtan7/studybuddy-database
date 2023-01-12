import psycopg2
import pandas as pd 

def getdblocation():
     # Define your connection details
    db = psycopg2.connect(
        # Get your credentials from the pgadmin. More details below.
        host='localhost',
        database='StudyBuddy',
        user='postgres',
        port=5432,
        password='Toothless56'
    )
    # return the c
    return db 

def modifydatabase(sql, values):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()
    
def querydatafromdatabase(sql, values, dfcolumns):
    #fpr Selecting commands 
    # ARGUMENTS
    # sql -- sql query with placeholders (%s)
    # values -- values for the placeholders
    # dfcolumns -- column names for the output
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows
