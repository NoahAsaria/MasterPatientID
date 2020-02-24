/*
import firebase from 'firebase';
import 'firebase/storage';

var config = {
  apiKey: "AIzaSyB0UDvO8aCT71DWFYMVZih5xhVq6-u-Mqw",
  authDomain: "mpi-test-d9494.firebaseapp.com",
  databaseURL: "https://mpi-test-d9494.firebaseio.com",
  storageBucket: "mpi-test-d9494.appspot.com",
};
firebase.initializeApp(config);
*/
function storeFiles() {
	var fileAttach = document.getElementById("userFile");
	var txt = "";
	if ('files' in fileAttach) 
	{
		for (var i = 0; i < fileAttach.files.length; i++) 
		{
			var file = fileAttach.files[i];
			var filename = file.name;
			console.log("ext: " + filename.split('.').pop());
			if ((file.name).split('.').pop() != "xml") 
			{
				txt+= "<br><strong>Please attach a .xml file</br></strong>";
				console.log(txt);
			}
			else 
			{
				txt+= filename +"\n";
				//Creating storage reference
				//var firebaseRef  = firebase.storage().ref('/CCDFiles/' + filename);
				//console.log(firebaseRef);
				//var uploadTask = firebaseRef.put(file);
				//console.log(uploadTask.snapshot.downloadFile);
			}
		}
	}
	document.getElementById("fileList").innerHTML += txt;	
}
