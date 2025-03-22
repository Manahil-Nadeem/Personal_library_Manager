import streamlit as st
import json

# Initialize an empty library list
library = []

# Function to load library data from a file (if exists)
def load_library():
    global library
    try:
        with open("library.json", "r") as file:
            library = json.load(file)
    except FileNotFoundError:
        print("No saved library found, starting with an empty library.")

# Function to save library data to a file
def save_library():
    with open("library.json", "w") as file:
        json.dump(library, file)

# Function to add a book to the library
def add_book():
    st.header("Add a Book")
    title = st.text_input("Enter the book title")
    author = st.text_input("Enter the author")
    year = st.number_input("Enter the publication year", min_value=1000, max_value=9999)
    genre = st.text_input("Enter the genre")
    read_status = st.radio("Have you read this book?", ("Yes", "No"))

    if st.button("Add Book"):
        book = {
            'title': title,
            'author': author,
            'year': year,
            'genre': genre,
            'read': True if read_status == "Yes" else False
        }
        library.append(book)
        save_library()
        st.success(f"Book '{title}' added successfully!")

# Function to remove a book from the library
def remove_book():
    st.header("Remove a Book")
    title_to_remove = st.text_input("Enter the title of the book to remove")
    
    if st.button("Remove Book"):
        global library
        library = [book for book in library if book['title'].lower() != title_to_remove.lower()]
        save_library()
        st.success(f"Book '{title_to_remove}' removed successfully!")

# Function to search for a book by title or author
def search_book():
    st.header("Search for a Book")
    search_option = st.radio("Search by:", ("Title", "Author"))

    if search_option == "Title":
        title_to_search = st.text_input("Enter the title to search")
        if st.button("Search by Title"):
            results = [book for book in library if title_to_search.lower() in book['title'].lower()]
    else:
        author_to_search = st.text_input("Enter the author to search")
        if st.button("Search by Author"):
            results = [book for book in library if author_to_search.lower() in book['author'].lower()]

    if 'results' in locals() and results:
        st.write(f"### Matching Books ({len(results)} results found):")
        for book in results:
            read_status = "Read" if book['read'] else "Unread"
            st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    elif 'results' in locals():
        st.write("No matching books found.")

# Function to display all books in the library
def display_all_books():
    st.header("Your Library")
    if library:
        for book in library:
            read_status = "Read" if book['read'] else "Unread"
            st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    else:
        st.write("Your library is empty.")

# Function to display statistics about the library
def display_statistics():
    total_books = len(library)
    if total_books == 0:
        st.write("No books in the library.")
        return

    read_books = sum(1 for book in library if book['read'])
    unread_books = total_books - read_books
    percentage_read = (read_books / total_books) * 100

    st.write(f"Total books: {total_books}")
    st.write(f"Books read: {read_books}")
    st.write(f"Books unread: {unread_books}")
    st.write(f"Percentage read: {percentage_read:.1f}%")

# Streamlit app interface
def main():
    # Load library from file
    load_library()

    st.title("*Personal Library Manager!*")

    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Exit"]
    choice = st.sidebar.selectbox("*MENU🚀*", menu)

    if choice == "Add a Book":
        add_book()
    elif choice == "Remove a Book":
        remove_book()
    elif choice == "Search for a Book":
        search_book()
    elif choice == "Display All Books":
        display_all_books()
    elif choice == "Display Statistics":
        display_statistics()
    elif choice == "Exit":
        save_library()  # Save the library data to file
        st.write("🚀Library saved to file. Goodbye!")

if __name__ == "__main__":
    main()