# Octoscrape

A flexible framework for building and managing multiple asynchronous web scrapers with built-in concurrency control and browser management.

## 🎯 Overview

Octoscrape provides a robust foundation for web scraping projects that need to:
- Run multiple scrapers concurrently
- Share browser instances efficiently
- Manage asynchronous task pools
- Configure scrapers via YAML
- Control scrapers at runtime via CLI

## ✨ Key Features

- **Multi-Runner Architecture** - Launch and manage multiple asynchronous scrapers simultaneously
- **Async Pool Implementation** - Built-in pool for managing auxiliary coroutines with concurrency limits
- **Browser Manager** - Singleton pattern for sharing browser instances (Playwright & Camoufox support)
- **Configuration System** - YAML-based configuration with type-safe accessors
- **Simple CLI** - Interactive shell for runtime scraper management
- **Extensible Mixins** - Reusable components for common scraping tasks
- **Factory Pattern** - Clean scraper registration and instantiation

## 📁 Project Structure

```
octoscrape/
├── octoscrape/
│   ├── browser_manager/       # Browser lifecycle management
│   │   ├── camoufox.py        # Camoufox browser manager
│   │   ├── playwright.py      # Playwright browser manager
│   │   └── interface.py       # Browser manager interface
│   ├── concurrency/           # Async task management
│   │   └── async_pool.py      # Concurrent coroutine pool
│   ├── config/                # Configuration system
│   │   ├── common_config_acessor.py
│   │   └── scraper_config_acessor.py
│   ├── scraper/               # Core scraper framework
│   │   ├── factory.py         # Scraper factory
│   │   ├── interfaces.py      # Base scraper interface
│   │   ├── mixins.py          # Reusable scraper components
│   │   └── multirunner.py     # Multi-scraper manager
│   └── shell.py               # Interactive CLI
├── dummies/                   # Example scrapers
├── tests/                     # Test suite
├── config.yaml                # Configuration file
└── main.py                    # Entry point
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd octoscrape

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e .
```

### Basic Usage

1. **Define your scraper**:

```python
from octoscrape.scraper import IAsyncScraper

class MyScraper(IAsyncScraper):
    async def async_start(self):
        self._is_stopped = False
        # Your scraping logic here
        
    async def async_stop(self):
        self._is_stopped = True
```

2. **Configure in `config.yaml`**:

```yaml
scrapers:
  MyScraperConfig:
    human_name: My Website Scraper
    name: my_scraper
    url: https://example.com
    scraper: MyScraper
    pool_size: 10
```

3. **Run the shell**:

```python
from octoscrape.shell import Shell
from my_module import MyScraper

if __name__ == "__main__":
    Shell([MyScraper]).cmdloop()
```

4. **Control via CLI**:

```bash
> start                    # Start all scrapers
> start MyScraperConfig    # Start specific scraper
> stop                     # Stop all scrapers
> exit                     # Exit shell
```

## ⚙️ Configuration

### Common Settings

Global settings affecting all scrapers:

| Key             | Type | Description                          | Default |
|-----------------|------|--------------------------------------|---------|
| `path_to_csv`   | str  | Output directory for CSV results     | `.`     |
| `max_width`     | int  | Browser window width                 | 1920    |
| `max_height`    | int  | Browser window height                | 1080    |
| `pool_size`     | int  | Number of concurrent processes       | 1       |
| `headless`      | bool | Run browser in headless mode         | false   |

### Scraper Settings

Per-scraper configuration:

| Field         | Type   | Required | Description                              |
|---------------|--------|----------|------------------------------------------|
| `human_name`  | string | optional | Display name for logs and UI             |
| `name`        | string | yes      | Internal identifier & filename prefix    |
| `url`         | string | yes      | Starting URL for the scraper             |
| `scraper`     | string | yes      | Factory key for scraper implementation   |
| `pool_size`   | int    | optional | Concurrent tasks within this scraper     |
| `proxy`       | object | optional | Proxy configuration (server/user/pass)   |

### Example Configuration

```yaml
common:
  path_to_csv: ./results
  max_width: 1920
  max_height: 1080
  pool_size: 2
  headless: true

scrapers:
  ProductScraper:
    human_name: E-commerce Products
    name: products
    url: https://shop.example.com
    scraper: ProductScraper
    pool_size: 20
    proxy:
      server: "http://proxy:8080"
      username: "user"
      password: "pass"
```

## 🏗️ Architecture

### Core Components

1. **Browser Manager** - Singleton lifecycle management for browser instances
   - Supports Playwright and Camoufox
   - Ensures single browser per manager
   - Context manager pattern for safe cleanup

2. **Async Pool** - Concurrency-limited coroutine execution
   - Configurable parallelism
   - Queue-based task distribution
   - Graceful shutdown and cancellation

3. **Multi-Runner** - Coordinates multiple scrapers
   - Separate event loop in dedicated thread
   - Factory-based scraper instantiation
   - Runtime start/stop control

4. **Configuration System** - Type-safe YAML configuration
   - Property-based accessors
   - Validation and defaults
   - Separate common and per-scraper settings

### Design Patterns

- **Singleton Pattern** - Browser managers
- **Factory Pattern** - Scraper instantiation
- **Template Method** - Base scraper interface
- **Mixin Pattern** - Reusable scraper components

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=octoscrape --cov-report=html

# Run specific test module
pytest tests/concurrency/async_pool_test.py
```

Test structure:
- `tests/browser_manager/` - Browser lifecycle tests
- `tests/concurrency/` - Async pool tests
- `tests/config/` - Configuration accessor tests
- `tests/scraper/` - Scraper framework tests

## 📚 Advanced Usage

### Using the Async Pool

```python
from octoscrape.concurrency import AsyncPool

async def process_item(item):
    # Process item
    pass

async with AsyncPool(concurrency=10) as pool:
    for item in items:
        await pool.submit(process_item(item))
    # Automatically waits for all tasks to complete
```

### Custom Browser Context

```python
from octoscrape.scraper import IAsyncScraper, MixinContextCreator

class MyScraper(IAsyncScraper, MixinContextCreator):
    async def async_start(self):
        context = await self._new_context(browser)
        page = await context.new_page()
        # Use the page
```

### Accessing Configuration

```python
from octoscrape.config import common_config, scrappers_configs

# Access common settings
output_dir = common_config.path_to_csv_dir
is_headless = common_config.headless

# Access scraper-specific settings
for key, config in scrappers_configs.items():
    print(f"Scraper: {config.human_name}")
    print(f"URL: {config.url}")
    if config.is_proxy_available:
        print(f"Proxy: {config.proxy['server']}")
```

## 🔧 CLI Commands

The interactive shell supports the following commands:

- `start` - Start all configured scrapers
- `start <scraper1> <scraper2>` - Start specific scrapers
- `stop` - Stop all running scrapers
- `stop <scraper1> <scraper2>` - Stop specific scrapers
- `exit` - Shut down all scrapers and exit
- `help` - Show available commands

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure tests pass (`pytest`)
5. Format code (`black octoscrape/`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Create a Pull Request

## 📝 Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all public methods
- Write tests for new functionality
- Keep scrapers independent and reusable
- Use type hints where appropriate
- Document configuration options
