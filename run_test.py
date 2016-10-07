import unittest
from get_price_selenium import O2GetPrice
import os

class InequalityTest(unittest.TestCase):

  """ Testing for non-exsistant country Wakanda """
  def testWrongCountry(self):
    with O2GetPrice() as o2:
      self.failUnlessEqual(o2.get_standard_prices("Wakanda"), [None,None])

  """ Testing for empty string """
  def testEmptyCountry(self):
    with O2GetPrice() as o2:
      self.failUnlessEqual(o2.get_standard_prices(""), [None,None])

  """ Testing for known quantity """
  def testKnownCountry(self):
    with O2GetPrice("file://{}/tests/testGermany.html".format(os.getcwd())) as o2:
      self.failUnlessEqual(o2.get_standard_prices("Germany"), [1.50,1.50])

  """ Testing for missing div """
  def testMissingDiv1(self):
    with O2GetPrice("file://{}/tests/testMissing.html".format(os.getcwd())) as o2:
      self.failUnlessEqual(o2.get_standard_prices("Test"), [None,1.50])

  """ Testing for missing div """
  def testMissingDiv2(self):
    with O2GetPrice("file://{}/tests/testMissing2.html".format(os.getcwd())) as o2:
      self.failUnlessEqual(o2.get_standard_prices("Test"), [1.50,None])

if __name__ == '__main__':
    unittest.main()
