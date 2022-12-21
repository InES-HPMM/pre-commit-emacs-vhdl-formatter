# Emacs VHDL Formatter

Pre-commit hook to format VHDL files with emacs vhdl-mode.

## Format your vhdl files with pre-commit

Add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/pre-commit/mirrors-prettier
  rev: "" # Use the sha / tag you want to point at
  hooks:
    - id: emacs-vhdl-formatter
```
