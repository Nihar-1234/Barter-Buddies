# API Contract

The agreement between the FastAPI backend and the React frontend. If an endpoint's shape changes, update this file in the same PR.

Field names in request bodies and responses are a starting point. Adjust them here first, then in code.

## Endpoints

| Method | Path | Owner | Request body | Returns | Notes |
|---|---|---|---|---|---|
| GET | `/feed?category=` | Vamsi | — | `200` list of listings | `category` is optional; omit it for all categories. |
| GET | `/listings/{id}` | Vamsi | — | `200` one listing | `404` if the listing doesn't exist. |
| POST | `/listings` | Vamsi | `{ title, description, category }` | `201` the created listing | Owner is taken from the JWT, not the body. |
| POST | `/wants` | Vamsi | `{ title, description, category }` | `201` the created want | Owner is taken from the JWT. Wants feed into matching. |
| GET | `/me` | Vamsi | — | `200` my profile, rank, stats | The profile of whoever the JWT belongs to. |
| GET | `/profiles/{id}` | Vamsi | — | `200` profile with reviews | `404` if the user doesn't exist. |
| GET | `/notifications` | Vamsi | — | `200` `{ unread: number }` | Unread count only. |
| GET | `/matches` | Abhyuday | — | `200` list of users with a score | Sorted best match first. Excludes the caller. |
| POST | `/exchanges` | Abhyuday | `{ to_user_id, offer, ask }` | `201` the created exchange | Starts in `proposed`. `400` if you propose to yourself. |
| GET | `/exchanges/{id}` | Abhyuday | — | `200` one exchange | `403` if you aren't one of the two parties. `404` if it doesn't exist. |
| GET | `/exchanges/mine` | Abhyuday | — | `200` `{ incoming, pending, active, closed }` | Each key is a list of exchanges. Register this route before `/exchanges/{id}` so `mine` isn't read as an id. |
| POST | `/exchanges/{id}/respond` | Abhyuday | `{ accept: boolean }` | `200` the updated exchange | Recipient only (`403` otherwise). `proposed` → `accepted` or `declined`. `409` if the exchange isn't `proposed`. |
| POST | `/exchanges/{id}/lock` | Abhyuday | — | `200` the updated exchange | Freezes the terms. `accepted` → `locked`. `409` from any other status. |
| POST | `/exchanges/{id}/complete` | Abhyuday | — | `200` the updated exchange | Both parties must call it. Stays `locked` until the second confirmation, then moves to `completed`. `409` if the exchange isn't `locked`. |
| POST | `/reviews` | Abhyuday | `{ exchange_id, rating, comment }` | `201` the created review | Only for a `completed` exchange you were part of. `409` if you've already reviewed it. |

## Auth

Every request sends:

```
Authorization: Bearer <supabase jwt>
```

The backend verifies the token with `SUPABASE_JWT_SECRET` and takes the user id from it. A missing, invalid or expired token returns `401`.

## Error shape

All errors return:

```json
{ "detail": "message" }
```

This matches FastAPI's default `HTTPException` output, so the frontend can always read `response.detail`.

## Status codes

| Code | Meaning |
|---|---|
| `200` | OK |
| `201` | Created (any POST that creates a new row) |
| `400` | Bad request: invalid or missing fields |
| `401` | No valid JWT |
| `403` | Valid JWT, but you aren't allowed to do this |
| `404` | Not found |
| `409` | Conflict: the action doesn't fit the current state (for example, locking an exchange that isn't accepted) |

## Exchange status

An exchange is always in exactly one of these five states:

| Status | Meaning |
|---|---|
| `proposed` | Sent, waiting for the recipient to respond |
| `accepted` | Recipient agreed; terms can still be discussed |
| `locked` | Terms are frozen; waiting for both sides to confirm completion |
| `completed` | Both sides confirmed; reviews are open |
| `declined` | Recipient said no (final) |

```
proposed ──► accepted ──► locked ──► completed
    │
    └──────► declined
```

## Not part of the API

These go from the browser directly to Supabase and never reach the backend:

- **Login**
- **Signup**
- **Chat**
