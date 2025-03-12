# CLAUDE.md - Coding Assistant Guidelines

## Commands
- **Frontend Build/Run**: `npm install && npm run dev`
- **Backend Run**: `pip install -r requirements.txt && uvicorn app.main:app --reload`
- **Frontend Test**: `npm test`
- **Backend Test**: `pytest`
- **Test Single (Backend)**: `pytest path/to/test_file.py::test_function`
- **Test Single (Frontend)**: `npm test -- -t "test name"`
- **Lint Backend**: `black app/ && flake8 app/ && isort app/`
- **Lint Frontend**: `npm run lint`
- **Docker**: `docker-compose up -d`

## Development Methodology
- **TDD Approach**: Always write tests before implementation code
  - Red: Write failing test first
  - Green: Implement minimum code to pass test
  - Refactor: Clean up while keeping tests green
- **Code Coverage**: Aim for 85%+ test coverage
- **Continuous Testing**: Run tests frequently during development

## Code Style Guidelines
- **Frontend**: TypeScript, React, NextJS, TailwindCSS
  - ESLint + Prettier config
  - Variables/functions: camelCase, Components: PascalCase
  - Imports: grouped by type, alphabetized
  - Strong typing with TypeScript (no any)
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy
  - PEP 8 compliant (black/flake8)
  - Variables/functions: snake_case, Classes: PascalCase
  - Type hints required
  - Docstrings for all functions/classes
- **Architecture**: Clean architecture with layered approach
  - Microservices: auth, users, content, learning, analytics
  - JWT authentication
  - Error handling with specific error types

## GitHub Guidelines
- **Branch Strategy**: GitFlow-based (main, develop, feature/, bugfix/, release/, hotfix/)
- **Commit Format**: `type(scope): brief description` (types: feat, fix, docs, style, refactor, test, chore)
- **PR Process**: Use template, self-review, assign reviewers, mark "Ready for review"
- **CI/CD**: GitHub Actions runs linting, tests, build, coverage analysis on each PR
- **Contributors**: Fork repo, create branch, make changes, test, submit PR

## Math Specifics
- MathJax/KaTeX for math rendering
- Test math calculations for precision
- Target: University-level mathematics LMS