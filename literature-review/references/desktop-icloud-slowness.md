# Desktop iCloud Slowness Workaround

## Problem

`/Users/ding/Desktop/论语/` is backed by iCloud Drive. Every filesystem operation times out:
- `ls`, `find`, `stat` → 10-60s timeout
- `search_files` → timeout
- `read_file` → timeout
- `write_file` → succeeds but slow

This is a persistent environment condition, not a transient error.

## When This Matters

- User asks to retrieve analysis output from the current or recent session
- User asks to check what files exist on Desktop
- Need to reference previously saved stage files

## Workaround: session_search

When filesystem access to Desktop fails repeatedly, use `session_search` to retrieve content from the current session's conversation history:

```python
# Find the session:
session_search(query="<topic>", sort="newest", limit=5)

# Scroll to the relevant message:
session_search(session_id="...", around_message_id=<id>, window=5)
```

The conversation history contains the complete output of all stages, since the agent outputs them in chat before saving to disk.

## When NOT to use this

- Writing NEW files: still use write_file (it succeeds, just slow)
- Reading files from other sessions: session_search works, but read_file with generous timeout may also work
- Non-Desktop paths: unaffected by iCloud sync

## Root Cause

Likely iCloud Drive sync. The Desktop directory is synced to iCloud, and the sync daemon serializes filesystem operations. No fix available — this is a macOS/iCloud behavior.
