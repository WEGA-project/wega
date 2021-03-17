<?php
include "menu.php";

$ns=$_GET['ns'];

if ( $_GET['ns'] ){
      include_once "func.php";
      include_once "sqvar.php";

$namebot=dbval("Ev_namebot",$ns);
$token=dbval("Ev_token",$ns);
$chat_id=dbval("Ev_chat_id",$ns);


//$msg=system("curl -s -X POST https://api.telegram.org/".$namebot.":".$token."/getUpdates -d chat_id=".$chat_id);

//echo $msg;
//echo convert_uudecode($msg);

//getUpdates?offset=823200646
if ($_GET["offset"]) {$offset=$_GET["offset"];}else{$offset=0;}
//?offset=".$offset
$url="https://api.telegram.org/bot".$token."/getUpdates?offset=".$offset;

//  Initiate curl
$ch = curl_init();
// Will return the response, if false it print the response
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
// Set the url
curl_setopt($ch, CURLOPT_URL,$url);
// Execute
$result=curl_exec($ch);
// Closing
curl_close($ch);

// Will dump a beauty json :3
//$rjson=var_dump(json_decode($result, true));
$jres=json_decode($result, true);


foreach ($jres as $v1) 
 {
    foreach ($v1 as $v2) 
     {
        echo "<br>";
        $msgdate=date('d.m.Y H:i:s',$v2[message][date]);
        $update_id=$v2[update_id];
        $username=$v2[message][from][username];
        $text=$v2[message][text];
        $chatid=$v2[message][chat][id];

        echo "date: ".$msgdate."<br>";
        echo "update_id: ".$update_id."<br>";
        echo "chat_id: ".$chatid."<br>";
        echo "username: ".$username."<br>";
        echo "text: ".$text."<br>";
        
        //echo $v2[message_id];
        echo "<br>";
        echo'<pre>';
        //var_dump ($v2);
        var_dump ($v2);
        echo'</pre>';
     }




    }

    if ($update_id){
        echo "<br><a href=telegrambot.php?ns=".$ns."&offset=".($update_id+1).">".Очистить."</a>";
           }else {echo "<br>Нет свежих сообщений";}

}
else

{
 echo "Не выбрана система";
}
?>