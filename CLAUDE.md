
---

### `CLAUDE.md`

```md
# CLAUDE.md

This document provides instructions for Claude Code while working on this repository.

---

# Project Goal

Build an AI-powered Valorant coaching system that combines:

- Computer Vision (YOLO)
- Multimodal LLMs (Gemini)
- Video processing
- Structured JSON outputs

The emphasis is on engineering a reliable AI pipeline rather than simply calling an LLM.

---

# General Workflow

Before writing code:

1. Explain your understanding of the task.
2. Explain your implementation plan.
3. Mention which files will change.
4. Wait if clarification is needed.

---

# Architecture

Do **not** significantly change the project's architecture without asking first.

Examples include:

- introducing new frameworks
- moving large modules
- changing data flow
- changing the JSON schema
- replacing libraries

Small refactors are encouraged.

---

# Coding Style

Prefer:

- readable code
- modular functions
- type hints
- descriptive variable names
- docstrings for public functions
- small files with clear responsibilities

Avoid:

- giant functions
- duplicated logic
- unnecessary abstractions
- premature optimization

---

# Existing Features

Do not break existing functionality.

Whenever modifying existing code:

- preserve behavior
- preserve APIs when possible
- explain breaking changes before making them

---

# Project Priorities

Highest priority:

1. Correctness
2. Reliability
3. Maintainability

Performance comes after correctness.

---

# AI Pipeline Principles

The project follows these principles:

- Never hallucinate gameplay details.
- Prefer uncertainty over incorrect certainty.
- Ground conclusions in visible evidence.
- Use structured outputs instead of parsing free text.

---

# YOLO Usage

YOLO is used for:

- ally detection
- enemy detection
- event detection
- frame selection

YOLO should support Gemini rather than replace it.

If detector output conflicts with the image, assume the image is correct.

---

# Gemini Usage

Gemini is responsible for:

- reasoning
- coaching
- connecting events across frames
- explaining decisions

Gemini should not invent facts.

---

# Refactoring Guidelines

Refactor aggressively when it improves:

- modularity
- readability
- reuse

Avoid unnecessary rewrites.

---

# Testing

When implementing new features:

- verify existing functionality still works
- prefer incremental changes
- keep commits focused on one feature

---

# Communication

When completing a task:

- summarize what changed
- explain why
- mention any tradeoffs
- point out future improvements if relevant

Never silently make major architectural decisions.