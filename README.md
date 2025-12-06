# Settings

## Configuration Format

This document describes the structure and purpose of the configuration file used by the scraping framework.
The configuration is divided into two main sections:

- common — Global application settings
- scrapers — Per-worker (per-scraper) settings

### Common Settings

Global settings that affect the entire application.

| Key             | Type   | Description                                                                           | Default                   |
| --------------- | ------ | ------------------------------------------------------------------------------------- | ------------------------- |
| **path_to_csv** | string | Path to the folder where all CSV results will be stored. Can be absolute or relative. | Current working directory |
| **max_width**   | int    | Maximum browser window width.                                                         | 1920                      |
| **max_height**  | int    | Maximum browser window height.                                                        | 1080                      |
| **pool_size**   | int    | Number of multiprocessing workers that can run simultaneously.                        | 1                         |
| **headless**    | bool   | optional | Run the browser in headless mode.                                          | false                     |

#### Example:
```yaml
common:
  path_to_csv: ./results
  max_width: 1920
  max_height: 1080
  pool_size: 2
  headless: true
```

## Scraper Settings

Each entry under process: defines an independent logical scraping worker.
Every worker has its own target URL, scraper implementation, and concurrency limits.

### Common Fields
| Field          | Type   | Required | Description                                                                  | Default                      |
| -------------- | ------ | -------- | ---------------------------------------------------------------------------- | ---------------------------- |
| **human_name** | string | optional | Human-readable name used for logs and UI messages.                           | ""                           |
| **name**       | string | yes      | Internal worker name. Also used as the prefix for output filenames.          |                              |
| **url**        | string | yes      | Base URL of the page that the worker will process.                           |                              |
| **label**      | string | optional | Identifier used by the scraper factory to select the scraper implementation. | `process.<thread_name>.name` |
<!-- | **headless**   | bool   | optional | Run the browser in headless mode.                                            | false                        | -->
| **pool_size**  | int    | optional | Number of concurrent asynchronous tasks allowed within this worker.          | 1                            |
| **proxy**      | object | optional | Per-worker proxy settings (server, username, password).                      | None                         |

#### Proxy structure:
```yaml
proxy:
  server: "http://example.com:8080"
  username: "user"
  password: "pass"
```

#### Example: Scraper settings
```yaml
scrapers:
  SomeWebsiteScraperExample:
    human_name: Some website
    name: some_website
    url: https://some_website.com
    # label: some_website_emplemantation_label
    # pool_size: 10
    # proxy:
    #   server: "http://proxy:8080"
    #   username: "user"
    #   password: "pass"
```

<!-- ## Multi-Scraper Process

The process can contain multiple scraper implementations. 
This is used when a single worker needs to run multiple scrapers in parallel, each with its own settings.

### Additional Field
| Field               | Type   | Required | Description                                                                 | Default |
| ------------------- | ------ | -------- | --------------------------------------------------------------------------- | ------- |
| **is_multiscraper** | bool   | yes      | Enables multi-scraper mode.                                                 |         |
| **name**            | string | yes      | Internal worker name.                                                       |         |
| **human_name**      | string | optional | Human-readable name used for logs and UI messages.                          | ""      |
| **label**           | string | yes      | Identifier used by the scraper factory to select the scraper implementation |         |
| **pool_size**       | int    | optional | Sets how many scrapers can be run.                                          | 1       |
| **scrapers**        | object | yes      | List of scraper configurations handled by this worker.                      |         |

#### Example: Multi Scraper Process
```yaml
process:
  MultiScraperExample:
    is_multiscraper: true
    label: multi_scraper_label
    pool_size: 2
    scrapers:
      SomeExample1:
        human_name: Some website
        name: some_website
        url: https://some_website.com/some_path/

      SomeExample2:
        human_name: Some website 2
        name: some_website_2
        url: https://pakcoat.org/other_path/
        label: some_website

      SomeExample3:
        human_name: Another website
        name: another_website_with_price_information
        url: https://another_website.com
        label: another_website
``` -->


<!-- # How run
### (Optional) Create environment
```bash
# create environment
python -m venv .venv

# activate environment on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# activate environment on Windows (cmd)
.\.venv\Scripts\activate.bat

# activate environment on Linux/macOS
source .venv/bin/activate
```

### Install requirements
```bash
# optionally: upgrade pip first
python -m pip install --upgrade pip

# then install
pip install -r requirements.txt
```

### Start script
```bash
python main.py
``` -->