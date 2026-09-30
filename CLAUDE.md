# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e .

# Run MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

This is an MCP (Model Context Protocol) server that exposes document-processing tools to AI assistants via `FastMCP`.

**Entry point:** `main.py` imports tool functions from `tools/` and registers them with the MCP server using `mcp.tool()(fn)`.

**Tools directory:** Each file in `tools/` contains plain Python functions. Functions are imported into `main.py` and registered individually — they are not auto-discovered.

**Utilities vs. MCP tools:** `tools/document.py` contains helper functions (e.g. `binary_document_to_markdown`) that are not directly registered as MCP tools. `tools/math.py` contains `add`, which is registered as an MCP tool in `main.py`.

## Defining MCP Tools

Tools are plain Python functions registered via `mcp.tool()(fn)` in `main.py`. Follow this pattern:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="What this parameter controls"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of what the tool does.

    When to use:
    - Situation A
    - Situation B

    When NOT to use:
    - Situation C

    Examples:
    >>> my_tool("foo", 42)
    expected_output
    """
    # implementation
```

Then register in `main.py`:
```python
from tools.my_module import my_tool
mcp.tool()(my_tool)
```

Use `Field` from pydantic (not type annotations alone) for all parameter descriptions — these descriptions are what the AI assistant sees when deciding how to call the tool.
