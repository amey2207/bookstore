import streamlit as st
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('bookstore.db')
c = conn.cursor()

# Create a table to store books if it doesn't exist already
c.execute('''CREATE TABLE IF NOT EXISTS books
             (title TEXT, author TEXT, genre TEXT, price REAL, image_url TEXT)''')

# Sample data for books
books_data = [
    ("To Kill a Mockingbird", "Harper Lee", "Fiction", 10.99, "https://images.pexels.com/photos/265158/pexels-photo-265158.jpeg"),
    ("1984", "George Orwell", "Science Fiction", 9.99, "https://images.pexels.com/photos/5634323/pexels-photo-5634323.jpeg"),
    ("Pride and Prejudice", "Jane Austen", "Romance", 12.99, "https://images.pexels.com/photos/894853/pexels-photo-894853.jpeg"),
    # Add more books here
]

# Function to add books to the database
def add_books_to_db(books):
    c.executemany('INSERT INTO books VALUES (?, ?, ?, ?, ?)', books)
    conn.commit()

# Function to fetch books from the database
def fetch_books_from_db(title=None, genre=None):
    if title:
        query = f"SELECT * FROM books WHERE title LIKE '%{title}%'"
    elif genre:
        query = f"SELECT * FROM books WHERE genre='{genre}'"
    else:
        query = "SELECT * FROM books"
    return c.execute(query).fetchall()

# Function to display books in Streamlit
def display_books(books):
    st.write("Books available in the store:")
    num_books = len(books)
    num_rows = (num_books + 3) // 4
    for i in range(num_rows):
        cols = st.columns(4)
        for j in range(4):
            idx = i * 4 + j
            if idx < num_books:
                book = books[idx]
                cols[j].image(book[4], caption=f"{book[0]} by {book[1]} - {book[2]} (${book[3]})", use_column_width=True)
                if cols[j].button(f"Add to Cart: {book[0]}_{idx}"):
                    st.session_state.shopping_cart.append(book)
                    st.success(f"{book[0]} added to cart!")

# Initialize shopping cart
if "shopping_cart" not in st.session_state:
    st.session_state.shopping_cart = []

# Add sample books to the database
add_books_to_db(books_data)

# Main function
def main():
    st.set_page_config(page_title="Bookstore App", page_icon=":books:", layout="wide")

    page = st.sidebar.selectbox("Menu", ["Home", "Search", "Cart"])

    if page == "Home":
        st.header("Welcome to Bookstore")
        books = fetch_books_from_db()
        display_books(books)
    elif page == "Search":
        st.header("Search Books")
        search_query = st.text_input("Search by title:")
        genre = st.selectbox("Filter by genre:", ["All"] + list(set(book[2] for book in books_data)))
        if st.button("Search"):
            books = fetch_books_from_db(title=search_query, genre=genre)
            if books:
                display_books(books)
            else:
                st.write("No books found.")
    elif page == "Cart":
        st.header("Shopping Cart")
        st.write("Items in your cart:")
        for i, item in enumerate(st.session_state.shopping_cart, 1):
            st.write(f"{i}. {item[0]} by {item[1]} - {item[2]} (${item[3]})")

if __name__ == "__main__":
    main()
