const API_URL = "/books";

document.addEventListener("DOMContentLoaded", loadBooks);
document.getElementById("book-form").addEventListener("submit", saveBook);

function loadBooks() {
  fetch(API_URL)
    .then((res) => res.json())
    .then((data) => {
      const tbody = document.getElementById("book-list");
      tbody.innerHTML = "";
      data.forEach((book) => {
        const row = `
          <tr>
            <td>${book.title}</td>
            <td>${book.author}</td>
            <td>${book.isbn}</td>
            <td>${book.published_year}</td>
            <td>
              <button class="btn btn-sm btn-warning" onclick='editBook(${JSON.stringify(
                book
              )})'>Edit</button>
              <button class="btn btn-sm btn-danger" onclick='deleteBook(${
                book.id
              })'>Delete</button>
            </td>
          </tr>`;
        tbody.innerHTML += row;
      });
    });
}

function saveBook(e) {
  e.preventDefault();
  const id = document.getElementById("book-id").value;
  const book = {
    title: document.getElementById("title").value,
    author: document.getElementById("author").value,
    isbn: document.getElementById("isbn").value,
    published_year: parseInt(document.getElementById("published_year").value),
  };

  const method = id ? "PUT" : "POST";
  const url = id ? `${API_URL}/${id}` : API_URL;

  fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(book),
  }).then(() => {
    resetForm();
    loadBooks();
  });
}

function deleteBook(id) {
  if (confirm("Are you sure you want to delete this book?")) {
    fetch(`${API_URL}/${id}`, { method: "DELETE" }).then(() => loadBooks());
  }
}

function editBook(book) {
  document.getElementById("book-id").value = book.id;
  document.getElementById("title").value = book.title;
  document.getElementById("author").value = book.author;
  document.getElementById("isbn").value = book.isbn;
  document.getElementById("published_year").value = book.published_year;
}

function resetForm() {
  document.getElementById("book-id").value = "";
  document.getElementById("book-form").reset();
}
