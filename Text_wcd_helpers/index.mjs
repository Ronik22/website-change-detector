// node index.mjs "https://ronikb.ml/" "2_after.html" "2_last.html" "2_new.html"

import fetch from "node-fetch";
import fs from "fs";
import hdiff from "./htmldiff.js";

const CURRENT_URL = process.argv[2];
const OLD_FILE = process.argv[4];
const NEW_FILE = (process.argv[5] === undefined) ? OLD_FILE : process.argv[5];
const NAME_OF_FILE_WITH_CHANGES = process.argv[3];


const write_to_file = (data, outname) => {
	fs.writeFile(outname, data, (err) => {
		if (err) throw err;
	});
};

Promise.all([
	fetch(CURRENT_URL).then((resp) => resp.text()),
]).then((allResponses) => {

	const response2 = allResponses[0];
	write_to_file(response2, NEW_FILE);
	if(NEW_FILE != OLD_FILE) {
		const response1 = fs.readFileSync(OLD_FILE).toString();
		const output = hdiff(response1, response2);
		write_to_file(output, NAME_OF_FILE_WITH_CHANGES);
	}
	
});
