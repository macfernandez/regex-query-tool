# Regex Query Tool

<img alt="Code coverage" src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/macfernandez/4c379c3359827d18faef6e848a501031/raw/regex-query-tool-coverage.json&?style=plastic" />

This is my Regex Query Tool. It was developed to test regex patterns in python.
For using it, follow the instructions:

1. Clone this repo:

    ```{bash}
    git clone https://github.com/macfernandez/regex-query-tool
    ```

2. Create an environment (optional, but highly recommended).

3. Run:

    ```{bash}
    python -m src <pattern> <input> [-f] [-s] [-o <output-file>]
    ```

    - `pattern`: the regex pattern you want to test
    - `input`: either the string for testing the patter, or a file path with those string
    - `--file`, `-f`: if `input` is a file path, you must use this flag, otherwise the pattern will be tested against the file path as string
    - `--silent`, `-s`: for avoiding verbose behavior
    - `--output-file`, `-o`: to save the output in a file, you must use the flag and write the output file path following it
