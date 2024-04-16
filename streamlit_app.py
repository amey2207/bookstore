import streamlit as st
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bookstore"]
collection = db["books"]

class Book:
    def __init__(self, title, author, genre, price, image_url):
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.image_url = image_url

class Bookstore:
    def __init__(self):
        pass

    def add_book(self, book):
        collection.insert_one(book.__dict__)

    def search_book(self, title):
        return [Book(**book) for book in collection.find({"title": {"$regex": title, "$options": "i"}})]

    def display_books(self, books):
        st.write("Books available in the store:")
        num_books = len(books)
        num_rows = (num_books + 3) // 4
        for i in range(num_rows):
            cols = st.columns(4)
            for j in range(4):
                idx = i * 4 + j
                if idx < num_books:
                    cols[j].image(books[idx].image_url, caption=f"{books[idx].title} by {books[idx].author} - {books[idx].genre} (${books[idx].price})", use_column_width=True)
                    if cols[j].button(f"Add to Cart: {books[idx].title}_{i}"):
                        st.session_state.shopping_cart.append(books[idx])
                        st.success(f"{books[idx].title} added to cart!")

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
        st.write("Payment Method:")
        payment_method = st.radio("Select Payment Method", payment_methods)
        st.write(f"Payment method: {payment_method}")
        if st.button("Place Order"):
            st.write("Order placed successfully!")
            st.session_state.shopping_cart = []

def main():
    st.set_page_config(page_title="Bookstore App", page_icon=":books:", layout="wide")

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
        bookstore.display_books(bookstore.search_book(None))
    elif page == "Search":
        st.header("Search Books")
        search_query = st.text_input("Search by title:")
        if st.button("Search"):
            bookstore = Bookstore()
            search_results = bookstore.search_book(search_query)
            if search_results:
                bookstore.display_books(search_results)
            else:
                st.write("No books found.")
    elif page == "Cart":
        st.header("Shopping Cart")
        shopping_cart = ShoppingCart()
        shopping_cart.display_cart()
        card_details = st.empty()
        shopping_cart.place_order(card_details)

if __name__ == "__main__":
    main()
