import argparse
import PyPDF2
import difflib
import os


parser = argparse.ArgumentParser(description='PDF Split and rename tool.')
parser.add_argument('-f', '--file', type=str, help='PDF file to split')


def _they_are_similar(text1, text2):
    sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
    ratio = sequence_matcher.ratio()
    return ratio > 0.7


def _get_all_texts_found(pdf_filename):
    # TODO use an OCR to extract all text in the PDF
    return []


def _try_to_rename(individual_pdfs_per_page, possible_texts):
    for pdf_filename in individual_pdfs_per_page:
        texts_found = _get_all_texts_found(pdf_filename)
        similarity_found = False
        for text_found in texts_found:
            for possible_text in possible_texts:
                if _they_are_similar(text_found, possible_text):
                    # TODO rename pdf_filename to possible_text.pdf
                    similarity_found = True

                if similarity_found:
                    break
            if similarity_found:
                break


def _split_pdf(pdf_filename):
    individual_pdfs_per_page = []
    input_pdf = PyPDF2.PdfFileReader(open(pdf_filename, 'rb'))
    for i in range(input_pdf.numPages):
        output_pdf = PyPDF2.PdfFileWriter()
        output_pdf.addPage(input_pdf.getPage(i))
        output_pdf_filename = f'{i}' + pdf_filename
        with open(output_pdf_filename, 'wb') as outputStream:
            output_pdf.write(outputStream)
        individual_pdfs_per_page.append(output_pdf_filename)
    return individual_pdfs_per_page


def _get_possible_texts():
    pdf_split_texts_filename = 'pdf_split_texts'
    if not os.path.isfile(pdf_split_texts_filename):
        open(pdf_split_texts_filename, 'a').close()
        return []

    with open(pdf_split_texts_filename, 'r') as f:
        content = f.read()
        return content.split('\n')


def main():
    args = parser.parse_args()
    pdf_filename = args.file
    possible_texts = _get_possible_texts()
    individual_pdfs_per_page = _split_pdf(pdf_filename)
    _try_to_rename(individual_pdfs_per_page, possible_texts)


if __name__ == '__main__':
    main()
