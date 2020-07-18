<?php
include "top.php";


$ns=$_GET['ns'];



if (empty($_GET['days'])){$_GET['days']="-0 days";}
if (empty($_GET['wsdt'])){$_GET['wsdt']=date("Y-m-d",strtotime($_GET['days']))." 00:00:00";}
if (empty($_GET['wpdt'])){$_GET['wpdt']=date("Y-m-d")." 23:59:59";}
if (empty($_GET['limit'])){$_GET['limit']="100000";}

include "../config/".$ns.".conf.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";


$wsdt=$_GET['wsdt'];
$wpdt=$_GET['wpdt'];
$limit=$_GET['limit'];




// Подключаемся к базе

include "sql.php";




$AirTemp=$row[1];
$Humidity=$row[2];
$WaterTemp=$row[3];
$WaterTempEC=round($row[9],3);
$WaterTempECraw=$row[4];
$EC=$row[14];
$Level=$row[15];
$LightRaw=round($row[5],0);
$Lux=round($row[16],0);
$L1=$Level+$LevelAdd;
$L2=$LevelFull-$Level-$La;
$ECn=(-($EC*$L1 - $ECPlan*$L1 - $ECPlan*$L2 )/$L2);
$Soiln=$ECn*$Slk*($L2);
$levsm=$row[6];
$lasttime=date("U") - date("U",strtotime($row[0]) );


echo ("Дата: ".$row[0]." обновлено: ".$lasttime." сек. назад");
echo "<br>";
echo ("<br>Температура воздуха: ".$AirTemp."°C");
echo ("<br>Температура раствора (корни): ".$WaterTemp."°C");
echo ("<br>Температура раствора (бак): ".$WaterTempEC."°C (raw=".$WaterTempECraw.")");
echo ("<br>Влажность воздуха: ".$Humidity."%");
echo ("<br>Освещенность: ".$Lux." lux (raw: ".$LightRaw.")<br>");
echo ("<br>Текущий ЕС: ".round($EC,3)." мСм/см");
echo ("<br>Остаток в баке: <b>".round($Level,1)." л.</b> (".round($levsm,2)." см) ".round(100-($LevelFull-$Level)/$LevelFull*100,0)."%");
echo ("<br>Дополнительно в системе: ".round($LevelAdd,1)." л. Общий остаток раствора: ".round($L1,1)." л");
echo ("<br>Предельный объем бака: ".round($LevelFull,1)." л. Защита от аварийного перелива: ".round($La,1));
echo ("<br>Для получения ЕС=".$ECPlan." мСм/см нужно долить: <b>". round($L2,1)."л.</b> до уровня ".($LevelFull-$La).", c ЕС=".round( $ECn   ,2)." мСм/см" );
echo ("<br>Это: <b>".round($Soiln,2)." грамм</b> солей или по ".round( $Soiln/2/$konc*1000,0)." мл концентратов ".$konc.":1 с каждого");

?>

