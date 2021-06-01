<?php
include "menu.php";
include_once "func.php";

//$ns=$_GET['ns'];



if ( $ns ){
include "sqvar.php";

//include "../config/".$ns.".conf.php";
echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
echo "<br>";
echo "<h2>Сопоставление полей в базе данных</h2>";



form($ns,"A1","Датчик ЕС при положительной фазе (RAW)");
form($ns,"A2","Датчик ЕС при отрицательной фазе (RAW)");
form($ns,"ECtempRAW","Датчик EC температура (RAW)");
form($ns,"pHraw","Датчик pH (RAW)");
form($ns,"LightRAW","Датчик яркости света (RAW)");
form($ns,"RootTemp","Температура в зоне корней (град.)");
form($ns,"AirTemp","Температура воздуха (град.)");
form($ns,"AirHum","Влажность воздуха (%)");
form($ns,"Dst","Уровнемер (см)");
form($ns,"IntTempRaw","Температура внутри корпуса контроллера");
form($ns,"VddRaw","Напряжение питания");
}

else
{
echo "Не выбрана система";
}


//include "func.php";
