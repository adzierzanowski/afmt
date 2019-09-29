#!/usr/bin/env python3

import unittest

from tests import formatter

if __name__ == '__main__':
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTests([
    loader.loadTestsFromModule(formatter),
  ])

  runner = unittest.TextTestRunner(verbosity=3)
  runner.run(suite)
