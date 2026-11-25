from library import Library


def main():
    library = Library()

    while True:
        print("\n LIBRARY MANAGEMENT ")
        print("1. View all books")
        print("2. Add book")
        print("3. Search book")
        print("4. Delete book")
        print("5. Register member")
        print("6. View members")
        print("7. Issue book")
        print("8. Return book")
        print("9. Delete member")
        print("0. Save and exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            library.display_books()
        elif choice == "2":
            title = input("Book title: ").strip()
            author = input("Author: ").strip()
            library.add_book(title, author)
        elif choice == "3":
            query = input("Enter book ID, title, or author: ").strip()
            library.search_books(query)
        elif choice == "4":
            book_id = input("Book ID to delete: ").strip()
            library.delete_book(book_id)
        elif choice == "5":
            name = input("Member name: ").strip()
            library.register_member(name)
        elif choice == "6":
            library.display_members()
        elif choice == "7":
            member_id = input("Member ID: ").strip()
            book_id = input("Book ID: ").strip()
            library.issue_book(member_id, book_id)
        elif choice == "8":
            member_id = input("Member ID: ").strip()
            book_id = input("Book ID: ").strip()
            library.return_book(member_id, book_id)
        elif choice == "9":
            member_id = input("Member ID to delete: ").strip()
            library.delete_member(member_id)
        elif choice == "0":
            library.save_data()
            print("Data saved!!")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()
