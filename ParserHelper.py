import io
import os
import zipfile
import xlrd

class ParserHelper :

    mapOfLangs = {"English (United States)":"en-US",
                  "Chinese Simplified": "zh-CN",
                  "Chinese Traditional (Hong Kong)": "zh-TW",
                  "Czech":"cs",
                  "Danish": "da",
                  "Dutch (Netherlands)": "nl",
                  "French (France)": "fr",
                  "German (Germany)": "de",
                  "Hungarian": "hu",
                  "Italian (Italy)": "it",
                  "Polish": "pl",
                  "Portuguese (Brazil)":"pt-BR",
                  "Portuguese (Portugal)": "pt-PT",
                  "Romanian (Romania)": "ro",
                  "Russian (Russia)": "ru",
                  "Slovak": "sk",
                  "Spanish (Latin America)": "es-AR",
                  "Spanish (Spain)": "es-ES",
                  "Swedish (Sweden)": "sv-SE",
                  "Turkish": "tr",
                  "Ukrainian": "uk",
                  "Indonesian":"id",
                  "English (United Kingdom)":"en-GB",
                  "Malay (Malaysia)":"ms"}

    def __init__(self, response, parhToDir):
        self.response = response
        self.pathToDir = parhToDir

    def createStructureAndProperties(self):
        with zipfile.ZipFile(io.BytesIO(self.response.content)) as thezip:
            for zipinfo in thezip.infolist():
                with thezip.open(zipinfo) as thefile:
                    if (zipinfo.file_size == 0):
                        try:
                            os.makedirs(self.pathToDir + "%s" % zipinfo.filename)
                        except FileExistsError:
                            continue
                    else:
                        catalog = zipinfo.filename.split('/')[0].replace(' ', '_')
                        catalogWithTranslations = zipinfo.filename.split('/')[1].split('.')[0].replace(' ', '_')
                        try:
                            os.makedirs(self.pathToDir + "%s/%s" % (catalog, catalogWithTranslations))
                        except FileExistsError:
                            print("Directory exist")
                        self.parseExcelToProperties(thefile)


    def parseExcelToProperties(self, thefile):
        xlsxToByteCode = thefile.read()
        workbook = xlrd.open_workbook(file_contents=xlsxToByteCode)
        sheet = workbook.sheet_by_index(0)
        labels = sheet.row_values(0)
        columWithKey = sheet.col_values(0)[1:]
        for label in labels[1:]:
            print("Label: " + label)
            try:
                langLabel = self.mapOfLangs.get(label).lower()
            except AttributeError:
                continue
            pathToProperties = self.pathToDir + thefile.name.split('.')[0].replace(' ','_') + "/"

            newLangProperties = open(pathToProperties + 'messages_' + langLabel + '.properties', 'w+', encoding='utf-8')
            colum = sheet.col_values(labels.index(label))[1:]
            for wordIndex in range(len(columWithKey)):
                newLangProperties.write(columWithKey[wordIndex] + '=' + colum[wordIndex] + '\n')
            newLangProperties.close()

