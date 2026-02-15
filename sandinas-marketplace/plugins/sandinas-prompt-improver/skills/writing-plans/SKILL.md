---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
allowed-tools: AskUserQuestion
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. Testing (only if explicitly requested). Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Only include tests when user explicitly requests them in original task description.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the implementation code" - step
- "Run the verification" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use /executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`

**Step 1: Write implementation**

```python
def function(input):
    return expected
```

**Step 2: Verify manually**

Run: `python -c "from module import function; print(function(input))"`
Expected: Output shows expected value

**Step 3: Commit**

```bash
git add src/path/file.py
git commit -m "feat: add specific feature"
```
```

## When to Include Tests

**Default behavior:** Do NOT include tests in implementation plans.

**Only include tests when:**
- User explicitly requests "write tests", "add tests", "test coverage", or similar phrasing
- Requirements document specifies test requirements
- Critical business logic with explicit quality gates

**Alternative Task Structure (When tests are explicitly requested):**

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, frequent commits

## Execution Handoff

After saving the plan, first ask about workspace isolation, then offer execution choice:

**Step 1: Ask about workspace isolation**

Use AskUserQuestion:
```
question: Do you want to work in an isolated workspace (git worktree) or in the current branch?
header: Workspace
multiSelect: false
options:
  - label: Isolated worktree
    description: Create separate workspace using /using-git-worktrees - keeps current branch clean
  - label: Current branch
    description: Work directly in current branch - faster but mixes work in progress
```

**If Isolated worktree chosen:**
- Use /using-git-worktrees to create isolated workspace
- Then proceed with execution choice

**Step 2: Offer execution choice**

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- Stay in this session
- Check CLAUDE.md for specialized agents, use `general` if none defined for task type
- Use Task tool with appropriate agent for each task
- **ALWAYS atomize independent tasks for parallel subagent execution**

**If Parallel Session chosen:**
- Guide them to open new session in worktree (if using worktree) or current directory
- **REQUIRED SUB-SKILL:** New session uses /executing-plans
