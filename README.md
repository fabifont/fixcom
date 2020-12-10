# fixcom
Script to fix comments into a file.

## Usage
Just for the explanation:
- optional arguments are inside `()`
- the value of an argument is inside `<>`

`python3 main.py (-h) (-n) (-s) (-a) (-c <format_case>) (-e <excluded_words>) -t <comment_symbol> filename`

## Arguments explanation
### Mandatory arguments
- `-t`, `--type`: comment symbol (like `//` for C/C++, `#` for Python etc...) surrouned by `'`
  - Example: `--type '#'`
- `filename`: the file that needs comment formatting. **MUST BE THE LAST ARGUMENT**

### Optional arguments
Without value:
- `-h`, `--help`: prints the info message
- `-n`, `--no-space`: formats without space after the command symbol
  - Example: `# this is a comment` becomes `#this is a comment`
- `-s`, `--spaces`: removes extra spaces after comment symbol
  - Example: <pre>`#     this   is a  comment`</pre> becomes `# this is a comment`
- `-a`, `--all`: applies uppercase / lowercase to all words after comment symbol
  - Example: `# THis Is A COMMent` becomes `# this is a comment` or `# THIS IS A COMMENT` respecting excluded words
  
With value:
- `-c`, `--case`: `u`, `upper` or `l`, `lower`. Formatting type. Default: `u`
  - Example: `# this is a comment` becomes `# This is a comment` (without `--all`)
- `-e`, `--exclude`: string of words separated by `,` and surrounded by `'`
  - Example: `--exclude 'NULL,ERROR'`. `# VALUE is NULL` with `-c lower -all` becomes `# value is NULL`
  
## Example
`test.c`:
```C
#include <stdio.h>

// main     function
int main() {
    //p poINTS to NULL
    int *p = NULL;
    //RETURNS 0
    return 0;
}
```

Comment formatting:
`python3 main.py -s -a -t '//' -c lower -e 'NULL' test.c`

Result (`new_test.c`):
```C
#include <stdio.h>

// main function
int main() {
    // p points to NULL
    int *p = NULL;
    // returns 0
    return 0;
}
```
