import streamlit as st
import random

# Sample data for books
books_data = [
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "price": 10.99, "image_url": "https://images.pexels.com/photos/265158/pexels-photo-265158.jpeg"},
    {"title": "1984", "author": "George Orwell", "genre": "Science Fiction", "price": 9.99, "image_url": "https://images.pexels.com/photos/5634323/pexels-photo-5634323.jpeg"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "price": 12.99, "image_url": "https://images.pexels.com/photos/894853/pexels-photo-894853.jpeg"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic", "price": 11.99, "image_url": "https://images.pexels.com/photos/1191635/pexels-photo-1191635.jpeg"},
    {"title": "Moby-Dick", "author": "Herman Melville", "genre": "Classic", "price": 13.99, "image_url": "https://images.pexels.com/photos/1615222/pexels-photo-1615222.jpeg"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Fiction", "price": 10.99, "image_url": "https://images.pexels.com/photos/5480912/pexels-photo-5480912.jpeg"},
    {"title": "Jane Eyre", "author": "Charlotte Bronte", "genre": "Romance", "price": 12.99, "image_url": "https://images.pexels.com/photos/5591691/pexels-photo-5591691.jpeg"},
    {"title": "Animal Farm", "author": "George Orwell", "genre": "Political Satire", "price": 9.99, "image_url": "https://images.pexels.com/photos/60254/pexels-photo-60254.jpeg"},
    {"title": "Frankenstein", "author": "Mary Shelley", "genre": "Gothic", "price": 11.99, "image_url": "https://images.pexels.com/photos/39811/pexels-photo-39811.jpeg"},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "price": 15.99, "image_url": "https://images.pexels.com/photos/33044/silverdale-landscape-new-zealand.jpg"},
    {"title": "Dracula", "author": "Bram Stoker", "genre": "Gothic Horror", "price": 11.99, "image_url": "https://images.pexels.com/photos/5621941/pexels-photo-5621941.jpeg"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "price": 14.99, "image_url": "https://images.pexels.com/photos/1005237/pexels-photo-1005237.jpeg"},
    {"title": "The Odyssey", "author": "Homer", "genre": "Epic", "price": 12.99, "image_url": "https://images.pexels.com/photos/1743168/pexels-photo-1743168.jpeg"},
    {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "genre": "Gothic", "price": 10.99, "image_url": "https://images.pexels.com/photos/4080342/pexels-photo-4080342.jpeg"},
    {"title": "Wuthering Heights", "author": "Emily Bronte", "genre": "Gothic", "price": 12.99, "image_url": "https://images.pexels.com/photos/5527592/pexels-photo-5527592.jpeg"},
    {"title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical Fiction", "price": 17.99, "image_url": "https://images.pexels.com/photos/853237/pexels-photo-853237.jpeg"},
    {"title": "The Adventures of Huckleberry Finn", "author": "Mark Twain", "genre": "Adventure", "price": 11.99, "image_url": "https://images.pexels.com/photos/4414749/pexels-photo-4414749.jpeg"},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "genre": "Psychological Thriller", "price": 13.99, "image_url": "https://images.pexels.com/photos/302381/pexels-photo-302381.jpeg"},
    {"title": "Anna Karenina", "author": "Leo Tolstoy", "genre": "Romance", "price": 14.99, "image_url": "https://images.pexels.com/photos/5904781/pexels-photo-5904781.jpeg"},
    {"title": "The Count of Monte Cristo", "author": "Alexandre Dumas", "genre": "Adventure", "price": 12.99, "image_url": "https://images.pexels.com/photos/6011941/pexels-photo-6011941.jpeg"}
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

    def search_book(self, title, genre):
        results = self.books
        if title:
            results = [book for book in results if title.lower() in book.title.lower()]
        if genre and genre != "All":
            results = [book for book in results if genre.lower() == book.genre.lower()]
        return results

    def display_books(self, books):
        st.write("Books available in the store:")
        num_books = len(books)
        num_rows = (num_books + 3) // 4
        for i in range(num_rows):
            cols = st.columns(4)
            for j in range(4):
                idx = i * 4 + j
                if idx < num_books:
                    cols[j].image(books[idx]["image_url"], caption=f"{books[idx]['title']} by {books[idx]['author']} - {books[idx]['genre']} (${books[idx]['price']})", use_column_width=True)
                    if cols[j].button(f"Add to Cart: {books[idx]['title']}_{i}"):
                        st.session_state.shopping_cart.append(books[idx])
                        st.success(f"{books[idx]['title']} added to cart!")

class ShoppingCart:
    def __init__(self):
        if "shopping_cart" not in st.session_state:
            st.session_state.shopping_cart = []

    def display_cart(self):
        st.write("Items in your cart:")
        for i, item in enumerate(st.session_state.shopping_cart, 1):
            st.write(f"{i}. {item['title']} by {item['author']} - {item['genre']} (${item['price']})")

    def place_order(self, card_details):
        total = sum(book['price'] for book in st.session_state.shopping_cart)
        st.write(f"Total amount to pay: ${total}")
        st.write("Payment Method:")
        payment_method = st.radio("Select Payment Method", payment_methods)
        st.write(f"Payment method: {payment_method}")

        st.write("Card Details:")
        card_number = st.text_input("Card Number")
        exp_date, cvv = st.columns(2)
        expiry_date = exp_date.text_input("Expiry Date", max_chars=5)
        cvv_code = cvv.text_input("CVV", max_chars=3)

        if st.button("Place Order"):
            st.write("Order placed successfully!")
            st.session_state.shopping_cart = []

def main():
    st.set_page_config(page_title="Bookstore App", page_icon=":books:", layout="wide")

    # Background styling
    page_bg_img = '''
    <style>
    body {
    background-image: url("https://images.pexels.com/photos/6319887/pexels-photo-6319887.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260");
    background-size: cover;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

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
        bookstore.display_books(books_data)
    elif page == "Search":
        st.header("Search Books")
        search_query = st.text_input("Search by title:")
        genre = st.selectbox("Filter by genre:", ["All"] + list(set(book['genre'] for book in books_data)))
        if st.button("Search"):
            bookstore = Bookstore()
            search_results = bookstore.search_book(search_query, genre)
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
