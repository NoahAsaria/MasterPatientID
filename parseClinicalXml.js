var fs = require('fs');
var cli = require('cli');
var BlueButton = require('bluebutton');

var filePath = cli.args[0];

var xml = fs.readFileSync(filePath, 'utf-8');
var myRecord = BlueButton(xml);
var result = myRecord.data.json();
console.log(result); // goes to stdout, which is piped into our variable `result` above