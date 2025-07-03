# Super simple script to extract pages from a PDF file
# Pending: Handling input errors

import PyPDF2

filename = input("Enter your PDF file name: ")
pdf = (str(filename) + '.pdf')

startpage = int(input("Enter the FIRST page from where the extraction will start (NOTE: page count starts at 0): "))
endpage = int(input("Enter the LAST page where the extraction will end (NOTE: page count starts at 0): "))

# Function to get PDF reader and number of pages
def get_pdf_reader(pdf_path):
    while True:
        try:
            # Use with statement for automatic file closing
            with open(pdf_path, 'rb') as pdfFile:
                reader = PyPDF2.PdfFileReader(pdfFile)
                # Access numPages to ensure file is readable by PyPDF2
                # PyPDF2.PdfFileReader can be lazy, so actually try to read something
                reader.getNumPages()
                # Re-open the file for the reader to be used outside this 'with' scope,
                # or pass the reader object around.
                # For simplicity here, we'll re-open or pass the path and let the main logic handle it.
                # Let's return the reader object after it's confirmed readable.
                # This means the file handle within this function will be closed.
                # The caller will need to re-open or we change strategy.

                # Strategy change: Open the file and return the reader, caller handles closing.
                # This is not ideal if we want 'get_pdf_reader' to be purely a validation step.
                # Let's stick to validating and then re-opening in the main flow,
                # or better, wrap the entire subsequent logic in the 'with' block.

                # Revised strategy: The main logic will use 'with open...'
                # This function will just validate the path and readability.
                # For now, let's assume the main loop will handle the 'with open'.
                # The current diff is aiming to put 'with open' in the main loop.
                return PyPDF2.PdfFileReader(open(pdf_path, 'rb')) # This open needs a corresponding close.
                                                                # This is becoming messy.

        except FileNotFoundError:
            print(f"Error: The file '{pdf_path}' was not found. Please try again.")
            # Prompt for a new filename if not found, then continue loop
            new_filename = input("Enter your PDF file name (without .pdf extension): ")
            pdf_path = new_filename + '.pdf' # Update pdf_path to retry
            continue # Restart the loop with the new path
        except PyPDF2.errors.PdfReadError:
            print(f"Error: Failed to read '{pdf_path}'. The file might be corrupted or not a valid PDF. Please try another file.")
            new_filename = input("Enter your PDF file name (without .pdf extension): ")
            pdf_path = new_filename + '.pdf' # Update pdf_path to retry
            continue # Restart the loop with the new path
        except Exception as e:
            print(f"An unexpected error occurred while trying to open or read '{pdf_path}': {e}")
            new_filename = input("Enter your PDF file name (without .pdf extension): ")
            pdf_path = new_filename + '.pdf' # Update pdf_path to retry
            continue # Restart the loop with the new path
        # If we reach here, it means an error occurred and we prompted for a new file.
        # The loop should continue. If successful, the function would have returned.

# This structure for get_pdf_reader is getting complicated with retries.
# Let's simplify and put the retry loop directly in the main script body.

# --- Input Phase ---
# Loop for PDF file input
while True:
    filename_input = input("Enter your PDF file name (without .pdf extension): ")
    pdf_path = filename_input + '.pdf'
    try:
        # Try to open and read the PDF to validate it immediately
        with open(pdf_path, 'rb') as test_file:
            PyPDF2.PdfFileReader(test_file).getNumPages() # Check if readable and get num_pages
        break # File is valid and readable, exit loop
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found. Please try again.")
    except PyPDF2.errors.PdfReadError:
        print(f"Error: Failed to read '{pdf_path}'. The file might be corrupted or not a valid PDF. Please try another file.")
    except Exception as e: # Catch any other unexpected error during file open/read
        print(f"An unexpected error occurred while trying to open or read '{pdf_path}': {e}")

# Loop for start page input
while True:
    try:
        startpage_str = input("Enter the FIRST page from where the extraction will start (NOTE: page count starts at 0): ")
        startpage = int(startpage_str)
        if startpage < 0:
            print("Error: Start page cannot be negative.")
            continue
        break
    except ValueError:
        print(f"Error: Invalid input. '{startpage_str}' is not a valid integer. Please enter a number.")

# Loop for end page input
while True:
    try:
        endpage_str = input("Enter the LAST page where the extraction will end (NOTE: page count starts at 0): ")
        endpage = int(endpage_str)
        if endpage < 0: # Basic check, more comprehensive check against num_pages will be done later
            print("Error: End page cannot be negative.")
            continue
        break
    except ValueError:
        print(f"Error: Invalid input. '{endpage_str}' is not a valid integer. Please enter a number.")

# --- Processing Phase ---
try:
    with open(pdf_path, 'rb') as pdfFile:
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        num_pages = pdfReader.getNumPages()

        # Validate page range (now that we have num_pages)
        if startpage > endpage:
            print(f"Error: Start page ({startpage}) cannot be greater than end page ({endpage}).")
            exit() # Or handle differently, e.g., re-prompt

        if startpage >= num_pages:
            print(f"Error: Start page ({startpage}) is out of range. This PDF has {num_pages} pages (0 to {num_pages - 1}).")
            exit()

        if endpage >= num_pages:
            print(f"Error: End page ({endpage}) is out of range. This PDF has {num_pages} pages (indexed 0 to {num_pages - 1}).")
            print("Exiting script.")
            exit()

        # This check is implicitly covered if startpage > endpage initially, or if startpage itself is >= num_pages.
        # if startpage > endpage : # Recheck if adjustment made endpage < startpage
        #      print(f"Error: Adjusted end page ({endpage}) is now less than start page ({startpage}). Nothing to extract.")
        #      exit()


        pdfWriter = PyPDF2.PdfFileWriter()

        # The loop for pageNum in range(startpage, endpage + 1) ensures 'endpage' is inclusive.
        for pageNum in range(startpage, endpage + 1):
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

        output_filename = 'myfile_out.pdf'
        with open(output_filename, 'wb') as pdfOutputFile:
            pdfWriter.write(pdfOutputFile)

        print(f"Extraction completed successfully. Output file: {output_filename}")

except PyPDF2.errors.PdfReadError:
    # This specific error might occur if the file was accessible during the input phase check,
    # but something went wrong when re-opening or re-reading it in the processing phase.
    # Or if the initial check wasn't thorough enough.
    print(f"Error: Failed to process '{pdf_path}'. The file might be corrupted or not a valid PDF.")
except Exception as e:
    print(f"An unexpected error occurred during PDF processing: {e}")
# No 'finally' needed to close pdfFile or pdfOutputFile as 'with' handles it.
