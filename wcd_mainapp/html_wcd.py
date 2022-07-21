import difflib
import os
import requests
from lxml import html, etree
from loguru import logger


class HtmlWCD:
    """
    Class for Web change detection via HTML comparison
    """

    def __init__(self, id, url, css, threshold):
        self.id = id
        self.url = url
        self.css = css
        self.threshold = threshold
        self.folder = "./HTML_wcd_helpers"

    def trim_with_xpath(self, r):
        if self.css and not self.css == "full":
            tree = html.fromstring(r.content)
            for elem in tree.xpath(self.css):
                file1 = etree.tostring(elem, pretty_print=True)
            with open(f"{self.id}_new.html", 'wb') as outfile:
                outfile.write(file1)
        else:
            with open(f"{self.id}_new.html", 'w', encoding="utf8") as outfile:
                outfile.write(r.text)

    def run(self):
        firsttime = True
        ischanged = False
        
        logger.debug("changing dir to {}", self.folder)
        os.chdir(self.folder)
        try:
            r = requests.get(self.url)
        except:
            logger.error("URL cannot be reached")
            return
        self.trim_with_xpath(r)
        logger.debug("Saving file")

        if os.path.exists(f"{self.id}_last.html"):
            firsttime = False
            
            file1 = open(f"{self.id}_new.html", 'r', encoding="utf8").readlines()
            file2 = open(f"{self.id}_last.html", 'r', encoding="utf8").readlines()
            # htmlDiffer = difflib.HtmlDiff()
            
            # check similarity ratio
            similarity = difflib.SequenceMatcher(a=file2,b=file1).ratio()
            logger.debug("similarity: {}", similarity)
            if similarity < self.threshold:
                ischanged = True
                logger.debug("similarity less than threshold({})", self.threshold)
                logger.debug("Changes detected... Working on them")
                htmlDiffer = difflib.HtmlDiff(wrapcolumn=70)
                htmldiffs = htmlDiffer.make_file(file2, file1)

                with open(f"{self.id}_after.html", 'w', encoding="utf8") as outfile:
                    outfile.write(htmldiffs)

            os.remove(f"{self.id}_last.html")
            logger.debug("Saving file")
        
        os.rename(f"{self.id}_new.html", f"{self.id}_last.html")
        # change dir back to root
        os.chdir("..")

        context = {
            "firsttime": firsttime,
            "ischanged": ischanged,
            "website": self.url,
            "filepath": self.folder + f"/{self.id}_after.html",
            "similarity": None if firsttime else similarity,
            "threshold": self.threshold
        }
        return context
        