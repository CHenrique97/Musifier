var music = require('musicjson');
const fs = require('fs');
var parseString = require('xml2js').parseString;
var xmlserializer = require('xmlserializer');
const dataJSON=JSON.parse(fs.readFileSync('tempFile.json', 'utf8'))
program   = require('commander')

music.musicXML( dataJSON, function(err, xml) {
    console.log(xmlserializer.serializeToString(xml));
    converted = xml.end();
fs.writeFile('tempFile2.xml', converted, function(err, data) {
    if (err) {
      console.log(err);
    }
    else {
      console.log('updated!');
    }

  });
});
 