import subprocess
import os
import urllib.request
from cv2 import threshold
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
from loguru import logger


class ImageWCD:
    """
    Class for Web change detection via Image comparison
    """
    def __init__(self, id, url, css, threshold):
        self.id = id
        self.url = url
        self.css = css
        self.threshold = threshold
        self.folder = "./Image_wcd_helpers"
        # use hosts file to remove ads for more reproducible websites
        # References: https://github.com/StevenBlack/hosts
        self.hostsfile = "http://sbc.io/hosts/alternates/fakenews-gambling-porn-social/hosts"
        self.indexjs = r"""
            const fs = require('fs');

            const puppeteer = require('puppeteer');

            hosts = {};
            //now we read the host file
            var hostFile = fs.readFileSync('hosts', 'utf8').split('\n');
            var hosts = {};
            for (var i = 0; i < hostFile.length; i++) {
                if (hostFile[i].charAt(0) == "#") {
                    continue
                }
                var frags = hostFile[i].split(' ');
                if (frags.length > 1 && frags[0] === '0.0.0.0') {
                    hosts[frags[1].trim()] = true;
                }
            }

            (async () => {

                const browser = await puppeteer.launch({ headless: true });
                const page = await browser.newPage();
                await page.setRequestInterception(true)

                page.on('request', request => {

                    var domain = null;
                    var frags = request.url().split('/');
                    if (frags.length > 2) {
                        domain = frags[2];
                    }

                    // just abort if found
                    if (hosts[domain] === true) {
                        request.abort();
                    } else {
                        request.continue();
                    }
                });
                // Adjustments particular to this page to ensure we hit desktop breakpoint.
                page.setViewport({ width: 1000, height: 1000, deviceScaleFactor: 1 });

                await page.goto(process.argv[2], { waitUntil: 'networkidle2' });
                // await page.waitFor(5000);

                if (process.argv[4] == 'full') {
                    await page.screenshot({
                        path: process.argv[3],
                        fullPage: true
                    })
                    await browser.close();
                    return
                }
                /**
                * References: https://gist.github.com/shospodarets/b4e8284e42fdaeceab9a67a9b0263743
                * Takes a screenshot of a DOM element on the page, with optional padding.
                *
                * @param {!{path:string, selector:string, padding:(number|undefined)}=} opts
                * @return {!Promise<!Buffer>}
                */
                async function screenshotDOMElement(opts = {}) {
                    const padding = 'padding' in opts ? opts.padding : 0;
                    const path = 'path' in opts ? opts.path : null;
                    const selector = opts.selector;

                    if (!selector)
                        throw Error('Please provide a selector.');

                    const rect = await page.evaluate(selector => {
                        const element = document.querySelector(selector);
                        if (!element)
                            return null;
                        const { x, y, width, height } = element.getBoundingClientRect();
                        return { left: x, top: y, width, height, id: element.id };
                    }, selector);

                    if (!rect)
                        throw Error(`Could not find element that matches selector: ${selector}.`);

                    return await page.screenshot({
                        path,
                        clip: {
                            x: rect.left - padding,
                            y: rect.top - padding,
                            width: rect.width + padding * 2,
                            height: rect.height + padding * 2
                        }
                    });
                }

                await screenshotDOMElement({
                    path: process.argv[3],
                    selector: process.argv[4],
                    padding: 16
                });

                browser.close();
            })();
            """

    def compare_images(self, img1, img2):
        """
        References: https://stackoverflow.com/a/71634759
        Compare 2 images and draws a bounding box around the difference of the latest image and returns score
        """
        before = cv2.imread(img1)
        after = cv2.imread(img2)

        # Convert images to grayscale
        before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
        after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

        # Compute SSIM between two images
        try:
            (score, diff) = ssim(before_gray, after_gray, full=True)
        except ValueError as e:
            if "{}".format(e) == "Input images must have the same dimensions.":
                # images are different
                cv2.imwrite(f"images/{self.id}_after.jpg", after, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
                return 0
            else:
                raise e

        # The diff image contains the actual image differences between the two images
        # and is represented as a floating point data type in the range [0,1]
        # so we must convert the array to 8-bit unsigned integers in the range
        # [0,255] before we can use it with OpenCV
        diff = (diff * 255).astype("uint8")

        # Threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = contours[0] if len(contours) == 2 else contours[1]

        mask = np.zeros(before.shape, dtype="uint8")
        filled_after = after.copy()

        for c in contours:
            area = cv2.contourArea(c)
            if area > 40:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(before, (x, y), (x + w, y + h), (36, 255, 12), 2)
                cv2.rectangle(after, (x, y), (x + w, y + h), (36, 255, 12), 2)
                cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
                cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

        cv2.imwrite(f"images/{self.id}_before" + img1 + img2, before)
        cv2.imwrite(f"images/{self.id}_after" + img1 + img2, after)
        cv2.imwrite(f"images/{self.id}_after.jpg", after, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

        return score


    def run(self):
        """
        Main function to run
        """
        firsttime = True
        ischanged = False
        logger.debug("changing dir to {}", self.folder)
        os.chdir(self.folder)
        with open("index.js", "w") as f:
            f.write(self.indexjs)
        if not os.path.exists(os.path.join("node_modules", "puppeteer")):
            logger.debug("installing puppeteer in {}", os.path.abspath("."))
            os.system("npm i puppeteer")
        if not os.path.exists(os.path.join("hosts")):
            logger.debug("downloading hosts file {}", self.hostsfile)
            urllib.request.urlretrieve(self.hostsfile, "hosts")
        node_cmd = "node index.js " + self.url + f" images/{self.id}_new.png '" + self.css + "'"
        
        # to launch pupeteer
        p1 = subprocess.Popen(['node', 'index.js', self.url, f'images/{self.id}_new.png', self.css], stdout=subprocess.PIPE)
        logger.debug(node_cmd)
        logger.debug("saving new image")
        # wait for image to be saved
        p1.wait()
        if os.path.exists(f"images/{self.id}_last.png"):
            firsttime = False
            logger.debug("comparing images")
            similarity = self.compare_images(f"images/{self.id}_last.png", f"images/{self.id}_new.png")
            logger.debug("similarity: {}", similarity)
            if similarity < self.threshold:
                ischanged = True
                logger.debug("similarity less than threshold({})", self.threshold)
                k = os.path.join(os.path.abspath("."), f"{self.id}_after.jpg")
                logger.debug(k)
        
            os.remove(f"images/{self.id}_last.png")
        
        os.rename(f"images/{self.id}_new.png", f"images/{self.id}_last.png")
        # change dir back to root
        os.chdir("..")

        context = {
            "firsttime": firsttime,
            "ischanged": ischanged,
            "website": self.url,
            "filepath": self.folder + f"/images/{self.id}_after.jpg",
            "similarity": None if firsttime else similarity,
            "threshold": self.threshold
        }
        return context



