import os
import re
import sys

def ansi_supported():
  '''
  Returns True if the output device supports ANSI escape codes,
  returns False otherwise.

  Heavily based on Django `supports_color` function
  https://github.com/django/django/blob/master/django/core/management/color.py
  '''

  device_requirements = (
    hasattr(sys.stdout, 'isatty'),
    sys.stdout.isatty(),
    sys.platform != 'Pocket PC',
    sys.platform != 'win32' or 'ANSICON' in os.environ
  )

  if all(device_requirements):
    return True
  return False

def _optional_formatting(func):
  '''
  This decorator is used for __format__ method to format text only if
  the output device supports ANSI escape codes.
  '''
  def dont_format(instance, spec):
    return ''
  
  if ansi_supported():
    return func
  return dont_format

class Formatter:
  def __esc(spec, end='m'):
    return f'\033[{spec}{end}'

  RESET = __esc('0')
  BOLD = __esc('1')
  FAINT = __esc('2')
  ITALIC = __esc('3')
  UNDERLINE = __esc('4')
  SLOW_BLINK = __esc('5')
  RAPID_BLINK = __esc('6')
  REVERSE_VIDEO = __esc('7')
  CONCEAL = __esc('8')
  CROSSED_OUT = __esc('9')
  PRIMARY_FONT = __esc('10')

  FRAKTUR = __esc('20')
  DOUBLE_UNDERLINE = __esc('21')
  BOLD_OFF_FAINT_OFF = __esc('22')
  ITALIC_OFF_FRAKTUR_OFF = __esc('23')
  UNDERLINE_OFF = __esc('24')
  BLINK_OFF = __esc('25')
  REVERSE_VIDEO_OFF = __esc('26')
  CONCEAL_OFF = __esc('27')
  CROSSED_OUT_OFF = __esc('28')
  DEFAULT_BACKGROUND_COLOR = __esc('49')
  FRAMED = __esc('51')
  ENCIRCLED = __esc('52')
  OVERLINED = __esc('53')
  FRAMED_OFF_ENCIRCLED_OFF = __esc('54')
  OVERLINED_OFF = __esc('55')

  FMTSPECS = {
    'e': RESET,
    'end': RESET,
    'reset': RESET,
    'b': BOLD,
    'bold': BOLD,
    'f': FAINT,
    'faint': FAINT,
    'i': ITALIC,
    'italic': ITALIC,
    'u': UNDERLINE,
    'underline': UNDERLINE,
    'sb': SLOW_BLINK,
    'blink': SLOW_BLINK,
    'rb': RAPID_BLINK,
    'r': REVERSE_VIDEO,
    'reverse': REVERSE_VIDEO,
    'co': CONCEAL,
    'conceal': CONCEAL,
    'c': CROSSED_OUT,
    'crossed': CROSSED_OUT,
    'pf': PRIMARY_FONT,

    'fr': FRAKTUR,
    'fraktur': FRAKTUR,
    'du': DOUBLE_UNDERLINE,
    '!b': BOLD_OFF_FAINT_OFF,
    '!bold': BOLD_OFF_FAINT_OFF,
    '!f': BOLD_OFF_FAINT_OFF,
    '!faint': BOLD_OFF_FAINT_OFF,
    '!i': ITALIC_OFF_FRAKTUR_OFF,
    '!italic': ITALIC_OFF_FRAKTUR_OFF,
    '!fr': ITALIC_OFF_FRAKTUR_OFF,
    '!u': UNDERLINE_OFF,
    '!underline': UNDERLINE_OFF,
    '!sb': BLINK_OFF,
    '!blink': BLINK_OFF,
    '!rb': BLINK_OFF,
    '!r': REVERSE_VIDEO_OFF, 
    '!reverse': REVERSE_VIDEO_OFF,
    '!co': CONCEAL_OFF,
    '!conceal': CONCEAL_OFF,
    '!c': CROSSED_OUT_OFF,
    '!crossed': CROSSED_OUT_OFF,

    'framed': FRAMED,
    'encircled': ENCIRCLED,
    'overlined': OVERLINED,
    '!framed': FRAMED_OFF_ENCIRCLED_OFF,
    '!encircled': FRAMED_OFF_ENCIRCLED_OFF
  }

  FG_COLORS_4BIT = {
    'k': 30,
    'bk': 30,
    'black': 30,
    'r': 31,
    'red': 31,
    'g': 32,
    'green': 32,
    'y': 33,
    'yellow': 33,
    'bl': 34,
    'blue': 34,
    'm': 35,
    'magenta': 35,
    'c': 36,
    'cyan': 36,
    'w': 37,
    'white': 37,

    'bbk': 90,
    'brightblack': 90,
    'br': 91,
    'brightred': 92,
    'bg': 93,
    'brightgreen': 93,
    'by': 94,
    'brightyellow': 95,
    'bbl': 96,
    'brightblue': 96,
    'bm': 97,
    'brightmagenta': 97,
    'bc': 98,
    'brightcyan': 98,
    'bw': 99,
    'brightwhite': 99
  }

  FG_REGEX = re.compile(r'fg\((.+)\)', re.IGNORECASE)
  FG8_REGEX = re.compile(r'fg8\((.+)\)', re.IGNORECASE)
  BG_REGEX = re.compile(r'bg\((.+)\)', re.IGNORECASE)
  BG8_REGEX = re.compile(r'bg8\((.+)\)', re.IGNORECASE)

  @staticmethod
  def fg8(color_code):
    return Formatter.__esc(f'38;5;{color_code}')

  @staticmethod
  def bg8(color_code):
    return Formatter.__esc(f'48;5;{color_code}')

  @staticmethod
  def fg24(r, g, b):
    return Formatter.__esc(f'38;2;{r};{g};{b}')

  @staticmethod
  def bg24(r, g, b):
    return Formatter.__esc(f'48;2;{r};{g};{b}')
  
  @staticmethod
  def _generic_color(color_spec, offset=0):
    if color_spec in Formatter.FG_COLORS_4BIT:
      return Formatter.__esc(str(Formatter.FG_COLORS_4BIT[color_spec] + offset))

    try:
      color = int(color_spec)
      return Formatter.__esc(color)
    except ValueError:
      if ',' in color_spec:
        r, g, b = [int(c) for c in color_spec.split(',')]
        if offset == 0:
          return Formatter.fg24(r, g, b)
        else:
          return Formatter.bg24(r, g, b)
      else:
        return ''

  @staticmethod
  def fg(color_spec):
    return Formatter._generic_color(color_spec)
  
  @staticmethod
  def bg(color_spec):
    return Formatter._generic_color(color_spec, offset=10)

  @_optional_formatting
  def __format__(self, spec_):
    spec = spec_.split(' ')

    fmt = ''

    if 'e' in spec:
      fmt = Formatter.RESET
      return fmt

    for s in spec:
      if s.lower() in Formatter.FMTSPECS:
        fmt += Formatter.FMTSPECS[s.lower()]
        continue

      fg_match = Formatter.FG_REGEX.match(s)
      if fg_match:
        color_spec = fg_match.group(1)
        fmt += Formatter.fg(color_spec)
        continue

      bg_match = Formatter.BG_REGEX.match(s)
      if bg_match:
        color_spec = bg_match.group(1)
        fmt += Formatter.bg(color_spec)
        continue

      fg8_match = Formatter.FG8_REGEX.match(s)
      if fg8_match:
        color_code = fg8_match.group(1)
        fmt += Formatter.fg8(color_code)
        continue

      bg8_match = Formatter.BG8_REGEX.match(s)
      if bg8_match:
        color_code = bg8_match.group(1)
        fmt += Formatter.bg8(color_code)
        continue

    return fmt
