import unittest
import ParserClass as parser

class MyTestCase(unittest.TestCase):
    def test_MaryGrantDemographics(self):
        file_path = 'TestFiles/MaryGrant-ClinicalSummary.xml'
        maryDemographics = parser.createNewDemographicsInstance(file_path)
        assert(maryDemographics.getFilePath() == 'TestFiles/MaryGrant-ClinicalSummary.xml')
        assert(maryDemographics.getDemographicDict() == {'given': ['Mary'], 'family': ['Grant'], 'address': ['No Address Indicated'], 'city': ['No City Indicated'], 'state': ['CA'], 'postalcode': ['99999'], 'birthtime': '19870321', 'gender': 'F', 'race': 'White'})

    def test_IsabellaJonesDemographics(self):
        file_path = 'TestFiles/IsabellaJones-ReferralSummary.xml'
        isabellaDemographics = parser.createNewDemographicsInstance(file_path)
        assert(isabellaDemographics.getFieldFromDict('given') == 'Isabella')
        assert(isabellaDemographics.getFilePath() == 'TestFiles/IsabellaJones-ReferralSummary.xml')
        assert(isabellaDemographics.getDemographicDict() == {'given': ['Isabella'], 'family': ['Jones'], 'address': ['No Address Indicated'], 'city': ['No City Indicated'], 'state': ['CA'], 'postalcode': ['99999'], 'birthtime': '19470501', 'gender': 'F', 'race': 'Caucasian or European American'})

    def test_badFileType(self):
        file_path = 'TestFiles/Critical Review 2.docx'
        demographics = parser.createNewDemographicsInstance(file_path)
        print("ROOT: ",demographics.getRoot())
        assert(demographics.getFilePath() == file_path)
        assert(demographics.getRoot() == 0)

    def main(self):
        MyTestCase.test_MaryGrantDemographics()
        MyTestCase.test_IsabellaJonesDemographics()
if __name__ == '__main__':
    unittest.main()
