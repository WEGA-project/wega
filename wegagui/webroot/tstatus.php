<?php
if ($OutDate < $Max_OutDate){$OutDate_Status = "Норма";} else {$OutDate_Status = "Проблема";}

echo "<table border=1><tr>";
echo "<th>Параметр<th>Значение<th>Статус</tr>";
echo "<td>Дата и время замера<td>".$dt. "<td>".$OutDate_Status."</tr>";

if ($p_AirHum != 'null' and $p_AirHum)  {
    if ($AirHum < $Max_AirHum and $AirHum > $Min_AirHum ) {$AirHum_Status = "Норма";} else {$AirHum_Status = "Проблема";}
    echo "<td><a href=plotdb.php?ns=".$ns."&cl=".urlencode($p_AirHum).">Относительная влажность воздуха</a><td>".round($AirHum,1)."%<td>".$AirHum_Status."</tr>";
    echo "<td><a href=plotdb.php?ns=".$ns."&cl=".urlencode($p_Pa).">Абсолютная влажность воздуха</a><td>".round($Pa,2)." г/м³<td>".$AirHum_Status."</tr>";
}

if ($p_AirTemp != 'null' and $p_AirTemp)  {
    if ($AirTemp < $Max_AirTemp and $AirTemp > $Min_AirTemp ) {$AirTemp_Status = "Норма";} else {$AirTemp_Status = "Проблема";}
    echo "<td><a href=plotdb.php?ns=".$ns."&cl=".urlencode($p_AirTemp).">Температура воздуха</a><td>".round($AirTemp,2)."°C <td>".$AirTemp_Status."</tr>";

}

if ($p_RootTemp != 'null' and $p_RootTemp)  {
    if ($RootTemp < $Max_RootTemp and $RootTemp > $Min_RootTemp ) {$RootTemp_Status = "Норма";} else {$RootTemp_Status = "Проблема";}
    echo "<td><a href=plotdb.php?ns=".$ns."&cl=".urlencode($p_RootTemp).">Температура в зоне корней</a><td>".round($RootTemp,2)."°C <td>".$RootTemp_Status."</tr>";

}

if ($p_ECtempRAW != 'null' and $p_ECtempRAW)  {
    if ($WaterTemp < $Max_WaterTemp and $WaterTemp > $Min_WaterTemp ) {$WaterTemp_Status = "Норма";} else {$WaterTemp_Status = "Проблема";}
    echo "<td><a href=plotdb.php?ns=".$ns."&cl=".urlencode($p_ECtemp).">Температура раствора в баке</a><td>".round($tempEC,2)."°C <td>".$WaterTemp_Status."</tr>";
}

if ($P_A1 != 'null' and $P_A2 != 'null' and $P_A1 and $P_A2)  {
    if ($ec < $Max_EC and $ec > $Min_EC ) {$ec_Status = "Норма";} else {$ec_Status = "Проблема";}
    echo "<td><a href=plotdb.php?ns=".$ns."&cl=".urlencode($p_EC).">Удельная электропроводность ЕС</a><td>".round($ec,3)." mS/cm <td>".$ec_Status."</tr>";
}

if ($p_ph != 'null' and $p_ph)  {
    if ($ph < $Max_pH and $ph > $Min_pH ) {$pH_Status = "Норма";} else {$pH_Status = "Проблема";}
    if($ph){      echo "<td><a href=plotdb.php?ns=".$ns."&cl=".urlencode($p_pH).">Водородный показатель pH</a><td>".round($ph,3)." <td>".$pH_Status."</tr>";}

}

if ($p_LightRaw != 'null' and $p_LightRaw)  {
    echo "<td><a href=plotdb.php?ns=".$ns."&cl=".urlencode($p_Lux).">Освещенность</a><td>".round($Lux,3)." kLux<td></tr>";
}

if ($p_CO2 != 'null' and $p_CO2)  {
   if ($CO2 < $Max_CO2 and $CO2 > $Min_CO2 ) {$CO2_Status = "Норма";} else {$CO2_Status = "Проблема";}
   echo "<td><a href=plotdb.php?ns=".$ns."&cl=".urlencode($p_CO2).">Уровень CO2</a><td>".round($CO2,3)." ppm<td>".$CO2_Status."</tr>";
}

if ($p_LightRaw != 'null' and $p_LightRaw)  {
    if ($lev < $Max_Level and $lev > $Min_Level ) {$lev_Status = "Норма";} else {$lev_Status = "Проблема";}
    if ($lev < $Crit_Level ) {$lev_Status = "АВАРИЯ";}
    echo "<td><a href=plotdb.php?ns=".$ns."&cl=".urlencode($p_lev).">Уровень раствора в баке </a><td>".round($lev,1)." литр. <td>".$lev_Status."</tr>";
    echo "<td>Общий остаток раствора в системе <td>".round($L1,1)." литр. <td></tr>";
    
}


echo "</table>";

?>
