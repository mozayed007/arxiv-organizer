# arxiv-organizer

`arxiv-organizer` is a standalone initial version subpackage for a larger project that aims to leverage Language Model Learning (LLMs) and classification techniques in the future.

This subpackage serves as a vanilla organizer for academic papers from the arXiv database. It uses Python's `re.match` for pattern matching and the arXiv API for fetching data.

## Requirements

This project requires the following packages:

- arxiv
- requests>=2.25.1
- selenium
- webdriver_manager

You can install these packages using pip:

```bash
 pip install -r requirements.txt
```

This will install all the dependencies listed in the `requirements.txt` file.

## Usage

To use `arxiv-organizer`, you can run the `__main__.py` script with the following command:

```bash
python -m src.arxiv_organizer
```

You can also use the `--update-categories` flag to update the categories, and the `--directory` flag to specify the directory to process:

```bash
python -m src.arxiv_organizer --update-categories --directory your_directory
```

## Installation

To install `arxiv-organizer`, you need to have Python installed on your machine. Then, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/mozayed007/arxiv-organizer.git
```

2. Navigate to the project directory:

```bash
cd arxiv-organizer
```

3. Install the package:

```bash
cd src
python setup.py install .
```

## Contributing

We welcome contributions to `arxiv-organizer`! If you have a feature request, bug report, or want to contribute code, please open an issue or pull request on our [GitHub repository](https://github.com/mozayed007/arxiv-organizer).
