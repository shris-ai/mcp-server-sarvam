# MCP Server for Sarvam

A Model Context Protocol (MCP) server that provides access to Sarvam's language processing capabilities. This server enables LLMs to perform tasks such as translation, language identification, and transliteration, specifically supporting translation between English and Indic languages, as well as transliteration across different scripts.

## Components

### Tools
The server implements the following tools:

- **translate_text**: Translates text between English and Indic languages.
- **identify_language**: Detects the language of the input text.
- **transliterate_text**: Converts text from one script to another while preserving pronunciation.

## Configuration
The server can be configured with the following arguments:

- `--api-key` (required): The API key for authentication with Sarvam services.

## Quickstart

### Install

#### Installing via Smithery
To install the MCP Server for Sarvam automatically via Smithery:

```sh
npx -y @smithery/cli install mcp-server-sarvam --client claude
```

### Development/Unpublished Servers Configuration

```json
"mcpServers": {
  "sarvam": {
    "command": "uv",
    "args": [
      "--directory",
      "{{PATH_TO_REPO}}",
      "run",
      "mcp-server-sarvam",
      "--api-key",
      "{{SARVAM_API_KEY}}"
    ]
  }
}
```

### Published Servers Configuration

```json
"mcpServers": {
  "sarvam": {
    "command": "uvx",
    "args": [
      "mcp-server-sarvam",
      "--api-key",
      "{{SARVAM_API_KEY}}"
    ]
  }
}
```

Replace `{{PATH_TO_REPO}}` and `{{SARVAM_API_KEY}}` with the appropriate values.

## Development

### Building and Publishing

To prepare the package for distribution:

```sh
uv sync  # Sync dependencies and update lockfile
uv build  # Build package distributions
```

This will create source and wheel distributions in the `dist/` directory.

### Publish to PyPI

```sh
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Username/password: `--username` / `UV_PUBLISH_USERNAME` and `--password` / `UV_PUBLISH_PASSWORD`

## Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging experience, we strongly recommend using the MCP Inspector.

You can launch the MCP Inspector via npm with this command:

```sh
npx @modelcontextprotocol/inspector uv --directory {{PATH_TO_REPO}} run mcp-server-sarvam
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

