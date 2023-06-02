import json
import mysql.connector

# load the database configuration from the file
with open('data_base\database_config.json') as f:
    config = json.load(f)

# connectaion to the database
connection = mysql.connector.connect(
    host=config['host'],  # the host ip address or name
    user=config['user'],  # the user name to connect with
    password=config['password'],  # the password of the user
    database=config['database']  # the database name
    )

cursor = connection.cursor()
print("Connected to the database successfully")

def craate_database():
   
    cursor.execute('''
    CREATE TABLE AuthorizedEmails (
        ID INT PRIMARY KEY AUTO_INCREMENT,
        Email VARCHAR(255) UNIQUE NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE RequestedFiles (
        FileID VARCHAR(255) PRIMARY KEY,
        FileSize BIGINT
    );
    ''')

    cursor.execute('''
    CREATE TABLE ReturnedFiles (
        FileID VARCHAR(255) PRIMARY KEY,
        RequestedFileID VARCHAR(255),
        CreationDate DATETIME,
        FOREIGN KEY (RequestedFileID) REFERENCES RequestedFiles(FileID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE Requests (
        RequestID INT AUTO_INCREMENT PRIMARY KEY,
        Email VARCHAR(255),
        Name VARCHAR(255),
        RequestedFileID VARCHAR(255),
        ReturnedFileID VARCHAR(255),
        RequestDate DATETIME,
        IsCopied BIT,
        FolderID VARCHAR(255),
        FOREIGN KEY (RequestedFileID) REFERENCES RequestedFiles(FileID),
        FOREIGN KEY (ReturnedFileID) REFERENCES ReturnedFiles(FileID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE ActiveFiles (
        ReturnedFileID VARCHAR(255) PRIMARY KEY,
        RequestedFileID VARCHAR(255),
        FOREIGN KEY (ReturnedFileID) REFERENCES ReturnedFiles(FileID),
        FOREIGN KEY (RequestedFileID) REFERENCES RequestedFiles(FileID)
    );
    ''')

    print("Tables created successfully")


def add_authorized_email(email):
    cursor.execute('''
    INSERT INTO AuthorizedEmails (Email)
    VALUES (%s)
    ''', (email,))

    connection.commit()
    print("Email added successfully:", email)

def update_folder_column():

    cursor.execute('ALTER TABLE Requests ADD COLUMN IsFolder BOOLEAN')
        # Update new column
    cursor.execute('UPDATE Requests SET IsFolder = 1 WHERE FolderID IS NOT NULL')
        # Remove old column
    cursor.execute('ALTER TABLE Requests DROP COLUMN FolderID')

    connection.commit()
    print("Column updated successfully")



#craate_database()

add_authorized_email("yuiui7776@gmail.com")
#cursor.execute("SET time_zone='+02:00';")  # Adjust this to '+03:00' for Israel Daylight Saving Time
#update_folder_column()
connection.commit()

connection.close()
print("Connection closed")