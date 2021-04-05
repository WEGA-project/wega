<?php

$start = microtime(true);

include_once "menu.php";
//include "func.php";

if ($ns){
include "sqvar.php";

//include "../config/".$ns.".conf.php";

echo "<h1>".$namesys."</h1>";
echo $comment;
echo "<br>";

echo "<h2>Калибровка датчика освещенности</h2>";


if (dbval("LightRAW",$ns) != "null") {

$pHraw=dbval("tRraw",$ns);
$RootTemp=dbval("RootTemp",$ns);


echo "<h4>Калибровка по трём точкам<br></h4>";
echo "<br>Точка 1 (минимальный уровень яркости)<br>";
pedit("pR_val_p1",$ns,0,"kLux Значение яркости точки 1");
pedit("pR_raw_p1",$ns,0,"Значение АЦП RAW точки 1");

echo "<br>Точка 2 (средний уровень яркости)<br>";
pedit("pR_val_p2",$ns,20,"kLux Значение яркости точки 2");
pedit("pR_raw_p2",$ns,600,"Значение АЦП RAW точки 2");

echo "<br>Точка 3 (высокий уровень яркости)<br>";
pedit("pR_val_p3",$ns,60,"kLux Значение яркости точки 3)");
pedit("pR_raw_p3",$ns,1200,"Значение АЦП RAW точки 3");

	$pR_val_p1=floatval(dbval("pR_val_p1",$ns));
	$pR_val_p2=floatval(dbval("pR_val_p2",$ns));
	$pR_val_p3=floatval(dbval("pR_val_p3",$ns));
	$pR_raw_p1=floatval(dbval("pR_raw_p1",$ns));
	$pR_raw_p2=floatval(dbval("pR_raw_p2",$ns));
	$pR_raw_p3=floatval(dbval("pR_raw_p3",$ns));


include "sqfunc.php";

include "datetime.php";

$P_LightRAW=dbval("LightRAW",$ns);
$LightRAW=sensval($P_LightRAW,$ns);


echo "<br><br>RAW (".$P_LightRAW.")=".$LightRAW;


$Light=sensval("fpR(".dbval("LightRAW",$ns).")",$ns);

echo "<br>Яркость ".round($Light,2)." kLux";

$strSQL ="select 

dt,
".$p_LightRaw.",
".$p_Lux."


from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt";


include "sqltocsv.php";


$text='
set terminal png size 1300,800
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 2,1
set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]



plot    \
	"'.$csv.'" using 1:2 w l title "'.dbval("LightRAW",$ns).'", \

plot    \
	"'.$csv.'" using 1:3 w l title "Яркость", \


';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';

}
else
{
echo "Датчик освещенности не найден. Если он есть сопоставьте соответсвующее поле в базе";
}

}
else
{
echo "Не выбрана система";
}

$time = microtime(true) - $start;
echo "<h0>".$time."</h0>";
?>

