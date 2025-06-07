# xitecli

[![XiteNodes Logo](https://billing.xitenodes.com/assets/img/logo.png)](https://xitenodes.com)  
**XiteNodes - NETPOOL TECHNOLOGIES PRIVATE LIMITED**

---

## Overview

`xitecli` is a lightweight, easy-to-use CLI tool to interact with local S3-compatible object storage (like MinIO) and optionally fallback to Cloudflare R2. It supports basic bucket and file operations using simple commands and configuration.

This tool is designed for developers and sysadmins who want a straightforward command-line interface to manage cloud or local object storage from their Linux environments.

---

## Features

- Connect to your local MinIO server or remote Cloudflare R2.
- Upload and download files with simple commands.
- Manage buckets (list, create, delete).
- Support for fallback to R2 storage if local storage is unavailable (optional).
- Minimal dependencies; written in Python 3 using `boto3` and `click`.
- Configurable via JSON config file in user home directory.

---

## Installation

### From `.deb` package (Recommended)

Download and install the `.deb` package:

```bash
sudo dpkg -i xitecli-deb.deb
````

This will install `xitecli` to `/usr/local/bin/xitecli`.

Make sure you have the required dependencies installed:

```bash
sudo apt-get install python3 python3-pip
pip3 install boto3 click requests
```

---

### From source

Clone the repo and run directly:

```bash
git clone https://github.com/xitenodes/xitecli.git
cd xitecli
python3 xitecli.py --help
```

---

## Configuration

The CLI reads configuration from:

```bash
~/.xitecli/config.json
```

Example config file:

```json
{
  "endpoint": "http://141.11.172.44:9000",
  "access_key": "YOUR_MINIO_ACCESS_KEY",
  "secret_key": "YOUR_MINIO_SECRET_KEY",
  "region": "us-east-1",
  "use_r2_fallback": false,
  "r2": {
    "endpoint": "https://<r2-endpoint>",
    "access_key": "R2_ACCESS_KEY",
    "secret_key": "R2_SECRET_KEY"
  }
}
```

> If you don’t want to use Cloudflare R2 fallback, set `"use_r2_fallback": false` or omit the `r2` section.

---

## Usage

### Common commands

```bash
# Show help
xitecli --help

# Upload a file to a bucket
xitecli upload --bucket mybucket --file /path/to/file.txt

# Download a file from a bucket
xitecli download --bucket mybucket --file file.txt --dest /path/to/save/

# List buckets
xitecli buckets list

# Create a new bucket
xitecli buckets create --bucket newbucket

# Delete a bucket
xitecli buckets delete --bucket oldbucket
```

---

## Development

* Python 3
* Dependencies: `boto3`, `click`, `requests`
* Use virtual environments recommended

---

## About XiteNodes

XiteNodes is a cutting-edge cloud and game hosting provider under **NETPOOL TECHNOLOGIES PRIVATE LIMITED**, delivering affordable, high-performance cloud solutions with AI-powered automation. We focus on game servers, local S3-compatible storage, and managed AI cloud platforms.

Visit our website: [https://xitenodes.com](https://xitenodes.com)

---

## License

MIT License © 2025 XiteNodes - NETPOOL TECHNOLOGIES PRIVATE LIMITED

---

## Contact

For support or inquiries, contact us at:
**[support@xitenodes.com](mailto:support@xitenodes.com)**

---

**XiteNodes - NETPOOL TECHNOLOGIES PRIVATE LIMITED**
Building India’s future cloud infrastructure.

```

---

Feel free to ask if you want me to generate a `.md` file for download or need help with other docs!
```
