# afmt

This module provides an easy way to format text in CLI environment.
It is designed for use in **f-strings** but regular string formatting with
`format` method is also supported.

The module takes care of stripping ANSI escape sequences from piped output
and puts the sequences only if they're supported by the output device.

# Setup 

`$ pip install afmt`

# Usage and examples

```python
from afmt import Formatter

f = Formatter()
warning = 'bold bg(yellow) fg(black) italic'
error = 'bold bg(red) fg(white) underline'
print(f'{f:{warning}}Warning: you shouldn\'t do it{f:e}')
print(f'{f:{error}}Error: you can\'t do it{f:e}')


# Move cursor to 4th row and 6th column and print text in reverse video mode 
print(f'{f:reverse goto(4,6)}hello, world{f:e}')
```

[![asciicast](https://asciinema.org/a/271390.svg)](https://asciinema.org/a/271390)

# Development status

This module is in the early stage of development.
More features are coming hopefully soon.
