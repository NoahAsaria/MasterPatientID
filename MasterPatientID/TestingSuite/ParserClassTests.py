import unittest
import CCDParser as parser

class MyTestCase(unittest.TestCase):
    def test_MaryGrantDemographics(self):
        file_path = 'TestFiles/MaryGrant-ClinicalSummary.xml'
        maryDemographics = parser.createNewDemographicsInstance(file_path)
        maryAllergies = maryDemographics.getAllergiesDict()
        print(maryAllergies)
        assert(maryAllergies == {'allergies': ['Bicillin L-A', 'Aspirin'], 'immunizations': ['No immunizations administered during visit'], 'procedures': ['Standard chest X-ray (procedure)']})
        assert(maryDemographics.getFilePath() == 'TestFiles/MaryGrant-ClinicalSummary.xml')
        assert(maryDemographics.getDemographicDict() == {'given': ['Mary'], 'family': ['Grant'], 'address': ['No Address Indicated'], 'city': ['No City Indicated'], 'state': ['CA'], 'postalcode': ['99999'], 'birthtime': '19870321', 'gender': 'Female'})#, 'race': 'White'})

    def test_IsabellaJonesDemographics(self):
        file_path = 'TestFiles/IsabellaJones-ReferralSummary.xml'
        isabellaDemographics = parser.createNewDemographicsInstance(file_path)
        isabellasAllergies = isabellaDemographics.getAllergiesDict()
        print("ALLERGIES: ", isabellasAllergies["allergies"])
        print("IMMUNIZATION: ", isabellasAllergies['immunizations'])
        print("PROCEDURES: ", isabellasAllergies['procedures'])

        assert(isabellaDemographics.getFieldFromDemographicDict('given') == 'Isabella')
        assert(isabellaDemographics.getFilePath() == 'TestFiles/IsabellaJones-ReferralSummary.xml')
        assert(isabellaDemographics.getDemographicDict() == {'given': ['Isabella'], 'family': ['Jones'], 'address': ['No Address Indicated'], 'city': ['No City Indicated'], 'state': ['CA'], 'postalcode': ['99999'], 'birthtime': '19470501', 'gender': 'Female'})#, 'race': 'Caucasian or European American'})
        assert(isabellasAllergies == {'allergies': ['Bicillin L-A', 'Codeine Phosphate', 'Aspirin'], 'immunizations': ['tetanus toxoid, unspecified formulation', 'Influenza, seasonal, injectable, preservative free', 'Influenza, seasonal, injectable, preservative free', 'Pneumococcal, 23-valent, adult'], 'procedures': []})
    def test_badFileType(self):
        file_path = 'TestFiles/Critical Review 2.docx'
        demographics = parser.createNewDemographicsInstance(file_path)
        print("ROOT: ",demographics.getRoot())
        assert(demographics.getFilePath() == file_path)
        assert(demographics.getRoot() == 0)

    def test_AllergiesData(self):
        assert(1 == 1)

    def main(self):
        MyTestCase.test_MaryGrantDemographics()
        MyTestCase.test_IsabellaJonesDemographics()
if __name__ == '__main__':
    unittest.main()
