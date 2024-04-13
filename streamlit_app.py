import streamlit as st

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
        num_books = len(self.books)
        num_rows = (num_books + 3) // 4
        for i in range(num_rows):
            cols = st.columns(4)
            for j in range(4):
                idx = i * 4 + j
                if idx < num_books:
                    cols[j].image(self.books[idx].image_url, caption=f"{self.books[idx].title} by {self.books[idx].author} - {self.books[idx].genre} (${self.books[idx].price})", use_column_width=True)

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
    bookstore.add_book(Book("To Kill a Mockingbird", "Harper Lee", "Fiction", 10.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("1984", "George Orwell", "Science Fiction", 9.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("Pride and Prejudice", "Jane Austen", "Romance", 12.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 11.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("The Catcher in the Rye", "J.D. Salinger", "Classic", 9.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("Moby-Dick", "Herman Melville", "Adventure", 14.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 13.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "Fantasy", 15.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("The Da Vinci Code", "Dan Brown", "Thriller", 12.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("The Girl with the Dragon Tattoo", "Stieg Larsson", "Mystery", 10.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("The Hunger Games", "Suzanne Collins", "Young Adult", 9.99, "https://via.placeholder.com/150"))
    bookstore.add_book(Book("The Alchemist", "Paulo Coelho", "Philosophical", 11.99, "https://via.placeholder.com/150"))

    st.title("Bookstore")

    search_query = st.text_input("Search for a book:")

    if st.button("Search"):
        book = bookstore.search_book(search_query)
        if book:
            st.write(f"{book.title} by {book.author} - {book.genre} (${book.price})")
            if st.button("Add to Cart"):
                shopping_cart.add_to_cart(book)
                st.success("Book added to cart!")
        else:
            st.error("Book not found!")

    st.write("Books available in the store:")
    bookstore.display_books()

    option = st.sidebar.selectbox("Menu", ["View Cart", "Place Order"])

    if option == "View Cart":
        st.header("Shopping Cart")
        shopping_cart.display_cart()
    elif option == "Place Order":
        st.header("Place Your Order")
        shopping_cart.display_cart()
        if st.button("Place Order"):
            shopping_cart.place_order()

if __name__ == "__main__":
    main()
