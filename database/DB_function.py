import sqlite3

conn = sqlite3.connect('User_info.db')
cursor = conn.cursor()


def create_file_database():
    create_table_query_files = '''
    CREATE TABLE IF NOT EXISTS UserFiles (
        id INTEGER PRIMARY KEY,
        UserID INTEGER,
        Name TEXT NOT NULL,
        Size INTEGER NOT NULL,
        Date TEXT NOT NULL,
        FileBytes BLOB,  -- Assuming this is for storing file content
        FOREIGN KEY (UserID) REFERENCES Authenticated(id)
    );
    '''
    cursor.execute(create_table_query_files)
    conn.commit()


def create_user_database(conn, cursor):
    # query for user login
    create_table_query_users = '''
    CREATE TABLE IF NOT EXISTS Authenticated (
        id INTEGER PRIMARY KEY,
        email TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    '''

    cursor.execute(create_table_query_users)
    conn.commit()


def delete_all_accounts(conn, cursor):
    # query to delete all accounts
    delete_query = '''
    DELETE FROM Authenticated;
    '''

    cursor.execute(delete_query)
    conn.commit()


def remove_account_by_email(email):
    conn = sqlite3.connect('User_info.db')
    cursor = conn.cursor()

    # query to remove account based on email
    remove_query = '''
    DELETE FROM Authenticated WHERE email = ?;
    '''

    cursor.execute(remove_query, (email,))
    conn.commit()
    conn.close()


def main():
    create_user_database(conn, cursor)
    create_file_database()
    print("create_file_database was created")

    while True:
        print("Choose an operation:")
        print("1. Delete all accounts")
        print("2. Remove account by email")
        print("3. Exit")

        choice = input("Enter the operation number: ")

        if choice == '1':
            delete_all_accounts(conn, cursor)
            print("All accounts deleted.")
        elif choice == '2':
            email_to_remove = input("Enter the email to remove: ")
            remove_account_by_email(email_to_remove)
            print(f"Account with email {email_to_remove} removed.")
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a valid operation number.")


if __name__ == "__main__":
    main()
