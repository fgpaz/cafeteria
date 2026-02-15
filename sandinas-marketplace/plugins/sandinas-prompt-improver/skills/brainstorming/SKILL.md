---
name: brainstorming
description: Use when creating or developing, before writing code or implementation plans - refines rough ideas into fully-formed designs through collaborative questioning, alternative exploration, and incremental validation. Don't use during clear 'mechanical' processes
allowed-tools: AskUserQuestion
---

# Brainstorming Ideas Into Designs

## Overview

Turn ideas into fully formed designs through collaborative dialogue using AskUserQuestion for structured interaction.

## The Process

**Understanding the idea:**
- Check project state first (read CLAUDE.md for context, docs locations, architecture)
- Ask questions ONE AT A TIME using AskUserQuestion to refine the idea
- Prefer multiple choice with 2-4 options; open-ended is fine too
- Focus on: purpose, scope, constraints, success criteria
- If data model is relevant but unclear, ask where it's located
- If architecture is unclear (not in CLAUDE.md), ask about the pattern

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Use AskUserQuestion to present options
- Lead with your recommendation and explain why

**Presenting the design:**
- Break into sections of 200-300 words
- Use AskUserQuestion after each section to validate
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify

## 4 Core Principles for Effective Prompts

**Be Specific Upfront**
Reference specific files, mention constraints, point to example patterns.
Example: "The checkout flow is broken for users with expired cards. Check src/payments/ for the issue."

**Give Something to Verify Against**
Include test cases, expected outputs, or screenshots.
Example: "Test cases: 'user@example.com' -> true, 'invalid' -> false. Run the tests after."

**Explore Before Implementing**
For complex problems, use plan mode first - read relevant code, then create plan.
Example: "Read src/auth/ and understand sessions. Then create a plan for adding OAuth."

**Delegate, Don't Dictate**
Give context and direction, then trust the agent to figure out details.
Example: "The checkout flow is broken. Relevant code is in src/payments/. Can you investigate?"

The brainstorming process should refine user requests to follow these principles.

## AskUserQuestion Format

```
question: [Single clear question ending with ?]
header: [Short label max 12 chars]
multiSelect: false
options:
  - label: [Concise choice]
    description: [Trade-offs or implications]
  - label: [Alternative choice]
    description: [Trade-offs or implications]
```

## After the Design

**Documentation:**
- Write to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Use /writing-clearly-and-concisely skill if available
- Commit to git

**Implementation (if continuing):**
- Use AskUserQuestion: "Ready to set up for implementation?"
- Use /using-git-worktrees for isolated workspace
- Use /writing-plans for detailed implementation plan

## Key Principles

- **Use AskUserQuestion** - Always use the tool for questions
- **One question at a time** - Don't overwhelm
- **Multiple choice preferred** - Ground options in research findings
- **YAGNI ruthlessly** - Remove unnecessary features
- **Explore alternatives** - Always propose 2-3 approaches
- **Incremental validation** - Validate each section
- **Check CLAUDE.md first** - Project-specific context lives there
