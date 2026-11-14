# Conduit - The MCP Server for Phabricator and Phorge
Conduit is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server that provides seamless integration with Phabricator and Phorge APIs, enabling advanced automation and interaction capabilities for developers and tools.

## Conduit
**Modern HTTP Client**: Built with `httpx` for HTTP/2 support and better performance

**MCP Integration**: Ready-to-use MCP tools for task management

**Type Safety**: Full type hints and runtime validation for better development experience

**Secure**: Token-based authentication with environment variable configuration

**Enhanced Features**:
- Advanced error handling with detailed error codes and suggestions
- Token optimization for efficient API responses
- Smart pagination and intelligent data limiting
- Runtime validation client for type safety
- Configurable client with caching and retry mechanisms

## Usage
### Via `uvx`
You need to install `uv` first. If it is not installed, run the following command:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
After installation, restart your shell or terminal to apply the environment variable changes.

Then run:
```bash
uvx --from git+https://github.com/mcpnow-io/conduit conduit-mcp
```

### From Source
To install from source for development or contribution:

```bash
# Clone the repository
git clone https://github.com/mcpnow-io/conduit.git
cd conduit

# Install in development mode with all dependencies
pip install -e .[dev]
```

This will install the package in editable mode with all development dependencies.

### Docker
The repository includes a [`Dockerfile`](Dockerfile) that packages the MCP server for **HTTP/SSE** mode.

Copy [`.env.example`](.env.example) to `.env`, edit it to update `PHABRICATOR_URL`, then:

```bash
docker compose up --build
```

The MCP server will be listening at port 8000 by default.

### Podman Quadlet
The [`quadlet/`](quadlet) directory holds [Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html) units that build the image from the `Dockerfile` and run the server as a systemd service with Podman:

- `conduit.build` builds the image `localhost/conduit:latest`, with the root of the checkout as the build context.
- `conduit.container` runs the container `conduit` and publishes port 8000 on `127.0.0.1`.

Link the directory into a Quadlet search path, for example for a rootless user:

```bash
mkdir -p ~/.config/containers/systemd
ln -s "$PWD/quadlet" ~/.config/containers/systemd/conduit
```

Set `PHABRICATOR_URL`, and optionally another host port, in a drop-in file `~/.config/containers/systemd/conduit.container.d/settings.conf`:

```ini
[Container]
Environment=PHABRICATOR_URL=https://your-phabricator-instance.com/api/
# Replace the published port:
PublishPort=
PublishPort=127.0.0.1:8080:8000
```

Then build the image and start the service:

```bash
systemctl --user daemon-reload
systemctl --user start conduit.service
```

The first start builds the image. To start the service at boot without a login session, enable lingering with `loginctl enable-linger`.

### As HTTP/SSE Server
Conduit can run as an HTTP/SSE server for multi-user scenarios. This mode allows multiple clients to connect simultaneously, each using their own authentication tokens.

```bash
conduit-mcp --host 127.0.0.1 --port 8000
```
When running as an HTTP server, authentication tokens are provided via HTTP headers instead of environment variables.

```
X-PHABRICATOR-TOKEN: your-32-character-token-here
```

## Configuration
Before running the server, you need to set up the following environment variables:

### Environment Variables
```bash
export PHABRICATOR_TOKEN=your-api-token-here
export PHABRICATOR_URL="https://your-phabricator-instance.com/api/"

export PHABRICATOR_PROXY="socks5://127.0.0.1:1080"  # Optional, if your network is behind a firewall
export PHABRICATOR_DISABLE_CERT_VERIFY=1  # Optional, if your network is under HTTPS filter (WARNING: Disabling certificate verification can expose you to security risks. Only set this if you trust your network environment.)
```
Do note that in HTTPS/SSE mode, `PHABRICATOR_TOKEN` is NOT needed.

### Getting Your API Token
1. Log into your Phabricator instance
2. Go to Settings > API Tokens
3. Generate a new token
4. Copy the 32-character token and use it as `PHABRICATOR_TOKEN`

## Contributing
There are many ways in which you can participate in this project, for example:
* Submit [bugs and feature requests](https://github.com/mcpnow-io/conduit/issues), and help us verify as they are checked in
* Review [source code changes](https://github.com/mcpnow-io/conduit/pulls)
* Review the [wiki](https://github.com/mcpnow-io/conduit/wiki) and make pull requests for anything from typos to additional and new content

If you are interested in fixing issues and contributing directly to the code base, please see the document [How to Contribute](https://github.com/mcpnow-io/conduit/wiki/How-to-Contribute)：
* [First-Time Setup](https://github.com/mcpnow-io/conduit/wiki/How-to-Contribute#first-time-setup)
* [Submitting a Pull Request](https://github.com/mcpnow-io/conduit/wiki/How-to-Contribute#submitting-a-pull-request)
* [Running Unittests](https://github.com/mcpnow-io/conduit/wiki/How-to-Contribute#running-unittests)

## License
Copyright (c) 2025 mpcnow.io. all rights reserved.

Licensed under the [MIT](LICENSE) license.
