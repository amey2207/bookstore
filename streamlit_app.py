import streamlit as st
import random

# Sample data for books
books_data = [
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "price": 10.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "1984", "author": "George Orwell", "genre": "Science Fiction", "price": 9.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "price": 12.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic", "price": 11.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Moby-Dick", "author": "Herman Melville", "genre": "Classic", "price": 13.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Fiction", "price": 10.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Jane Eyre", "author": "Charlotte Bronte", "genre": "Romance", "price": 12.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Animal Farm", "author": "George Orwell", "genre": "Political Satire", "price": 9.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Frankenstein", "author": "Mary Shelley", "genre": "Gothic", "price": 11.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "price": 15.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Dracula", "author": "Bram Stoker", "genre": "Gothic Horror", "price": 11.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "price": 14.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "The Odyssey", "author": "Homer", "genre": "Epic", "price": 12.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "genre": "Gothic", "price": 10.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Wuthering Heights", "author": "Emily Bronte", "genre": "Gothic", "price": 12.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical Fiction", "price": 17.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "The Adventures of Huckleberry Finn", "author": "Mark Twain", "genre": "Adventure", "price": 11.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "genre": "Psychological Thriller", "price": 13.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Anna Karenina", "author": "Leo Tolstoy", "genre": "Romance", "price": 14.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "The Count of Monte Cristo", "author": "Alexandre Dumas", "genre": "Adventure", "price": 12.99, "image_url": "https://via.placeholder.com/150"}
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
        num_books = len(self.books)
        num_rows = (num_books + 3) // 4
        for i in range(num_rows):
            cols = st.columns(4)
            for j in range(4):
                idx = i * 4 + j
                if idx < num_books:
                    cols[j].image(self.books[idx].image_url, caption=f"{self.books[idx].title} by {self.books[idx].author} - {self.books[idx].genre} (${self.books[idx].price})", use_column_width=True)
                    if cols[j].button(f"Add to Cart: {self.books[idx].title}"):
                        st.session_state.shopping_cart.append(self.books[idx])
                        st.success(f"{self.books[idx].title} added to cart!")

class ShoppingCart:
    def __init__(self):
        if "shopping_cart" not in st.session_state:
            st.session_state.shopping_cart = []

    def display_cart(self):
        st.write("Items in your cart:")
        for i, item in enumerate(st.session_state.shopping_cart, 1):
            st.write(f"{i}. {item.title} by {item.author} - {item.genre} (${item.price})")

    def place_order(self, card_details):
        total = sum(book.price for book in st.session_state.shopping_cart)
        st.write(f"Total amount to pay: ${total}")
        payment_method = st.selectbox("Select Payment Method", payment_methods)
        st.write(f"Payment method: {payment_method}")
        st.write("Card Details:")
        st.write(card_details)
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
        for data in books_data:
            book = Book(**data)
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
        card_details = st.text_input("Enter your card details:")
        shopping_cart.place_order(card_details)

if __name__ == "__main__":
    main()
