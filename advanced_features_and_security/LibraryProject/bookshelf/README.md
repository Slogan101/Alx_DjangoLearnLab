# Group & Permission Setup in Django App

## Custom Permissions on `Book` model

Defined in `Book.Meta.permissions`:
- `can_view`: View books
- `can_create`: Create books
- `can_edit`: Edit books
- `can_delete`: Delete books

## Groups

- **Viewers**
  - Permissions: `can_view`

- **Editors**
  - Permissions: `can_view`, `can_create`, `can_edit`

- **Admins**
  - Permissions: All (view, create, edit, delete)

## Usage in Views

Views are protected using `@permission_required` decorators. Example:

```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_view(request):
    ...
