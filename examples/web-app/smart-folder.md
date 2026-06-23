# Smart Folder: Web App

## Purpose
Build and maintain the React frontend. Contains all UI components, pages, styles, and client-side logic. Output here feeds directly into the deployable product.

## Role
- **Name**: Creator
- **Description**: The workshop — turns designs and requirements into working frontend code
- **Level**: 1
- **Depth**: medium

## Scope
**CAN do**:
- Create and modify React components, pages, hooks, and utilities
- Write CSS/Tailwind styles
- Write frontend tests (Jest, React Testing Library)
- Update package.json dependencies for frontend packages

**CANNOT do**:
- Modify backend API code (that belongs in `api-service/`)
- Make architecture decisions without reading `ARCHITECTURE.md` first
- Add packages without checking if equivalent functionality already exists

## Boundaries
- **CAN see**: ["*.tsx", "*.ts", "*.jsx", "*.js", "*.css", "*.json", "*.md"]
- **CANNOT see**: ["node_modules/", "dist/", "build/", ".cache/", "*.log", "*.env"]
- **Token budget**: 10000
- **File limit**: 300

## Instructions
1. All components go in `src/components/` — one file per component
2. Pages go in `src/pages/` — one file per route
3. Shared hooks go in `src/hooks/`
4. Follow the design system documented in `knowledge-base/` — do not invent new colors or spacing
5. Every new component must have a corresponding test in `src/__tests__/`
6. Use TypeScript — no `any` types
7. Accessibility: WCAG 2.1 AA minimum on all interactive elements

## Context
- **Parent folder**: ../../smart-folder.md
- **Child folders**:
  - `src/components/` — Reusable UI components
  - `src/pages/` — Route-level page components
  - `src/hooks/` — Custom React hooks
- **Related folders**: `knowledge-base/` (design patterns), `api-service/` (API contracts)
- **Tools available**: generate, refactor, test, lint

## Connections
- **Feeds into**: Deploy pipeline
- **Receives from**: `knowledge-base/` (design patterns), `api-service/` (API types)
- **Siblings**: `api-service/`

## Laws
- [ ] Never: use `any` TypeScript type
- [ ] Never: commit code that fails type checking or tests
- [ ] Never: duplicate a component that already exists in `src/components/`
- [ ] Always: write tests for new components
- [ ] Always: ensure WCAG 2.1 AA accessibility compliance
- [ ] Always: import API types from `api-service/` — never redefine them here
- [ ] If: a component needs data from the API, create a hook in `src/hooks/` — not inline

## Metadata
- **Created**: 2026-06-23
- **Author**: ArchangelVoidOrigin
- **Version**: 1
- **Quality score**: 9
- **Last modified**: 2026-06-23
