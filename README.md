# pdfextractpages

## Description
This script allows users to extract a specified range of pages from a PDF file. It is interactive, prompting the user for the necessary information.

## Features
*   Interactive selection of PDF file and page range.
*   Comprehensive error handling:
    *   Handles cases where the specified PDF file is not found.
    *   Catches errors if the provided file is not a valid PDF or is corrupted.
    *   Validates page number inputs (checks for non-integer values, negative page numbers).
    *   Ensures page ranges are logical (start page not greater than end page) and within the actual page count of the PDF.
*   User-friendly prompts and error messages to guide the user.

## Requirements
*   Python 3
*   PyPDF2 library

## Installation
To use this script, you need to have Python 3 installed. You also need to install the PyPDF2 library. You can install it using pip:
```bash
pip install PyPDF2
```

## Usage
1.  Save the script as `pdfextractpages.py`.
2.  Open a terminal or command prompt.
3.  Navigate to the directory where you saved the script.
4.  Run the script using the command:
    ```bash
    python pdfextractpages.py
    ```
5.  The script will then prompt you to enter:
    *   The name of your PDF file (without the .pdf extension).
    *   The first page number for extraction (page counting starts at 0).
    *   The last page number for extraction (this page will be included).

## Error Handling
The script is designed to handle common issues gracefully:
*   **File Not Found:** If the PDF file you specify doesn't exist in the same directory as the script, you'll be prompted to enter the name again.
*   **Invalid PDF/Corrupted File:** If the file is not a valid PDF or is corrupted, the script will inform you and ask for a different file.
*   **Invalid Page Numbers:** If you enter non-numeric text for page numbers, negative numbers, or a start page that is greater than the end page, the script will show an error and may prompt again or exit.
*   **Page Range Out of Bounds:** If the start or end page numbers are outside the actual range of pages in the PDF, an error message will be displayed, and the script will exit.

## Output
If the extraction is successful, a new PDF file named `myfile_out.pdf` will be created in the same directory. This file will contain the extracted pages.

## License
This project is licensed under the terms of the LICENSE file.
