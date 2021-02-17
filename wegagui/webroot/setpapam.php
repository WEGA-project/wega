<?php

$ns=$_GET['ns'];
$p_name=$_GET['parameter'];


include "../config/".$ns.".conf.php";
include "func.php";



if ( $my_db ){

$p_value=dbval($p_name,$ns);
$p_comment=dbcomment($p_name,$ns);

// Добавляем или обновляем
if ( $_GET['act'] == 'set' ) {
setdbval($ns,$_GET['parameter'],$_GET['value'],$_GET['comment']);
header("Location: ".$_SERVER['HTTP_REFERER']);
 }


echo "
           <form>
              <form action='' method='get'>
                   <input type='hidden' name='ns' value=$ns>
                   Имя параметра: <input type='text' readonly name='parameter' value=".$p_name."><br>
                   Параметр: <input type='text' name='value' value='".$p_value."'><br>
                   Коментарий: <input type='text' name='comment' value='".$p_comment."'><br>
              <input type='submit' value='set' name='act'>
              <input type='button' onclick='history.back();' value='Back'/>
           </form>
";


}



?>
