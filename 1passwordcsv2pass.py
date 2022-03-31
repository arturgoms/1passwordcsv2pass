import csv
from subprocess import Popen, PIPE


def pass_import_entry(path, data):
    proc = Popen(['pass', 'insert', '--multiline', path], stdin=PIPE,
                 stdout=PIPE)
    proc.communicate(data.encode('utf8'))
    proc.wait()


def escape(str_to_escape):
    return str_to_escape.replace(" ", "-") \
        .replace("&", "and") \
        .replace("[", "") \
        .replace("]", "")


def prepare_for_insertion(row):
    path = row[0] + '/' + row[7] + '/' + row[2]
    username = row[2]
    password = row[3]
    url = row[1]
    tag = row[7]
    notes = row[8]
    otp = row[4]

    data = '{}\n'.format(password)

    if username:
        data += 'user: {}\n'.format(username)

    if url:
        data += 'url: {}\n'.format(url)

    if notes:
        data += 'notes: {}\n'.format(notes)

    if otp:
        data += 'otpauth: {}\n'.format(otp)

    if tag:
        data += 'tag: {}\n'.format(tag)

    return path, data


def confirmation(prompt):

    prompt = '{0} {1} '.format(prompt, '(Y/n)')

    while True:
        user_input = input(prompt)

        if len(user_input) > 0:
            first_char = user_input.lower()[0]
        else:
            first_char = 'y'

        if first_char == 'y':
            return True
        elif first_char == 'n':
            return False

        print('Please enter y or n')


def main():
    with open('1password_example.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        entries = []
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if row[6] == 'false' and row[7] != 'ignore':
                    path, data = prepare_for_insertion(row)
                    if path and data:
                        entries.append((path, data))
                line_count += 1

        print('Entries to import:')

        for (path, data) in entries:
            print(path)

        if confirmation('Proceed?'):
            for (path, data) in entries:
                pass_import_entry(path, data)
                print(path, 'imported!')


if __name__ == '__main__':
    main()
