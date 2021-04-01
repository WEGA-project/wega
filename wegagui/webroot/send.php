<?php

$ns=$_GET['ns'];

if ( $_GET['ns'] ){
      include_once "func.php";
      include_once "sqvar.php";

    
//$OutDate = strtotime("now")-strtotime($dt);

if ($OutDate < $Max_OutDate){


// Проверки выхода за пороговые значения
// Температура воздуха
if ($AirTemp > $Max_AirTemp) { $EventBody=$EventBody."Превышение температуры воздуха ". $AirTemp." > ".$Max_AirTemp."\n";}
if ($AirTemp < $Min_AirTemp) { $EventBody=$EventBody."Низкая температуры воздуха ". $AirTemp." < ".$Min_AirTemp."\n";}

// Температура корней
if ($RootTemp > $Max_RootTemp) { $EventBody=$EventBody."Превышение температуры зоны корней ". $RootTemp." > ".$Max_RootTemp."\n";}
if ($RootTemp < $Min_RootTemp) { $EventBody=$EventBody."Низкая температуры зоны корней ". $RootTemp." < ".$Min_RootTemp."\n";}

// Температура бака
if ($tempEC > $Max_WaterTemp) { $EventBody=$EventBody."Превышение температуры расвтора ". round($tempEC,2)." > ".$Max_WaterTemp."\n";}
if ($tempEC < $Min_WaterTemp) { $EventBody=$EventBody."Низкая температура раствра ". round($tempEC,2)." < ".$Min_WaterTemp."\n";}

// Влажность воздуха
if ($AirHum > $Max_AirHum) { $EventBody=$EventBody."Высокая влажность воздуха ". $AirHum."% > ".$Max_AirHum."%\n";}
if ($AirHum < $Min_AirHum) { $EventBody=$EventBody."Низкая влажность воздуха ". $AirHum."% < ".$Min_AirHum."%\n";}




// Уровень раствора
if ($lev < $Crit_Level) {$EventBody=$EventBody."КРИТИЧЕСКИ НИЗКИЙ УРОВЕНЬ РАСТВОРА! \n";}
if ($lev < $Min_Level) { 
      $EventBody=$EventBody."Уровень раствора ниже заданного ". round($lev,1)."л < ".$Min_Level."л\n";
      $EventBody=$EventBody."Текущий ЕС = ". round($ec,3)." мСм/см\n";
      $EventBody=$EventBody."Для получения ЕС=".$ECPlan." мСм/см нужно долить: ". round($L2,1)."л. до уровня ".($LevelFull-$La).", c ЕС=".round( $ECn   ,2)." мСм/см\n";
      $EventBody=$EventBody."Это: ".round($Soiln,2)." грамм солей или по ".round( $Soiln/2/$konc*1000,0)." мл концентратов ".$konc.":1 с каждого";
}

// ЕС
if ($ec > $Max_EC) { $EventBody=$EventBody."Высокий EC расвтора ". round($ec,3)." > ".$Max_EC."\n";}
if ($ec < $Min_EC) { $EventBody=$EventBody."Низкий EC расвтора ". round($ec,3)." < ".$Min_EC."\n";}

// pH
if (dbval("pHraw",$ns) != "null"){
      if ($ph > $Max_pH) { $EventBody=$EventBody."Высокий pH расвтора ". round($ph,3)." > ".$Max_pH."\n";}
      if ($ph < $Min_pH) { $EventBody=$EventBody."Низкий pH расвтора ". round($ph,3)." < ".$Min_pH."\n";}
  }
}

else // Если данные давно не поступали
{

       $EventBody="Данные от устройства отсутсвуют более чем ".$OutDate." сек"."\n";
       $EventBody=$EventBody."Последние данные получены ". $dt."\n";

}


if ($EventBody){
      $EventBody=$namesys."\n".$EventBody;

echo "<pre>";

echo $EventBody;

echo "</pre>";


$namebot=dbval("Ev_namebot",$ns);
$token=dbval("Ev_token",$ns);
$chat_id=dbval("Ev_chat_id",$ns);


system("curl -s -X POST https://api.telegram.org/bot".$token."/sendMessage -d text='".$EventBody."' -d chat_id=".$chat_id);
//echo $trep;

}else
{
      echo "Все контрольные параметры в норме, нечего слать";
}




}

else
{
 echo "Не выбрана система";
}




?>

