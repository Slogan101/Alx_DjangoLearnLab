## API Endpoints - Book

### Public Endpoints:
- `GET /api/books/` – List all books
- `GET /api/books/<id>/` – Retrieve book by ID

### Authenticated Endpoints:
- `POST /api/books/create/` – Create a new book
- `PUT /api/books/<id>/update/` – Update a book
- `DELETE /api/books/<id>/delete/` – Delete a book

### Permissions:
- Unauthenticated users: Read-only
- Authenticated users: Full CRUD
