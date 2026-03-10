---
mode: "agent"
model: GPT-4.1 (copilot)
tools: ["codebase"]
description: Generate unit tests for the selected function.
---

Generate unit tests for the following:

${selected_function_code}

Use the `unittest` framework and ensure that the tests cover various edge cases and typical scenarios for the function.

- If dependency exists, mock them appropriately.
- Name the test file as ${fileBasenameNoExtension}\_test.py and place it in the same directory as the original file.
- Name the test with a meaningful name that reflects the function being tested.
- If '**test**' directory exists in ${fileDirname}, place the test file there.

Return only the valid code.
