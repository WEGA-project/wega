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

if ($p_DstRAW != 'null' and $P_A1 != 'null' and $P_A2 != 'null') {
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

$strSQL ="select 
dt,
".$p_AirTemp.",
".$p_RootTemp.",
".$p_ECtemp."

from sens 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt";
include "sqltocsv.php";

$name="Температура";
$dimens="°C";
$nplot1="Воздух";
$nplot2="Зона корней";
$nplot3="Бак";

gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
}


// Влажность
if ($p_AirHum != 'null') {
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
    $nplot1="Воздух";

    
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    }


// График EC
if ($P_A1 != 'null' and $P_A2 != 'null') {


    $pref="ec";    
    $xsize=1000;
    $ysize=400;
    

    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
 	".$p_EC.",
    EC(".$P_A1.",".$P_A2.",25)
    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="EC (Удельная электропроводность раствора)";
    $dimens="мСм/см";
    $nplot1="ЕС";
    $nplot2="ЕС без термокомпенсации";

    
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    }

// График pH

if ($p_pHraw != 'null') {
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

    
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    }


// График света

if ($p_LightRaw != 'null') {
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
if ($p_Dst != 'null') {
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

    
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    }

// График остатка солей

if ($p_Dst != 'null' and $P_A1 != 'null' and $P_A2 != 'null') {
    
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

    
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    }

}
else
{
echo "<h1>Система не выбрана</h1>";
}










?>

