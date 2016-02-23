<?php
//system("sudo python /home/pi/fishtank/lights.py 19 ON");
//die;

$key = "";

$headers = apache_request_headers();
foreach ($headers as $header => $value) {
    //echo "$header: $value <br />\n";
    if ($header == "Authorization") {
        $key = "$value";
    }
}

if ($key == "Basic a2V2bzpiYW5hbmFz") {
    
    if($_POST){
        $cmd = "python /home/pi/fishtank/lights.py ";
        
       if(isset($_POST['white'])){
           $cmd .= "26 ".strtoupper($_POST['white']);
       } else if(isset($_POST['blue'])){
           $cmd .= "19 ".strtoupper($_POST['blue']);
       } else if(isset($_POST['moon'])){
           $cmd .= "20 ".strtoupper($_POST['moon']);
       }
       
//       echo $cmd;
       system($cmd);
    }
} else {
    echo "No soup for you!";
} 

die;
?>

