## Prerequisites:

- Python 3.6 or higher
- pip (Python package manager)

## Steps:

### Clone the Autotelegram repository from GitHub:
``` git clone https://github.com/OSCA-Kampala-Chapter/autotelegram.git ```

### Navigate to the project directory:
```cd autotelegram ```

### Install the project's dependencies:
``` pip install -r requirements.txt ```

### Install the testing dependencies:
``` pip install -r requirements-dev.txt ```

## Create a test Telegram bot by following the Telegram documentation on how to create bots.

Create a .env file in the project's root directory with the following content, replacing <YOUR_BOT_TOKEN> with the token of the bot you created in the previous step:


`` TELEGRAM_BOT_TOKEN=<YOUR_BOT_TOKEN> ``

## Run the tests:
`` pytest ``

This will run all the tests in the project and output the results in the terminal.

Alternatively, you can run a specific test file by specifying the path to the file:

`` pytest tests/path/to/test_file.py ``

You can also run a specific test function within a test file by specifying the path to the file and the function name:

`` pytest tests/path/to/test_file.py::test_function_name ``

When running the tests, you can use the -s flag to print the output from print statements in the test code.

If you encounter any issues when running the tests, please refer to the Autotelegram documentation or open an issue on the project's GitHub repository.