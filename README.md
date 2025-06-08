[![Playwright](https://custom-icon-badges.demolab.com/badge/Playwright-2EAD33?logo=playwright&logoColor=fff)](#)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)


# Parser Test Assignment

This project is a parser utility designed to process and extract price information from various data sources.
It is built using Python and utilizes the Playwright library for web scraping. The parser is structured to handle multiple e-commerce platforms, including kaspi, halyk, and wildberries.

## Installation

1. Clone the repository.
```bash
git clone https://github.com/alisher-nil/parser_test_assignment
```
2. Install dependencies.
```bash
uv sync
```
3. Install playwright browsers.
```bash
playwright install
```
4. Copy the `.env.example` file to `.env` and set your environment variables.
```bash
cp .env.example .env
```
5. Run the parser with your input data.
```bash
# Example usage
uv run app/demo.py
```

## Features
- **Data Extraction**: Extracts price information from e-commerce platforms kaspi, halyk, wildberries.
- **Class Based Design**: Utilizes a class-based design for better organization, maintainability and extensibility.
