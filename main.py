"""fixcom"""
import getopt
import sys
import re

# options
OPTIONS = 'hnt:c:e:'
LONG_OPTIONS = ['help', 'no-space', 'type=', 'case=', 'exclude=']

# get argv
argument_list = sys.argv[1:]

# no space after comment_type
no_space = False

# comment type
comment_type = None

# list of excluded words
excluded_list = []

# upper / Lower case
upper = True

# parsing arguments
try:
  arguments, values = getopt.getopt(argument_list, OPTIONS, LONG_OPTIONS)

  # empty command or filename not specified and arg is not 'help'
  if len(arguments) == 0 or (len(values) != 1 and (not any('-h' in arg for arg in arguments) and not any('--help' in arg for arg in arguments))):
    print('\nEmpty command or missing filename')
    print('\nUsage: main.py (-n) -t <comment_type> (-c <upper/lower_case>) (-e <exclude_stringlist>) <filename>')
    print('\nUse -h or --help flag to get more info')
    sys.exit(2)

  for current_argument, current_value in arguments:
    # case: help
    if current_argument in ('-h', '--help'):
      print('\nUsage: main.py (-n) -t <comment_type> (-c <upper/lower_case>) (-e <exclude_stringlist>) <filename>')

      print('\nMandatory arguments:')
      print('  -t | --type : comment_type. For example: \'#\' or \'//\'')
      print('  filename : filename at the end of the command. For example: \'myfile.py\'')
      print('\nExample with only mandaory arguments: python3 main.py -t \'#\' myfile.py')

      print('\nOptional arguments:')
      print('  -h | --help : guideline')
      print('  -n | --no-space : format without space after command_type')
      print('  -c | --case : uppercase (or u) / lowercase (or l) first char of the word after command_type. Default upper')
      print('  -e | --exclude : stringlist of words to exclude from `case` format. For example: \'NULL,OK\'')
      print('\nExample: python3 main.py -t \'#\' -c l -e \'NULL,OK\' myfile.py')
      sys.exit(0)
    # case: no-space
    elif current_argument in ('-n', '--no-space'):
      no_space = True
    # case: type
    elif current_argument in ('-t', '--type'):
      comment_type = str(current_value)
    elif current_argument in ('-c', '--case'):
      # case: lowercase, default uppercase
      if(str(current_value) == 'lower' or str(current_value) == 'l'):
        upper = False
      # case: wrong case value
      elif(str(current_value) != 'upper' and str(current_value) != 'u'):
        print(
            'Wrong case type. Available types are: lower (or l), upper (or u). Default: upper')
    # case: exclude
    elif current_argument in ('-e', '--exclude'):
      # get list of excluded words
      excluded_list = current_value.split(',')
# wrong command or values
except getopt.error as err:
  print(err)
  print('\nUsage: main.py (-n) -t <comment_type> (-c <upper/lower_case>) (-e <exclude_stringlist>) <filename>')
  sys.exit(2)

# Check mandatory arguments
if comment_type == None:
  print('\nMissing mandatory comment_type')
  print('\nUsage: main.py (-n) -t <comment_type> (-c <upper/lower_case>) (-e <exclude_stringlist>) <filename>')
  sys.exit(2)

comment_type_size = len(comment_type)
filename = str(values[0])

# read the input file
file = open(filename, 'r')
file_text = file.read()
file.close()

# find the comments that match
matches = [m.start() for m in re.finditer(comment_type, file_text)]

# convert read text into list to edit char by index
text_list = list(file_text)

# counter of spaces added / removed
counter = 0

for match in matches:
  if(no_space):
    # if there is a space after command_type, remove it
    if(text_list[match + comment_type_size + counter] == ' '):
      del text_list[match + comment_type_size + counter]
      counter -= 1
      # there were a space, indexes are the same but we need to edit the next char
      move = 1
    else:
      # everything ok, no need to add space counter
      move = 0
  elif(not no_space):
    # if there isn't a space after command_type add it
    if(text_list[match + comment_type_size + counter] != ' '):
      text_list.insert(match + comment_type_size + counter, ' ')
      counter += 1
      # everything ok, no need to add space counter
      move = 0
    else:
      # there were a space, indexes are the same but we need to edit the next char
      move = 1

  # case: uppercase
  if upper:
    text_list[match + comment_type_size + counter + move] = text_list[match + comment_type_size + counter + move].upper()
  # case: lowercase
  else:
    text_list[match + comment_type_size + counter + move] = text_list[match + comment_type_size + counter + move].lower()

# join list intto text
file_text = ''.join(text_list)

# write the result into a new file
new_file = open('new_' + filename, 'w')
new_file.write(file_text)
new_file.close()
