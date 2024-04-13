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
                    with cols[j]:
                        if st.button(f"Add to Cart: {self.books[idx].title}"):
                            st.session_state.shopping_cart.append(self.books[idx])
                            st.experimental_set_query_params(view="cart")
                            st.success(f"{self.books[idx].title} added to cart!")

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
    st.title("Bookstore")
    page = st.experimental_get_query_params().get("view", ["home"])[0]

    if page == "search":
        search_query = st.text_input("Search for a book:")
        if st.button("Search"):
            # Search logic here
            pass
    elif page == "cart":
        shopping_cart = ShoppingCart()
        st.header("Shopping Cart")
        shopping_cart.display_cart()
    elif page == "order":
        shopping_cart = ShoppingCart()
        st.header("Place Your Order")
        shopping_cart.display_cart()
        if st.button("Place Order"):
            shopping_cart.place_order()
    else:
        bookstore = Bookstore()
        bookstore.display_books()

    st.sidebar.markdown("## Menu")
    if st.sidebar.button("Home"):
        st.experimental_set_query_params(view="home")
    if st.sidebar.button("Search"):
        st.experimental_set_query_params(view="search")
    if st.sidebar.button("View Cart"):
        st.experimental_set_query_params(view="cart")
    if st.sidebar.button("Place Order"):
        st.experimental_set_query_params(view="order")

if __name__ == "__main__":
    main()
