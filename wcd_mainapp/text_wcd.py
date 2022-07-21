import difflib
import os
import requests
from lxml import html, etree
from loguru import logger


class TextWCD:
    """
    Class for Web change detection via Text comparison
    """
    def __init__(self, id, url, css, threshold):
        self.id = id
        self.url = url
        self.css = css
        self.threshold = threshold
        self.folder = "./Text_wcd_helpers"
        self.extra_css = """
            <style>
                .twcd135654640ghghi, .twcd135654640ghghi * {
                    background-color:#00E600 !important; 
                    color:black !important;
                    border: 3px solid black !important;
                }
                .twcd135654640ghghd, .twcd135654640ghghd * {
                    background-color:#FF0000 !important; 
                    color:white !important;
                    border: 3px solid black !important;
                }
            </style>
        """


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


    def show_diff(self, seqm):
        """Unify operations between two compared strings seqm is a difflib.SequenceMatcher instance whose a & b are strings"""
        output= []
        for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
            if opcode == 'equal':
                output.append(''.join(map(str, seqm.a[a0:a1])))
            elif opcode == 'insert':
                output.append("<ins class='twcd135654640ghghi'>" + ''.join(map(str, seqm.b[b0:b1])) + "</ins>")
            elif opcode == 'delete':
                output.append("<del class='twcd135654640ghghd'>" + ''.join(map(str, seqm.a[a0:a1])) + "</del>")
            elif opcode == 'replace':
                output.append("<del class='twcd135654640ghghd'>" + ''.join(map(str, seqm.a[a0:a1])) + "</del>")
                output.append("<ins class='twcd135654640ghghi'>" + ''.join(map(str, seqm.b[b0:b1])) + "</ins>")
            else:
                raise RuntimeError( f"unexpected opcode unknown opcode {opcode}" )
        
        return ''.join(map(str, output))


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
            
            # check similarity ratio
            similarity = difflib.SequenceMatcher(a=file2,b=file1).ratio()
            logger.debug("similarity: {}", similarity)
            if similarity < self.threshold:
                ischanged = True
                logger.debug("Changes detected... Working on them")
                logger.debug("similarity less than threshold({})", self.threshold)
                sm= difflib.SequenceMatcher(None, file2, file1)
                htmldiffs = self.show_diff(sm)

                with open(f"{self.id}_after.html", 'w', encoding="utf8") as outfile:
                    outfile.write(htmldiffs + self.extra_css)

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
        