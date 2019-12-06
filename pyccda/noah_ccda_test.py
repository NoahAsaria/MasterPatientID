"""Unit tests for ccda.py."""

import ccda
import os
import unittest

TESTDATA_DIR = os.path.join(os.path.dirname(__file__), 'testdata')


class CcdaDocumentTestCase(unittest.TestCase):

  def _test_to_csv(self, fp):
    """Verify CCDA document can be converted to a CSV file."""
    ccda_doc = ccda.CcdaDocument(fp)
    ccda_csv = ccda_doc.to_csv()
    print(ccda_csv)
    self.assertTrue(ccda_csv)
    # TODO: Implement stronger test. Verify generated CSV against testdata.

  def _test_to_message(self, fp):
    """Verify CCDA document can be converted to a ProtoRPC message."""
    ccda_doc = ccda.CcdaDocument(fp)
    ccda_message = ccda_doc.to_message()
    #print(ccda_doc, ", ", ccda_message.allergies)
    #print(ccda_doc, ", ", ccda_message.demographics)
    #print(ccda_doc, ", ", ccda_message.immunizations)
    #print(ccda_doc, ", ", ccda_message.labs)
    #print(ccda_doc, ", ", ccda_message.medications)
    #print(ccda_doc, ", ", ccda_message.problems)
    #print(ccda_doc, ", ", ccda_message.procedures)
    #print(ccda_doc, ", ", ccda_message.vitals)
    #print("------------------------------")
    self.assertTrue(ccda_message)
    # TODO: Implement stronger test. Verify generated message against testdata.

  def test_sample_ccda_files(self):
    """Test all sample CCDA files in the testdata directory."""
    for basename in os.listdir(TESTDATA_DIR):
      fp = open(os.path.join(TESTDATA_DIR, basename))
      self._test_to_csv(fp)
      fp.seek(0)
      self._test_to_message(fp)
      fp.close()


if __name__ == '__main__':
  unittest.main()
