from heb_utils import HEX_GIBBERISH_TO_ANSI
from string import ascii_letters
from argparse import ArgumentParser
from os import remove


def replace_char_at_index(line, char, index):
    line_temp = list(line)
    line_temp[index] = char
    return "".join(line_temp)


def main(args):
    temp_filename = "temp.txt"
    file_arr = []
    line_words = []
    start_index = 0

    # Reading the input file as binary, and replacing the gibberish hex to Hebrew
    with open(args.InputFile, 'rb') as f:
        input_file_data = f.read().encode("hex")
        for key, val in HEX_GIBBERISH_TO_ANSI.iteritems():
            input_file_data = input_file_data.replace(key, val)
        with open(temp_filename, "wb") as temp_file:
            temp_file.write(input_file_data.decode("hex"))

    # Reading the replaced hex file as text and reversing so it will be readable hebrew
    # Also reversing back the english being flipped in the procedure
    with open(temp_filename, 'r') as f:
        for line in f.readlines():
            line_index = 0
            for letter in line:
                # If we found words in english, reverse them
                if letter not in ascii_letters and not letter.isdigit() and line_words and letter != " ":
                    for word_letter in line_words[::-1]:
                        line_temp = list(line)
                        line_temp[start_index] = word_letter
                        line = "".join(line_temp)
                        start_index += 1
                    start_index = 0
                    line_words = []

                # Checking if the letter is english, and adding to line_words array
                if letter in ascii_letters or (line_words and letter == " ") or letter.isdigit():
                    if start_index == 0:
                        start_index = line_index
                    line_words.append(letter)

                # Reversing '(' and ')'
                if letter == "(":
                    line = replace_char_at_index(line, ")", line_index)
                elif letter == ")":
                    line = replace_char_at_index(line, "(", line_index)

                line_index += 1
            file_arr.append(line[::-1].replace('\n', ''))
    remove(temp_filename)

    with open(args.OutputFile, 'wb') as f:
        f.writelines(file_arr)

if __name__ == '__main__':
    parser = ArgumentParser(description='Replacing converting gibberish file to hebrew.')
    parser.add_argument('-InputFile', default='default.txt', type=str,
                        help='Extracted gibberish file from PDF')
    parser.add_argument('-OutputFile', default='output.txt', type=str,
                        help='Output file)')
    main(parser.parse_args())