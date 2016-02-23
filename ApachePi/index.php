<!DOCTYPE html>
<html>
<title>Kevin's Tank</title>
<head>
<style>

h1 {
  margin: 0;
}

body {
  background-color:#EDF2E9;
}

#container { 
 margin: 0 auto;
 width:640px;
}

</style>
</head>
<body>

<div id="container">
<h1>Kevin's Tank!</h1>
<br/>
<input id="checkbox" type="checkbox" onclick="startStop();" checked/> Auto 60 Second Refresh?
<br/>
Updated: <?php echo date('m/d/Y g:i:s A'); ?><br/>
<img src="tank.jpg?<?php echo time(); ?>"/>
</br>
<strong>Temp: <?php system("python /home/pi/fishtank/temp.py"); ?> F</strong>

</div>

</body>
<script>

var x = document.getElementById("checkbox").checked;
console.log("Init Checked: "+x);


var timer = setTimeout(function(){
   refresh();
}, 60000);


function startStop() {
	 var isChecked = document.getElementById("checkbox").checked;
	 console.log("Is checked: "+isChecked);
	 if(isChecked){
		refresh();
	 } else {
	 	clearTimeout(timer);
	 }
}

function refresh() {
	window.location.reload(1);
}
</script>
</html>
