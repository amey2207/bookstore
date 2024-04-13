import streamlit as st

# Sample data for books
books_data = [
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "price": 10.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "1984", "author": "George Orwell", "genre": "Science Fiction", "price": 9.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "price": 12.99, "image_url": "https://via.placeholder.com/150"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic", "price": 11.99, "image_url": "https://via.placeholder.com/150"},
    # Add more books here...
]

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
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def display_books(self):
        if not self.books:
            st.write("No books in the store yet!")
            return
        st.write("Books available in the store:")
        for book in self.books:
            st.image(book.image_url, caption=f"{book.title} by {book.author} - {book.genre} (${book.price})", use_column_width=True)
            if st.button(f"Add to Cart: {book.title}"):
                st.session_state.shopping_cart.append(book)
                st.experimental_set_query_params(view="cart")
                st.success(f"{book.title} added to cart!")

class ShoppingCart:
    def __init__(self):
        if "shopping_cart" not in st.session_state:
            st.session_state.shopping_cart = []

    def display_cart(self):
        if not st.session_state.shopping_cart:
            st.write("Your cart is empty!")
            return
        st.write("Items in your cart:")
        for i, item in enumerate(st.session_state.shopping_cart, 1):
            st.write(f"{i}. {item.title} by {item.author} - {item.genre} (${item.price})")

    def place_order(self):
        total = sum(book.price for book in st.session_state.shopping_cart)
        st.write(f"Total amount to pay: ${total}")
        confirm = st.radio("Confirm order?", ("Yes", "No"))
        if confirm == "Yes":
            st.write("Order placed successfully!")
            st.session_state.shopping_cart = []
        else:
            st.write("Order canceled.")

def main():
    st.title("Bookchor")

    # Initialize shopping cart
    if "shopping_cart" not in st.session_state:
        st.session_state.shopping_cart = []

    page = st.experimental_get_query_params().get("view", ["home"])[0]

    if page == "search":
        st.header("Search Books")
        search_query = st.text_input("Search for a book:")
        if st.button("Search"):
            # Search logic here
            pass
    elif page == "cart":
        st.header("Shopping Cart")
        shopping_cart = ShoppingCart()
        shopping_cart.display_cart()
        if st.button("Place Order"):
            shopping_cart.place_order()
    else:
        st.header("Welcome to Bookchor")
        bookstore = Bookstore()
        for book_data in books_data:
            book = Book(**book_data)
            bookstore.add_book(book)
        bookstore.display_books()

    st.sidebar.markdown("## Menu")
    if st.sidebar.button("Home"):
        st.experimental_set_query_params(view="home")
    if st.sidebar.button("Search"):
        st.experimental_set_query_params(view="search")
    if st.sidebar.button("View Cart"):
        st.experimental_set_query_params(view="cart")

if __name__ == "__main__":
    main()
