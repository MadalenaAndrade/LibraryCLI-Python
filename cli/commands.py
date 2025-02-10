from database.dbconnection import get_connection
from localization.localization import load_localization
import sys #to stop program if an input error occurs


loc = load_localization()

def book_exists(sn):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = "SELECT SerialNumber FROM LibraryHub.Book WHERE SerialNumber = ?"
        cursor.execute(query, (sn))
        result = cursor.fetchone()

        if result:
            return True
        else:
            return False
        
    except Exception as ex:
        print(loc["bookError"], ex)
        return False
    
    finally:
        if 'connection' in locals():
            connection.close()

#function to add new book
def addBook(sn:int, title:str, year:int, fine:float, publisher_id:int, amount:int, available_amount:int, category_id:int, author:str):
    if book_exists(sn):
        print(loc["bookExists"])
        return
    
    try:
        #create a connection
        connection = get_connection()
        cursor = connection.cursor()


        stored_procedure = "EXEC InsertBook ?, ?, ?, ?, ?, ?, ?, ?, ?"
        cursor.execute(stored_procedure, (sn, title, year, fine, publisher_id, amount, available_amount, category_id, author))

        #commit!
        connection.commit()

        #check if book was introduced with success
        if book_exists(sn):
            print(loc["bookAdded"])
        else:
            print(loc["bookNotAdded"].format(serial_number = loc["snField"]))

    except Exception as ex:
        print(loc["connectionError"], ex)
        connection.rollback()
    finally:
        if 'connection' in locals():
            connection.close()

#function to get book information
def getBook(sn, title, publisher, category, author):
    #check if user used more than one argument and gives an error if its the case. Appends any condition/parameter used
    parameters = []
    conditions = []
    
    if sn:
        conditions.append("Book.SerialNumber = ?")
        parameters.append(sn)
    if title:
        conditions.append("Book.Title = ?")
        parameters.append(title)
    if publisher:
        conditions.append("Publisher.Name = ?")
        parameters.append(publisher)    
    if category:
        conditions.append("Category.Name = ?")
        parameters.append(category) 
    if author:
        conditions.append("Author.Name = ?")
        parameters.append(author) 

    if not parameters:
        print(loc["criterionNumberError"])
        sys.exit()
    
    #join conditions with AND
    where_conditions = " AND ".join(conditions)

    query = f"""SELECT Book.Title, Author.Name AS Author, Book.Year, Book.FinePerDay, Publisher.Name AS Publisher 
            FROM LibraryHub.Book AS Book
            JOIN LibraryHub.BookAuthor AS BookAuthor 
            ON Book.SerialNumber = BookAuthor.SerialNumber
            JOIN LibraryHub.BookCategory AS BookCategory
            ON Book.SerialNumber = BookCategory.SerialNumber
            JOIN LibraryHub.Category AS Category
            ON BookCategory.CategoryID = Category.ID
            JOIN LibraryHub.Author AS Author 
            ON BookAuthor.AuthorID = Author.ID
            JOIN LibraryHub.Publisher AS Publisher
            ON Book.PublisherID = Publisher.ID 
            WHERE {where_conditions}
            ORDER BY Book.Title"""

    #make it work!
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, parameters)
        results = cursor.fetchall()

        if results:
            for row in results:
                print(row)
        else:
            print(loc["bookNotExist"])

    except Exception as ex:
        print(loc["connectionError"], ex)

    finally:
        if 'connection' in locals():
            connection.close()

#function to delete book information
def delBook(sn, copyid, condition):
    #check if user used more than one argument and gives an error if its the case. Appends any condition/parameter used
    parameters = []
    conditions = []
    
    if sn:
        conditions.append("BookCopy.SerialNumber = ?")
        parameters.append(sn)
    if copyid:
        conditions.append("BookCopy.ID = ?")
        parameters.append(copyid)
        
    if condition:
        if condition == "bad":
            conditions.append("BookCopy.BookConditionID = 4")
        if condition == "used":
            conditions.append("BookCopy.BookConditionID = 3")
        if condition == "good":
            conditions.append("BookCopy.BookConditionID = 2")
        if condition == "as new":
            conditions.append("BookCopy.BookConditionID = 1")
        parameters.append(condition) 

    if not parameters:
        print(loc["criterionNumberError"])
        return
    
    #join conditions with AND
    where_conditions = " AND ".join(conditions)

    query = f"""SELECT BookCopy.ID, Book.SerialNumber, Book.Title, Author.Name AS Author, Book.Year, Book.FinePerDay, BookCondition.Condition
            FROM LibraryHub.Book AS Book
            JOIN LibraryHub.BookAuthor AS BookAuthor 
            ON Book.SerialNumber = BookAuthor.SerialNumber
            JOIN LibraryHub.Author AS Author 
            ON BookAuthor.AuthorID = Author.ID
            JOIN LibraryHub.BookCopy AS BookCopy
			ON Book.SerialNumber = BookCopy.SerialNumber
			JOIN LibraryHub.BookCondition AS BookCondition
			ON BookCondition.ID = BookCopy.BookConditionID
            WHERE {where_conditions}
            ORDER BY Book.SerialNumber"""

    #make it work but with caution!
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, parameters)
        results = cursor.fetchall()

        if not results:
            print(loc["bookNotExist"])
            return
    
        print("\n", loc["delBookHeading"])
        for row in results:
            print(row)
        
        print("\n", loc["doubleCheckDeleting"])

        while True:
            proceed_question = input(loc["yesOrNo"]).strip().lower()
            if proceed_question == loc["No"]:
                print(loc["cancelDel"])
                return
            elif proceed_question == loc["Yes"]: #relantionships must be in cascade, need to resolve bug
                delete_query = f"""DELETE FROM LibraryHub.BookCopy
                            WHERE {where_conditions}"""
                cursor.execute(delete_query, parameters)
                print(loc["delConfirmed"])
                break
            else:
                print(loc["InvalidAnswerError"])

    except Exception as ex:
        print(loc["connectionError"], ex)

    finally:
        if 'connection' in locals():
            connection.close()