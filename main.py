"""fixcom"""
import getopt
import sys
import re

OPTIONS = 'nt:c:e:'
LONG_OPTIONS = ['no-space', 'type=', 'case=', 'exclude=']
argument_list = sys.argv[1:]

no_space = False
comment_type = None
excluded_list = []
upper = True

try:

  arguments, values = getopt.getopt(argument_list, OPTIONS, LONG_OPTIONS)

  if len(arguments) == 0 or len(values) != 1:
    print('\nUsage: main.py (-n) -t <comment_type> (-c <upper/lower_case>) (-e <exclude_stringlist>) <filename>')
    sys.exit(2)

  for current_argument, current_value in arguments:
    if current_argument in ('-n', '--no-space'):
      no_space = True
    elif current_argument in ('-t', '--type'):
      comment_type = str(current_value)
    elif current_argument in ('-c', '--case'):
      if(str(current_value) == 'lower' or str(current_value) == 'l'):
        upper = False
      elif(str(current_value) != 'upper' and str(current_value) != 'u'):
        print('Wrong case type. Available types are: lower (or l), upper (or u). Default: upper')
    elif current_argument in ('-e', '--exclude'):
      excluded_list = current_value.split(',')
except getopt.error as err:
  print(err)
  print('\nUsage: main.py (-n) -t <comment_type> (-c <upper/lower_case>) (-e <exclude_stringlist>) <filename>')
  sys.exit(2)

comment_type_size = len(comment_type)
file_stringname = str(values[0])

file = open(file_stringname, "r")
file_text = file.read()
file.close()

matches = [m.start() for m in re.finditer(str(comment_type), file_text)]

text_list = list(file_text)

counter = 0

for match in matches:

  if(no_space and text_list[match + comment_type_size + counter] == ' '):
    # print("\nno_space: " + str(no_space) + " index: " + text_list[match], "char: " + text_list[match + comment_type_size])
    text_list.remove(match + comment_type_size + counter)
    counter -= 1
  elif((not no_space) and text_list[match + comment_type_size + counter] != ' '):
    text_list.insert(match + comment_type_size + counter, ' ')
    counter += 1

  if upper:
    text_list[match + comment_type_size + no_space + counter] = text_list[match + comment_type_size + no_space + counter].upper()
  else:
    text_list[match + comment_type_size + (not no_space) + counter] = text_list[match + comment_type_size + (not no_space) + counter].lower()

file_text = ''.join(text_list)

new_file = open("new_" + file_stringname, "w")
new_file.write(file_text)
new_file.close()
