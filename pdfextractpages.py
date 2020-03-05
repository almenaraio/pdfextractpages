# Super simple script to extract pages from a PDF file
# Pending: Handling input errors

import PyPDF2

filename = input("Enter your PDF file name: ")
pdf = (str(filename) + '.pdf')

startpage = int(input("Enter the FIRST page from where the extraction will start (NOTE: page count starts at 0): "))
endpage = int(input("Enter the LAST page where the extraction will end (NOTE: page count starts at 0): "))

pdfFile = open(pdf, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFile)
pdfWriter = PyPDF2.PdfFileWriter()

for pageNum in range(startpage, endpage):
     pageObj = pdfReader.getPage(pageNum)
     pdfWriter.addPage(pageObj)

pdfOutputFile = open('myfile_out.pdf', 'wb')
pdfWriter.write(pdfOutputFile)
pdfOutputFile.close()
pdfFile.close()

print('Extraction completed successfully. Output file: myfile_out.pdf')
