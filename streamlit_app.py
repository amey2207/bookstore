import streamlit as st

class Book:
    def __init__(self, title, author, genre, price):
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price

class Bookstore:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def display_books(self):
        if not self.books:
            st.write("No books in the store yet!")
            return
        st.write("Books available in the store:")
        for i, book in enumerate(self.books, 1):
            st.write(f"{i}. {book.title} by {book.author} - {book.genre} (${book.price})")

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_to_cart(self, book):
        self.items.append(book)

    def display_cart(self):
        if not self.items:
            st.write("Your cart is empty!")
            return
        st.write("Items in your cart:")
        for i, item in enumerate(self.items, 1):
            st.write(f"{i}. {item.title} by {item.author} - {item.genre} (${item.price})")

    def place_order(self):
        total = sum(book.price for book in self.items)
        st.write(f"Total amount to pay: ${total}")
        confirm = st.radio("Confirm order?", ("Yes", "No"))
        if confirm == "Yes":
            st.write("Order placed successfully!")
            self.items = []
        else:
            st.write("Order canceled.")

def main():
    bookstore = Bookstore()
    shopping_cart = ShoppingCart()

    # Adding sample books
    bookstore.add_book(Book("To Kill a Mockingbird", "Harper Lee", "Fiction", 10.99))
    bookstore.add_book(Book("1984", "George Orwell", "Science Fiction", 9.99))
    bookstore.add_book(Book("Pride and Prejudice", "Jane Austen", "Romance", 12.99))

    st.title("Bookstore")

    option = st.sidebar.selectbox("Menu", ["Home", "Search", "View Cart", "Place Order"])

    if option == "Home":
        st.write("Welcome to the Bookstore!")
        st.write("Select an option from the sidebar.")
    elif option == "Search":
        st.header("Search for a Book")
        title = st.text_input("Enter the title of the book you want to search for:")
        if st.button("Search"):
            book = bookstore.search_book(title)
            if book:
                st.write(f"{book.title} by {book.author} - {book.genre} (${book.price})")
                if st.button("Add to Cart"):
                    shopping_cart.add_to_cart(book)
                    st.success("Book added to cart!")
            else:
                st.error("Book not found!")
    elif option == "View Cart":
        st.header("Shopping Cart")
        shopping_cart.display_cart()
    elif option == "Place Order":
        st.header("Place Your Order")
        shopping_cart.display_cart()
        if st.button("Place Order"):
            shopping_cart.place_order()

if __name__ == "__main__":
    main()
