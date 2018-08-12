import requests
from xml.etree import ElementTree

class CrowdInHelper :

    def __init__(self, project_name, project_key):
        self.project_name = project_name
        self.project_key = project_key

    def sendRequestForExportTranslationsToZip(self) :
        url = "https://api.crowdin.com/api/project/%s/export" % self.project_name
        querystring = {"key": self.project_key}
        response = requests.request("GET", url, params=querystring)
        tree = ElementTree.fromstring(response.content)
        status = tree.attrib['status']
        print("EXPORT STATUS: " + status)

        return status


    def downloadZipWithTranslations(self) :
        url = "https://api.crowdin.com/api/project/%s/download/all.zip" % self.project_name
        querystring = {"key": self.project_key}
        response = requests.request("GET", url, params=querystring)

        return response

