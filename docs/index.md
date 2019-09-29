# afmt

afmt is ANSI escape codes formatter for python.

To start using it, just import `Formatter` class from `afmt` and create an
instance. You can pass dictionary of custom styles with `styles` kwarg.

```python
from afmt import Formatter

f = Formatter(styles={
  'important': 'bold fg(red)'
})
```

You can then use `f` and format specs:

```python
print(f'{f: <format_specs...>}')
```

`format_specs` are separated with spaces. There are three types of specifiers:

* inline specifiers, e.g.: `bold`, `italic`
* inline "functions", e.g.: `fg(red)`, `goto(10,10)`
* custom styles, e.g.: `important` which are strings containing previously mentioned specs

Note that not all terminals support certain specifiers. E.g., blinking is not
widely supported. Fraktur is hardly supported ever. In publicly available
scripts it's advised to stick to standard ones like bold and 4-bit colors.

# Specifiers

| Specifiers          | Effect                |
|---------------------|-----------------------|
| `e`, `end`, `reset` | Resets all formatting |
| `b`, `bold` *       | Bold text             |
| `f`, `faint` *      | Faint color           |
| `i`, `italic` *     | Italic text           |
| `u`, `underline` *  | Underlined text       |
| `sb`, `blink` *     | Slow blink            |
| `rb`                | Rapid blink           |
| `r`, `reverse` *    | Reverse video         |
| `co`, `conceal` *   | Hidden text           |
| `c`, `crossed` *    | Crossed out text      |
| `pf`                | Primary font          |
| `fr`, `fraktur`     | Fraktur               |
| `du`                | Double underline      |
| `framed` *          | Framed text           |
| `encircled` *       | Encircled text        |
| `overlined`         | Overlined text        |

Specifiers annotated with `*` can be cancelled by prepending `!` to them, e.g.:

```python
print(f'{f:bold}bold on {f:!bold}bold off{f:e}')
```

# Functions

The available functions are:

### `fg`/`bg`

`fg` and `bg` are generic color functions. Depending on argument, they are
resolved into 4-bit, 8-bit or 24-bit color functions.

If the argument is a color name, the function is resolved into 4-bit color
according to the following table (the actual colors are implementation-dependent):

* `k`, `bk`, `black`
* `r`, `red`
* `g`, `green`
* `y`, `yellow`
* `bl`, `blue`
* `m`, `magenta`
* `c`, `cyan`
* `w`, `white`
* `bbk`, `brightblack`
* `br`, `brightred`
* `bg`, `brightgreen`
* `by`, `brightyellow`
* `bbl`, `brightblue`
* `bm`, `brightmagenta`
* `bc`, `brightcyan`
* `bw`, `brightwhite`

Example:

```python
print(f'{f:fg(green)}hello, world{f:e}')
```


If the argument is a single integer, the function is resolved into 8-bit color
function, e.g.:

```python
print(f'{f:fg(116)}hello, world{f:e}')
```


If the argument consists of three integers separated by commas, the function
is resolved into 24-bit color function, e.g.:

```python
print(f'{f:bg(128,255,0)}hello, world{f:e}')
```

### `goto`/`cur`

This function puts the cursor in a certain position.

```python
row = 10
col = 5
print(f'{f:goto({row},{col})}hello, world{f:e}')
```

# Custom styles

Custom styles can be specified in the initializer or can be added later.

```python
f = Formatter(styles={
  'important': 'fg(red) bold'
})

# alternatively
f = Formatter()
f.add_style('important', 'fg(red) bold')
```

They can be later referenced in the format specifier:

```python
print(f'{f:important}some important text{f:e}')
```
