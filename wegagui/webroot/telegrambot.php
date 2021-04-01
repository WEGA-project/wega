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


if ($_GET["offset"]) {$offset=$_GET["offset"];}else{$offset=0;}
//?offset=".$offset
$url="https://api.telegram.org/bot".$token."/getUpdates?offset=".$offset;


$ch = curl_init();
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_URL,$url);
$result=curl_exec($ch);
curl_close($ch);

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
        
        echo "<br>";
        echo'<pre>';
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