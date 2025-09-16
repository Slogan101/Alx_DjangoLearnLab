# Authentication & Permissions

## Token Authentication

We use Django REST Framework's Token Authentication.

### Steps to Get a Token:
- Send POST request to `/api/token/` with username and password.
- Receive token in response.
- Use it in `Authorization` header as: `Token <your-token>`

## Permissions

By default:
- All views require authentication (`IsAuthenticated`)
- Admin-only views use `IsAdminUser`
- Custom permission `IsOwnerOrReadOnly` can be applied to limit editing to the object's owner.
