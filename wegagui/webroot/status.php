<?php
include_once "menu.php";

$ns=$_GET['ns'];

if ($ns){

include_once "func.php";
include_once "sqvar.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
echo "<br>";

echo "<h3>Текущие контрольные показания</h3>";

$P_A1=dbval("A1",$ns);
$A1=sensval($P_A1,$ns);

$P_A2=dbval("A2",$ns);
$A2=sensval($P_A2,$ns);

echo "<table border=1><tr>";

echo "<td>Дата и время замера<td>".sensval("dt",$ns). "</tr>";

$AirHum=sensval($p_AirHum,$ns);
 echo "<td>Влажность воздуха<td>".round($AirHum,3)." % </tr>";

$AirTemp=sensval($p_AirTemp,$ns);
 echo "<td>Температура воздуха<td>".round($AirTemp,3)." °C </tr>";

$RootTemp=sensval($p_RootTemp,$ns);
 echo "<td>Температура в зоне корней<td>".round($RootTemp,3)." °C </tr>";

$tempEC=sensval("ftR(".dbval("ECtempRAW",$ns).")",$ns);
 echo "<td>Температура раствора в баке<td>".round($tempEC,3)." °C </tr>";

$Lux=sensval("fpR(".dbval("LightRAW",$ns).")",$ns);
if ($Lux){ echo "<td>Освещенность<td>".round($Lux,3)." kLux </tr>";}

$ec=sensval("EC($P_A1,$P_A2,".$tempEC.")",$ns);
 echo "<td>Удельная электропроводность ЕС<td>".round($ec,3)." mS/cm </tr>";

$ph=sensval("ph(".dbval("pHraw",$ns).")",$ns);
if($ph){ echo "<td>Водородный показатель pH<td>".round($ph,3)." </tr>";}

$lev=sensval("intpl(levmin(".$p_Dst."))",$ns);
 echo "<td>Уровень раствора в баке <td>".round($lev,1)." лит. </tr>";



echo "</table>";

}
else
{
echo "<h1>Система не выбрана</h1>";
}


?>
