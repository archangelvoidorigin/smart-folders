# Smart Folder: API Service

## Purpose
Build and maintain the REST API. Contains all routes, models, services, database logic, and tests. Defines the contract that the frontend consumes.

## Role
- **Name**: Architect
- **Description**: The blueprint room — the API is the contract; its shape determines everything downstream
- **Level**: 1
- **Depth**: medium

## Scope
**CAN do**:
- Create and modify API routes, models, and services
- Write database migrations and queries
- Write API tests (unit and integration)
- Define request/response TypeScript types
- Document API endpoints in `docs/api.md`

**CANNOT do**:
- Modify frontend code (that belongs in `web-app/`)
- Change the public API contract without updating `docs/api.md` and notifying `web-app/`
- Use ORM magic that hides SQL queries — all queries must be readable
- Add authentication schemes without updating security documentation

## Boundaries
- **CAN see**: ["*.ts", "*.js", "*.json", "*.sql", "*.md", "*.yaml"]
- **CANNOT see**: ["node_modules/", "dist/", ".env", ".env.*", "*.log", "secrets/"]
- **Token budget**: 10000
- **File limit**: 250

## Instructions
1. Routes go in `src/routes/` — one file per resource (users.ts, products.ts, etc.)
2. Business logic goes in `src/services/` — routes must not contain logic
3. Database models go in `src/models/`
4. All database access goes through `src/db/` — no direct SQL in routes or services
5. Export all request/response types from `src/types/` — the frontend imports from here
6. Every endpoint must be tested in `src/__tests__/`
7. Every change to the public API must update `docs/api.md` — treat this as a contract

## Context
- **Parent folder**: ../../smart-folder.md
- **Child folders**:
  - `src/routes/` — HTTP route handlers
  - `src/services/` — Business logic
  - `src/models/` — Database models
  - `src/types/` — Shared TypeScript types (consumed by web-app/)
- **Related folders**: `web-app/` (consumer of this API), `knowledge-base/` (patterns)
- **Tools available**: generate, test, document, migrate

## Connections
- **Feeds into**: `web-app/` (via types and runtime API)
- **Receives from**: `knowledge-base/` (architecture patterns)
- **Siblings**: `web-app/`

## Laws
- [ ] Never: put business logic in route handlers — it goes in services
- [ ] Never: write raw SQL outside `src/db/`
- [ ] Never: break the public API contract without a version bump
- [ ] Never: store secrets in code — use environment variables
- [ ] Always: write tests for every new endpoint
- [ ] Always: update `docs/api.md` when changing the public API
- [ ] Always: export new types from `src/types/` so the frontend can import them
- [ ] If: an endpoint changes its response shape, notify the web-app maintainer

## Metadata
- **Created**: 2026-06-23
- **Author**: ArchangelVoidOrigin
- **Version**: 1
- **Quality score**: 9
- **Last modified**: 2026-06-23
