import unittest
from get_price_selenium import O2GetPrice

class InequalityTest(unittest.TestCase):

  """ Testing for non-exsistant country Wakanda """
  def testNotEqual(self):
    with O2GetPrice as o2:
      self.failUnlessEqual(o2.get_standard_prices("Wakanda"), [None,None])

  """ Testing for empty string """
  def testNotEqual(self):
    with O2GetPrice() as o2:
      self.failUnlessEqual(o2.get_standard_prices(""), [None,None])

if __name__ == '__main__':
    unittest.main()
