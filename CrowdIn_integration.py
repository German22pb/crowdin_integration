from  CrowdInHelper import CrowdInHelper
from ParserHelper import ParserHelper

project_name = "project name"
project_key = "your project api key"
pathToDir = "Translations/"
crowdInHelper = CrowdInHelper(project_name, project_key)

# Extract translations
status = crowdInHelper.sendRequestForExportTranslationsToZip()
crowdInHelper.downloadZipWithTranslations()
zipResponse = crowdInHelper.downloadZipWithTranslations()
parserHelper = ParserHelper(zipResponse, pathToDir)
parserHelper.createStructureAndProperties()



