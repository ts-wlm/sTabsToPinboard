JsOsaDAS1.001.00bplist00�Vscript_const safari = Application("Safari Technology Preview");

const urlObjects = [];

// safari.windows is not an array...
const windowKeys = Object.keys(safari.windows)
// iteration with for ... of loop doesn't really work (yet)
for (i=0; i<windowKeys.length; i++) {
  // safari.windows also has non-existing keys that throw an exception
  // when their tabs-property is accessed
  try {
    nrOfTabs = safari.windows[i]().tabs().length;
	// push titles and urls of open tabs to the urlObjects array the will
	// the the output of the script
	for (j=0; j<nrOfTabs; j++) {
	  urlObjects.push({
	    url: safari.windows[i]().tabs()[j].url(),
		title: safari.windows[i]().tabs()[j].name()
	  });
	}
  } catch (e) {
    // just ignore the exception
  }
}
console.log(JSON.stringify(urlObjects));                              *jscr  ��ޭ