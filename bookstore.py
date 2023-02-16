import sqlite3
from tabulate import tabulate


def title(heading):
    """ Sets the heading styling for each page.
    :param heading: Title content.
    """
    print(f"\n{bright_grey}-----------------------------------------------------\n{end}"
          f"{bold_red}\t\t{heading}{end}\n")


def choose_a_book():
    """ Allows the user to search for a book by using the author, book title or ID number fields.
    :return field_of_search: (str) The field chosen to select a book.
    :return modify_information: (str) The chosen book value of that field.
    """
    field_of_search = ""
    modify_information = ""
    table_headers = ["Author", "Title", "ID"]

    # Loops until either information is entered in a relevant field or the user wishes to return to the main menu.
    while modify_information == "":
        field_of_search = input("What would you like to enter to search for a book: \n"
                                f"   {bright_green}Author\t   {bright_red}Title\t   {bright_blue}ID\t\t"
                                f"{purple}>>>{end}  ")

        # Displays the library to offer users the required data.
        if field_of_search == "library":
            view_library()

        # Invalid entry outside of fields in the table.
        elif field_of_search not in table_headers:
            print(f"\n\n{red}Please enter a relevant search field such as{end}: Author{red},{end} Title {red}or{end} "
                  f"ID."
                  f"\nTo view all of the books, enter {green}library{end}.\n\n")

        # If inputs are relevant.
        else:
            modify_information = (input("\nPlease enter the " + field_of_search + " of the book: "),)
    return field_of_search, modify_information


def search_books():
    """ Searches the database for a specific book.
    :return: (tuple) The book required.
    """
    book_field, book_value = choose_a_book()
    if book_value != "menu":
        while True:
            cursor.execute('''SELECT * FROM books WHERE ''' + book_field + ''' = ?''', book_value)
            found_book = cursor.fetchone()

            # If the book was not found ask the user to try again or return to the main menu.
            if found_book is None:
                re_enter = input(f"{red}There are no books with that " + book_field + f" on the system.\n{end}\n"
                                 f"Would you like to try again?\n "
                                 f"\t{yellow}Yes{end}/{yellow}No{end}\t\t"
                                 f"{purple}>>>{end}  ").lower()

                # Re-enter information to choose a book.
                if re_enter == "yes":
                    print(f"\n{bright_grey}-----------------------------------------------------\n{end}")
                    book_field, book_value = choose_a_book()

                # Returns to home page.
                elif re_enter == "no":
                    if menu_selection == "3" or "2":
                        found_book = str("NoneType override")
                        return book_field, book_value, found_book

            # Returns the book.
            else:
                # If accessed via the delete page, also provide the searched field and value for the deletion
                # process.
                if menu_selection == "3" or "2":
                    return book_field, book_value, found_book

                return found_book


def delete_book():
    """ Remove a book entry from the library. """
    book_field, book_value, book_to_delete = search_books()
    # Confirmation of deleting the book.
    confirmation = input(f"\nAre you sure you wish to {red}delete{end}:    "
                         f"" + str(book_to_delete[1]) + " by " + str(book_to_delete[2]) +
                         f"\n\t{yellow}Yes{end}/{yellow}No{end}\t\t"
                         f"{purple}>>>{end}  ").lower()

    if confirmation.lower() == "yes":
        cursor.execute('''DELETE FROM books WHERE ''' + book_field + ''' = ?''', book_value)
        print(f"\n{book_to_delete[1]} has been deleted.")

    else:
        print("\nReturning to menu.")


def view_library():
    """ Display records of all books within the library. """
    # Database header.
    book_library = [["ID", "Title", "Author", "Quantity"]]
    cursor.execute('''SELECT * FROM books''')
    all_books = cursor.fetchall()

    # Organise book data into a list where it can be printed as a table.
    for book in all_books:
        book3 = []
        for info in book:
            book3.append(info)
        book_library.append(book3)

    print("\n")
    print(tabulate(book_library, headers="firstrow", tablefmt="pipe"))
    print("\n")


# Initialise connection to the database.
db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()


# Checking if the table already exists. If there is no database, the try runs and creates the database with 5 books.
try:
    # Creates the books table with all the necessary fields and assigns the primary key.
    cursor.execute('''CREATE TABLE books (ID INTEGER PRIMARY KEY, Title STRING, Author STRING, Qty INTEGER)''')
    # Original books to be stored in the system.
    id1, title1, author1, qty1 = (3001, "A Tale of Two Cities", "Charles Dickens", 30)
    id2, title2, author2, qty2 = (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40)
    id3, title3, author3, qty3 = (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25)
    id4, title4, author4, qty4 = (3004, "The Lord of the Rings", "J.R.R. Tolkein", 37)
    id5, title5, author5, qty5 = (3005, "Alice in Wonderland", "Lewis Carroll", 12)

    # Packing the tuples together ready for insertion.
    library = ((id1, title1, author1, qty1), (id2, title2, author2, qty2), (id3, title3, author3, qty3),
               (id4, title4, author4, qty4), (id5, title5, author5, qty5))

    # Populates the library.
    cursor.executemany('''INSERT INTO books(ID, Title, Author, Qty) 
                          VALUES (?, ?, ?, ?)''', library)
    db.commit()
    print("\nWe have created a new e-bookstore.")

# If the table already exists, the except runs.
except sqlite3.OperationalError:
    print("\nYour e-bookstore has been found.")
finally:
    print("Now loading the library...")


# Styling variables.
green = '\033[32m'
cyan = '\033[36m'
red = '\033[31m'
purple = '\033[1;35m'
yellow = '\033[33m'
bright_grey = '\033[0;90m'
bright_blue = '\033[0;94m'
bright_green = '\033[0;92m'
bright_red = '\033[0;91m'
bright_yellow = '\033[0;93m'
bold_green = '\033[1;92m'
bold_red = '\033[1;91m'
end = '\033[0m'


# Bookstore menu.
while True:
    print(f"\n{bright_grey}-----------------------------------------------------\n{end}"
          f"{bold_green}\t\tBookstore - Electronic Library\n{end}")
    menu_selection = input(f"{purple}Choose an option:\n{end}"
                           "    1. Enter Book\n"
                           "    2. Update Book\n"
                           "    3. Delete Book\n"
                           "    4. Search Books\n"
                           "    5. View library\n"
                           "    6. Undo Last Edit\n"
                           "    0. Exit\n"
                           f"\n{purple} >>>  {end}")


    # Add a new book to the library.
    if menu_selection == "1":
        title("Add To Library")

        # Checks for the biggest book ID on record.
        cursor.execute('''SELECT MAX(ID) FROM books''')
        latest_book_id = cursor.fetchone()

        # Automatically creates a new ID for the new book and asks for the rest of the information.
        new_book_id = latest_book_id[0] + 1
        new_book_title = input("What is the name of the book: ")
        new_book_author = input("What is the authors name: ")
        new_book_quantity = input("How many copies of the book does the library hold: ")
        new_book = new_book_id, new_book_title, new_book_author, new_book_quantity

        # Adds the new book to the library and commits it to the database.
        cursor.execute('''INSERT INTO books(ID, Title, Author, Qty)
                          VALUES(?,?,?,?)''', new_book)
        db.commit()
        print("\nNew entry has been successfully recorded in the system.")


    # Update the quantity of a book.
    elif menu_selection == "2":
        title("Update Book Quantity")

        # Asks how the user would like to choose the book to update and stores the field used for the search, it's
        # value and the book itself. I returned field to make searches and updates easier throughout the program.
        field, value, update_book = search_books()

        # If the user wants to return to the main menu, the code to update the book is not run.
        if update_book == "NoneType override":
            print("\nReturning to the main menu.")

        # If a book is selected the update procedure begins.
        elif update_book is not None:
            updated_quantity = None
            print(f"\nThere are currently {green}{update_book[3]}{end} copies of the book.")

            # Menu for updating the quantity - adds or removes copies.
            add_or_remove = input(f"\n{bold_red}Would you like to: {end}\n"
                                  f"    1: Add new copies which were bought.\n"
                                  f"    2: Remove lost or stolen books from the system."
                                  f"\n{purple} >>>  {end}")

            # Adds copies to the system.
            if add_or_remove == "1":
                new_copies = int(input("\nHow many new copies were bought: "))
                updated_quantity = int(update_book[3]) + new_copies
                print(f"{green}{new_copies}{end} new copies of {green}{update_book[1]}{end} have been added to the "
                      f"system.")

            # Removes copies from the system.
            elif add_or_remove == "2":
                lost_copies = int(input("\nHow many were lost or stolen: "))
                updated_quantity = int(update_book[3]) - lost_copies
                print(f"{green}{lost_copies}{end} copies of {green}{update_book[1]}{end} have been removed from the "
                      f"system.")

            # Updates the new book quantity and commits it to the database.
            cursor.execute('''UPDATE books SET Qty = ? WHERE ''' + field + ''' = ?''', (updated_quantity, value[0]))
            db.commit()


    # Delete a book from the library.
    elif menu_selection == "3":
        title("Delete A Book")
        delete_book()
        db.commit()


    # Search the library for a book.
    elif menu_selection == "4":
        title("Find A Book")

        # Asks which book to search for and returns the data on it.
        result = search_books()

        # If the user wants to return to the main menu, the code to display a book is not run.
        if result[2] == "NoneType override":
            print("\nReturning to the main menu.")

        # The book information is printed in a table format.
        elif result is not None:
            book2 = [["ID", "Title", "Author", "Quantity"]]
            find_book = []

            for data in result[2]:
                find_book.append(data)

            book2.append(find_book)
            print("\n" + tabulate(book2, headers="firstrow", tablefmt="pipe"))


    # View entire library.
    elif menu_selection == "5":
        title("Entire Library")
        view_library()


    # Exit program.
    elif menu_selection == "0":
        print("Logging Out")
        db.close()
        break


    # Incorrect menu selection.
    else:
        print(f"\n{red}That menu choice is invalid, please try again.{end}")
