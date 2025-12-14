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
| **scraper**    | string | yes      | Identifier used by the scraper factory to select the scraper implementation. |                              |
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
    # scraper: some_website_emplemantation_label
    # pool_size: 10
    # proxy:
    #   server: "http://proxy:8080"
    #   username: "user"
    #   password: "pass"
```
