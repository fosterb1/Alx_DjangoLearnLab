# Permissions and Groups Setup

## Groups Created:
- **Viewers**: can_view books
- **Editors**: can_view, can_create, can_edit books  
- **Admins**: can_view, can_create, can_edit, can_delete books

## Permissions Defined:
- `can_view`: View book listings
- `can_create`: Create new books
- `can_edit`: Edit existing books
- `can_delete`: Delete books

## Setup Commands:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py setup_groups