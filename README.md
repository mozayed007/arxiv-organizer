# arxiv-organizer

Because of the ramping speed of publications, I thought of automating the organization of my research readings. This is just the initial version of a larger project that will leverage Large Language Models (LLMs) and NLP classification techniques in future versions instead of the categorization structure based on the [arxiv API python wrapper](https://github.com/lukasschwab/arxiv.py) to be more advanced using LLM-based categorization. I also plan to integrate it with the [Fully Local Chat Over Documents](https://github.com/jacoblee93/fully-local-pdf-chatbot) project in future versions.

`arxiv-organizer` is a Python package that helps you organize academic papers from the arXiv database. It uses pattern matching and the arXiv API for fetching data.

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

After installing the package, navigate to the directory where your papers are downloaded and simply run `arxiv-organizer` from the terminal. You can also update categories JSON scraped from arxiv category taxonomy using Chrome webdriver and specify the directory to process:

```bash
arxiv_organizer --update-categories --directory your_directory
```

## Installation

Installation is easy. You'll need Python installed on your machine, and Chrome webdriver (will try to improve that to be more generic in future versions). Just clone the repository and install the package:

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

I welcome any contributions, feature requests, or bug reports. Let's make academic research more organized together! Check out the project on GitHub: [arxiv-organizer](https://github.com/mozayed007/arxiv-organizer)

## License

[MIT License](https://github.com/mozayed007/arxiv-organizer/blob/main/LICENSE)
