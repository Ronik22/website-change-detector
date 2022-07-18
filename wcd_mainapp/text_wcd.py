import os
import subprocess
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
        

    def run(self):
        logger.debug("changing dir to {}", self.folder)
        os.chdir(self.folder)

        if not os.path.exists(os.path.join("node_modules")):
            logger.debug("installing packages in {}", os.path.abspath("."))
            os.system("npm i fs node-fetch")

        if os.path.exists(f"./htmls/{self.id}_last.html"):
            node_cmd = "node index.mjs " + self.url + f" ./htmls/{self.id}_after.html " + f" ./htmls/{self.id}_last.html " + f" ./htmls/{self.id}_new.html"
            # to launch htmldiff
            p1 = subprocess.Popen(['node', 'index.mjs', self.url, f"htmls/{self.id}_after.html", f"htmls/{self.id}_last.html", f"htmls/{self.id}_new.html"], stdout=subprocess.PIPE)
            logger.debug(node_cmd)
            logger.debug("Comparing with prev file and saving new html")
            # wait for html to be saved
            p1.wait()
            os.remove(f"htmls/{self.id}_last.html")
            os.rename(f"htmls/{self.id}_new.html", f"htmls/{self.id}_last.html")
        
        else:
            node_cmd = "node index.mjs " + self.url + f" ./htmls/{self.id}_after.html " + f" ./htmls/{self.id}_last.html"
            # to launch htmldiff
            p1 = subprocess.Popen(['node', 'index.mjs', self.url, f"htmls/{self.id}_after.html", f"htmls/{self.id}_last.html"], stdout=subprocess.PIPE)
            logger.debug(node_cmd)
            logger.debug("saving new html")
            # wait for html to be saved
            p1.wait()
        

        # change dir back to root
        os.chdir("..")
        