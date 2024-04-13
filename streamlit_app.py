import streamlit as st
import random

# Sample data for books
books_data = [
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "price": 10.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "1984", "author": "George Orwell", "genre": "Science Fiction", "price": 9.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "price": 12.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic", "price": 11.99, "image_url": "https://via.placeholder.com/150"},
    # Add more books here...
]

# Payment methods
payment_methods = ["Credit Card", "Debit Card", "PayPal"]

class Book:
    def __init__(self, title, author, genre, price, image_url):
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.image_url = image_url

class Bookstore:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_book(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def display_books(self):
        st.write("Books available in the store:")
        for i, book in enumerate(self.books):
            st.image(book.image_url, caption=f"{book.title} by {book.author} - {book.genre} (${book.price})", use_column_width=True)
            if st.button(f"Add to Cart: {book.title}_{i}"):
                st.session_state.shopping_cart.append(book)
                st.success(f"{book.title} added to cart!")

class ShoppingCart:
    def __init__(self):
        if "shopping_cart" not in st.session_state:
            st.session_state.shopping_cart = []

    def display_cart(self):
        st.write("Items in your cart:")
        for i, item in enumerate(st.session_state.shopping_cart, 1):
            st.write(f"{i}. {item.title} by {item.author} - {item.genre} (${item.price})")

    def place_order(self):
        total = sum(book.price for book in st.session_state.shopping_cart)
        st.write(f"Total amount to pay: ${total}")
        payment_method = st.selectbox("Select Payment Method", payment_methods)
        st.write(f"Payment method: {payment_method}")
        if st.button("Place Order"):
            st.write("Order placed successfully!")
            st.session_state.shopping_cart = []

def main():
    st.title("Bookstore")

    # Initialize shopping cart
    if "shopping_cart" not in st.session_state:
        st.session_state.shopping_cart = []

    page = st.sidebar.selectbox("Menu", ["Home", "Search", "Cart"])

    if page == "Home":
        st.header("Welcome to Bookstore")
        bookstore = Bookstore()
        for _ in range(10):
            book_data = random.choice(books_data)
            book = Book(**book_data)
            bookstore.add_book(book)
        bookstore.display_books()
    elif page == "Search":
        st.header("Search Books")
        search_query = st.text_input("Search for a book:")
        if st.button("Search"):
            bookstore = Bookstore()
            search_results = bookstore.search_book(search_query)
            if search_results:
                for i, book in enumerate(search_results):
                    st.image(book.image_url, caption=f"{book.title} by {book.author} - {book.genre} (${book.price})", use_column_width=True)
                    if st.button(f"Add to Cart: {book.title}_{i}"):
                        st.session_state.shopping_cart.append(book)
                        st.success(f"{book.title} added to cart!")
            else:
                st.write("No books found.")
    elif page == "Cart":
        st.header("Shopping Cart")
        shopping_cart = ShoppingCart()
        shopping_cart.display_cart()
        shopping_cart.place_order()

if __name__ == "__main__":
    main()
