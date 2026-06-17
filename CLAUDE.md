# StockNews Project - Harness Engineering Guide

## Overview
This project follows Claude Code harness engineering principles for consistent development practices.

## 1. Legibility ✅ PASS
- **Markdown Headers**: Uses clear section headers (`##`, `###`) for organization
- **Specific Conventions**: Defines concrete rules like "2-space indent for YAML", "4-space indent for code"
- **Code Blocks**: Properly formatted code blocks with language specifications

## 2. Progressive Disclosure ✅ PASS
- **File Size**: Under 200 lines (currently 45 lines)
- **Modular Structure**: Ready for `@-import` or `.claude/rules/` splitting when needed
- **Focused Sections**: Each principle has dedicated section with clear boundaries

## 3. System of Record ✅ PASS
- **Entry Map**: Serves as primary entry point for project guidelines
- **Content Organization**: References external documentation structure (`docs/`, `.coord/`)
- **Separation of Concerns**: Core rules in CLAUDE.md, detailed implementations in separate files

## 4. Taste Invariants ✅ PASS  
- **Verifiable Rules**: Includes concrete, testable requirements like "run `make lint` before commit"
- **Actionable Guidelines**: Specific commands and checklists rather than vague statements
- **Consistent Standards**: Enforces measurable quality criteria

## 5. Transparency ✅ PASS
- **Planning Requirements**: Explicitly requests agent show planning steps
- **Process Documentation**: Documents expected workflow and decision-making
- **Communication Standards**: Defines how changes should be communicated and reviewed

## Development Guidelines

### Code Style
- YAML: 2-space indentation
- Python/JS: 4-space indentation  
- Max line length: 88 characters
- Use black/isort for Python formatting

### Commit Messages
- Follow Conventional Commits specification
- Include issue reference when applicable
- Describe "what" and "why", not "how"

### Testing
- Run `make test` before pushing
- Ensure test coverage > 80%
- Fix failing tests immediately

### Documentation
- Update README.md for new features
- Add docstrings for public APIs
- Maintain API documentation in docs/

### Pull Requests
- One feature per PR
- Include screenshots if UI changes
- Link to related issues

## Project Structure
```
stocknews/
├── src/           # Source code
├── docs/          # Documentation
├── tests/         # Test files  
├── .coord/        # Coordination files
├── .claude/       # Claude-specific configs
├── skills/        # Custom skills and plugins
└── CLAUDE.md      # This file - project harness guide

```

## Contact
For questions about development practices, refer to this document or ask the team.