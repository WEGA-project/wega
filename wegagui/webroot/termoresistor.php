<?php
include "menu.php";

if ($ns){

//include "../config/".$ns.".conf.php";
include "sqvar.php";

echo "<h1>".$namesys."</h1>";
echo $comment;
echo "<br>";

echo "<h2>Калибровка терморезистора</h2>";


include_once "func.php";



if ($p_ECtempRAW != "null") {

echo "<h4>Калибровка по трём точкам<br></h4>";


echo "<br>Точка 1<br>";
pedit("tR_val_p1",$ns,36,"tR Темература точки 1");
pedit("tR_raw_p1",$ns,2300,"tR Значение АЦП RAW точки 1");

echo "
<details>
 <summary>Подробнее</summary> Точка номер один
</details>
";

echo "<br>Точка 2<br>";
pedit("tR_val_p2",$ns,23,"tR Темература точки 2");
pedit("tR_raw_p2",$ns,1677,"tR Значение АЦП RAW точки 2");

echo "<br>Точка 3<br>";
pedit("tR_val_p3",$ns,6,"tR Темература точки 3");
pedit("tR_raw_p3",$ns,920,"tR Значение АЦП RAW точки 3");

pedit("tR_val_korr",$ns,0,"Линейная коррекция");

	$tR_val_p1=floatval(dbval("tR_val_p1",$ns));
	$tR_val_p2=floatval(dbval("tR_val_p2",$ns));
	$tR_val_p3=floatval(dbval("tR_val_p3",$ns));
	$tR_raw_p1=floatval(dbval("tR_raw_p1",$ns));
	$tR_raw_p2=floatval(dbval("tR_raw_p2",$ns));
	$tR_raw_p3=floatval(dbval("tR_raw_p3",$ns));
	$tR_val_korr=floatval(dbval("tR_val_korr",$ns));




include "datetime.php";


echo "<br><br>RAW (".$p_ECtempRAW.")=".$ECtempRAW;
echo "<br>Расчетная температура (WaterTemp)=".round($WaterTemp,3);
echo "<br>Температура сравнения (".$p_RootTemp.")=".$RootTemp;


$strSQL ="select 

dt,												# 1
".$p_ECtempRAW.",
".$p_ECtemp.",
".$p_RootTemp."


from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt limit $limit";

include "sqltocsv.php";






$text='
set terminal png size 900,2000
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 4,1
set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]



plot    \
	"'.$csv.'" using 1:2 w l title "'.dbval("ECtempRAW",$ns).'", \

plot    \
	"'.$csv.'" using 1:3 w l title "ECtemp", \

plot    \
	"'.$csv.'" using 1:4 w l title "'.dbval("RootTemp",$ns).'", \

plot    \
	"'.$csv.'" using 1:3 w l title "ECtemp", \
	"'.$csv.'" using 1:4 w l title "'.dbval("RootTemp",$ns).'", \

';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';

}
else
{
echo "Датчик pH не задан. Если он есть сопоставьте соответсвующее поле в базе";
}

}
else
{
echo "Не выбрана система";
}

include "sqfunc.php";

?>

