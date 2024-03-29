<?php

include_once "menu.php";

$ns=$_GET['ns'];
include "../config/".$ns.".conf.php";
include_once "func.php";


if ($ns){
if (empty($_GET['days'])){$_GET['days']="-0 days";}
if (empty($_GET['wsdt'])){$_GET['wsdt']=date("Y-m-d",strtotime($_GET['days']))." 00:00:00";}
if (empty($_GET['wpdt'])){$_GET['wpdt']=date("Y-m-d")." 23:59:59";}
if (empty($_GET['limit'])){$_GET['limit']="100000";}

include "sqvar.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
echo "<br>";

include "tstatus.php";

if ($p_DstRAW != 'null' and $P_A1 != 'null' and $P_A2 != 'null' and $DstRAW and $A1 and $A2) {
echo "<br>";
    include_once "helper.php";
}

echo "<br>";
echo "<br>";
include_once "datetime.php";
$pref="";


// Графики температур
if ($p_AirTemp != 'null' or $p_RootTemp != 'null' or $p_ECtemp !='null') {
    $pref="temper";
    $xsize=1000;
    $ysize=400;


$gimg=$gimg.$pref;
$img=$img.$pref;

$strSQL = "select dt";
if ($AirTemp){$strSQL = $strSQL . "," . $p_AirTemp;}    else {$strSQL = $strSQL . ",null";}
if ($RootTemp){$strSQL = $strSQL . "," . $p_RootTemp;}  else {$strSQL = $strSQL . ",null";}
if ($ECtempRAW){$strSQL = $strSQL . "," . $p_ECtemp;}   else {$strSQL = $strSQL . ",null";}
if ($IntTempRaw){$strSQL = $strSQL . "," . $IntTempRaw;}   else {$strSQL = $strSQL . ",null";}

$strSQL = $strSQL . "

from sens 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt";
include "sqltocsv.php";

$name="Температура";
$dimens="°C";

$nplot1="Воздух";
$nplot2="В зоне корней";
$nplot3="В баке";
$nplot4="Система";

$LimitUP=$Max_AirTemp ;
$LimitDOWN=$Min_AirTemp;
gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
$LimitUP="";
$LimitDOWN="";

}


// Влажность
if ($p_AirHum != 'null' and $AirHum) {
    $pref="hum";
    $xsize=1000;
    $ysize=400;
 
    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
    ".$p_AirHum."

    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="Относительная влажность";
    $dimens="%";
    $nplot1="воздух";

    $LimitUP=$Max_AirHum ;
    $LimitDOWN=$Min_AirHum;
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    $LimitUP="";
    $LimitDOWN="";
    }

// Давление
if ($p_AirPress != 'null' and $AirPress) {
    $pref="press";
    $xsize=1000;
    $ysize=400;
 
    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
    ".$p_AirPress."

    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="Давление";
    $dimens="мм.рт.ст.";
    $nplot1="воздух";

    $LimitUP=$Max_AirPress ;
    $LimitDOWN=$Min_AirPress;
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    $LimitUP="";
    $LimitDOWN="";
    }

// Уровень CO2
if ($p_CO2 != 'null' and $CO2) {
    $pref="hum";
    $xsize=1000;
    $ysize=400;
 
    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
    ".$p_CO2."

    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="Уровень CO2";
    $dimens="ppm";
    $nplot1="";

    $LimitUP=$Max_CO2 ;
    $LimitDOWN=$Min_CO2;
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    $LimitUP="";
    $LimitDOWN="";
    }


// График EC
if ($P_A1 != 'null' and $P_A2 != 'null' and $A1 and $A2) {


    $pref="ec";    
    $xsize=1000;
    $ysize=400;
    

    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
 	".$p_EC."
    
    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="EC (Удельная электропроводность раствора)";
    $dimens="мСм/см";
    $nplot1="ЕС";
    //$nplot2="ЕС без термокомпенсации";

    $LimitUP=$Max_EC ;
    $LimitDOWN=$Min_EC;
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    $LimitUP="";
    $LimitDOWN="";
    }

// График pH

if ($p_pHraw != 'null' and $p_pHraw) {
    $pref="ph";
    $xsize=1000;
    $ysize=400;
    

    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
    if (".$p_pH." < 10 and ".$p_pH." > 1, ".$p_pH.", null)
    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'

    order by dt";
    include "sqltocsv.php";
    
    $name="pH (Кислотно-щелочной баланс)";
    $dimens="";
    $nplot1="Бак";

    $LimitUP=$Max_pH ;
    $LimitDOWN=$Min_pH;
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    $LimitUP="" ;
    $LimitDOWN="";
    }


// График света

if ($p_LightRaw != 'null' and $Lux) {
    $pref="light";
    $xsize=1000;
    $ysize=400;
    

    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
    ".$p_Lux."
    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="Освещение";
    $dimens="кЛюкс";
    $nplot1="Зона листвы";

    
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    }

// График уровня раствора
if ($p_Dst != 'null' and $lev) {
    $pref="level";
    $xsize=1000;
    $ysize=400;
    

    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
    ".$p_lev."
    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="Объем раствора";
    $dimens="Литры";
    $nplot1="Бак";

   
    $LimitUP=$Max_Level ;
    $LimitDOWN=$Min_Level;
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    $LimitUP="";
    $LimitDOWN="";   
    }

// График остатка солей

if ($p_Dst != 'null' and $P_A1 != 'null' and $P_A2 != 'null' and $lev and $A1 and $A2) {
    
    $pref="soil";
    $xsize=1000;
    $ysize=400;
    

    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
    ".$p_soil."
    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="Суммарный вес растворенных солей";
    $dimens="Граммы";
    $nplot1="Суммарно в системе";

    $LimitUP=($LevelFull+$LevelAdd)*($ECPlan*$Slk);
    $LimitDOWN=0.1;
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    $LimitUP="";
    $LimitDOWN="";   
    }

}
else
{
echo "<h1>Система не выбрана</h1>";
}










?>

