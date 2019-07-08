#!/usr/bin/env python3

import argparse
import PyPDF2
import difflib
import os
import pytesseract
import pdf2image


parser = argparse.ArgumentParser(description='PDF Split and rename tool.')
parser.add_argument('-f', '--file', type=str, help='PDF file to split')

# TODO
# parser.add_argument('-d', '--date', help='Add date to resultant filename')


def _they_are_similar(text1, text2):
    sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
    ratio = sequence_matcher.ratio()
    return ratio > 0.7


def _is_a_similar_string_inside_a_line(string, line):
    for idx in range(len(line)):
        possible_similar_string = line[idx:idx + len(string)]
        if _they_are_similar(possible_similar_string, string):
            return True
    return False


def _get_all_texts_found(pdf_filename):
    image = pdf2image.convert_from_path(pdf_filename)[0]
    strings = pytesseract.image_to_string(image).split('\n')
    return strings


def _try_to_rename(individual_pdfs_per_page, possible_texts):
    for pdf_filename in individual_pdfs_per_page:
        texts_found = _get_all_texts_found(pdf_filename)
        similarity_found = False
        for line in texts_found:
            for possible_text in possible_texts:
                if _is_a_similar_string_inside_a_line(possible_text, line):
                    os.rename(pdf_filename, f'{possible_text}.pdf')
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
        output_pdf_filename = f'{i}.pdf'
        with open(output_pdf_filename, 'wb') as outputStream:
            output_pdf.write(outputStream)
        individual_pdfs_per_page.append(output_pdf_filename)
    return individual_pdfs_per_page


def _get_possible_texts():
    pdf_split_texts_filename = 'pdf_split_texts'
    if not os.path.exists(pdf_split_texts_filename):
        open(pdf_split_texts_filename, 'a').close()
        return []

    with open(pdf_split_texts_filename, 'r') as f:
        content = f.read()
        return content.split('\n')


def main():
    args = parser.parse_args()
    pdf_filename = args.file
    possible_texts = _get_possible_texts()
    if pdf_filename is not None:
        individual_pdfs_per_page = _split_pdf(pdf_filename)
        _try_to_rename(individual_pdfs_per_page, possible_texts)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
