import sqlite3


def create_database():
    conn = sqlite3.connect('User_info.db')
    cursor = conn.cursor()

    # query for user login
    create_table_query_1 = '''
    CREATE TABLE IF NOT EXISTS Authenticated (
        id INTEGER PRIMARY KEY,
        email TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    '''

    cursor.execute(create_table_query_1)
    conn.commit()
    conn.close()


def delete_all_accounts():
    conn = sqlite3.connect('User_info.db')
    cursor = conn.cursor()

    # query to delete all accounts
    delete_query = '''
    DELETE FROM Authenticated;
    '''

    cursor.execute(delete_query)
    conn.commit()
    conn.close()


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
    create_database()

    while True:
        print("Choose an operation:")
        print("1. Delete all accounts")
        print("2. Remove account by email")
        print("3. Exit")

        choice = input("Enter the operation number: ")

        if choice == '1':
            delete_all_accounts()
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
