# PDF Split And Rename Tool
The idea came from having a single PDF with all the payrolls of employees, one per page in a single file.

This tool split the PDF into several PDFs, one per page and try to search string similarities with the ones found inside the file pdf_split_texts. If one is found, the PDF is renamed to the string.

If pdf_split_texts file contains employee names, it's easy separate all payrolls.

# Instalation
```bash
sudo apt install tesseract-ocr # this is needed
git clone https://github.com/koyadovic/pdf-split-and-rename.git
cd pdf-split-and-rename/
pip install -r requirements.txt
```

# Use
* First edit or create the file pdf_split_texts with all the employee names, one per line.
* Second execute the tool using -f argument.
```bash
python pdf_split.py -f file.pdf
```
