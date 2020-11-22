<?php
include "menu.php";



include "../config/".$ns.".conf.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";


include "datetime.php";


// Подключаемся к базе
$link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");

if (!$link) {
    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}



$strSQL ="select 

dt,												# 1
@dAirTemp:=".$dAirTemp.",
@RootTemp:=".$RootTemp.",
@EcTempRaw:=".$EcTempRaw.",
@LightRaw:=".$LightRaw.",
@dist:=".$dist.",
@A1:=".$A1.",
@A2:=".$A2."


from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt limit $limit";


//@lev:=intpl(".$dist."),

// Выполняем запрос
$rs=mysqli_query($link, $strSQL);
$numb=mysqli_num_rows($rs);
mysqli_data_seek($rs,$numb-1);
$row=mysqli_fetch_row($rs);
mysqli_data_seek($rs,0);


include("tbl.php");

?>
