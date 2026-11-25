from pathlib import Path
from storage import load_json, save_json

DATA_DIR = Path(__file__).parent / "data"


class Library:
    def __init__(self):
        self.books = load_json(DATA_DIR / "books.json", [])
        self.members = load_json(DATA_DIR / "members.json", [])
        self.loans = load_json(DATA_DIR / "loans.json", [])
        self.next_book_id = self._next_id(self.books, "B")
        self.next_member_id = self._next_id(self.members, "M")

    @staticmethod
    def _next_id(items, prefix):
        numbers = []
        for item in items:
            value = item.get("id", "")
            if value.startswith(prefix) and value[1:].isdigit():
                numbers.append(int(value[1:]))
        return max(numbers, default=0) + 1

    def save_data(self):
        save_json(DATA_DIR / "books.json", self.books)
        save_json(DATA_DIR / "members.json", self.members)
        save_json(DATA_DIR / "loans.json", self.loans)

    def add_book(self, title, author):
        if not title or not author:
            print("Title and author are required.")
            return

        book = {
            "id": f"B{self.next_book_id:03}",
            "title": title,
            "author": author,
            "available": True,
        }
        self.next_book_id += 1
        self.books.append(book)
        self.save_data()
        print(f"Book added successfully. Book ID: {book['id']}")

    def display_books(self):
        if not self.books:
            print("No books found. Add a book first.")
            return

        print("\nID      TITLE                         AUTHOR                  STATUS")
        print("-" * 76)
        for book in self.books:
            status = "Available" if book["available"] else "Issued"
            print(f"{book['id']:<7} {book['title'][:28]:<29} {book['author'][:22]:<23} {status}")

    def search_books(self, query):
        if not query:
            print("Please enter a book ID, title, or author.")
            return

        search_text = query.casefold()
        results = [
            book for book in self.books
            if search_text in book["id"].casefold()
            or search_text in book["title"].casefold()
            or search_text in book["author"].casefold()
        ]

        if not results:
            print("No matching books found.")
            return

        for book in results:
            status = "Available" if book["available"] else "Issued"
            print(f"{book['id']} | {book['title']} | {book['author']} | {status}")

    def delete_book(self, book_id):
        for book in self.books:
            if book["id"].casefold() == book_id.casefold():
                if not book["available"]:
                    print("Cannot delete a book that is currently issued.")
                    return
                self.books.remove(book)
                self.save_data()
                print("Book deleted successfully.")
                return
        print("Book ID not found.")

    def register_member(self, name):
        if not name:
            print("Member name is required.")
            return

        member = {"id": f"M{self.next_member_id:03}", "name": name}
        self.next_member_id += 1
        self.members.append(member)
        self.save_data()
        print(f"Member registered successfully. Member ID: {member['id']}")

    def display_members(self):
        if not self.members:
            print("No members registered yet.")
            return

        print("\nMEMBER ID   NAME")
        print("-" * 30)
        for member in self.members:
            print(f"{member['id']:<11} {member['name']}")

    def delete_member(self, member_id):
        if not member_id:
            print("Please enter a member ID.")
            return

        member = None
        for item in self.members:
            if item["id"].casefold() == member_id.casefold():
                member = item
                break

        if member is None:
            print("Member ID not found.")
            return

        
        for loan in self.loans:
            if (loan["member_id"].casefold() == member["id"].casefold()
                    and loan["status"] == "Issued"):
                print("This member still has an issued book. Return it first.")
                return

        self.members.remove(member)
        self.save_data()
        print(f"Member {member['name']} deleted successfully.")

    def issue_book(self, member_id, book_id):
        member = next(
            (item for item in self.members if item["id"].casefold() == member_id.casefold()),
            None,
        )
        book = next(
            (item for item in self.books if item["id"].casefold() == book_id.casefold()),
            None,
        )

        if member is None:
            print("Member ID not found. Register the member first.")
            return
        if book is None:
            print("Book ID not found.")
            return
        if not book["available"]:
            print("This book is already issued and is not available.")
            return

        book["available"] = False
        self.loans.append({
            "member_id": member["id"],
            "book_id": book["id"],
            "book_title": book["title"],
            "status": "Issued",
        })
        self.save_data()
        print(f"'{book['title']}' issued successfully to {member['name']}.")

    def return_book(self, member_id, book_id):
        loan = next(
            (
                item for item in self.loans
                if item["member_id"].casefold() == member_id.casefold()
                and item["book_id"].casefold() == book_id.casefold()
                and item["status"] == "Issued"
            ),
            None,
        )
        book = next(
            (item for item in self.books if item["id"].casefold() == book_id.casefold()),
            None,
        )

        if loan is None or book is None:
            print("No active issue record found for that member and book.")
            return

        loan["status"] = "Returned"
        book["available"] = True
        self.save_data()
        print(f"'{book['title']}' returned successfully. It is now available.")
