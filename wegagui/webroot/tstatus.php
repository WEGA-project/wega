<?php


echo "<table border=1><tr>";
echo "<td>Дата и время замера<td>".sensval("dt",$ns). "</tr>";
echo "<td>Влажность воздуха<td>".round($AirHum,1)."% </tr>";
echo "<td>Температура воздуха<td>".round($AirTemp,2)."°C </tr>";
echo "<td>Температура в зоне корней<td>".round($RootTemp,2)."°C </tr>";
echo "<td>Температура раствора в баке<td>".round($tempEC,2)."°C </tr>";
if ($Lux){ echo "<td>Освещенность<td>".round($Lux,3)." kLux </tr>";}
echo "<td>Удельная электропроводность ЕС<td>".round($ec,3)." mS/cm </tr>";
if($ph){ echo "<td>Водородный показатель pH<td>".round($ph,3)." </tr>";}
echo "<td>Уровень раствора в баке <td>".round($lev,1)." литр. </tr>";
echo "<td>Общий остаток раствора в системе <td>".round($L1,1)." литр. </tr>";

echo "</table>";

?>
