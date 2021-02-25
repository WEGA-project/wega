<?php
include_once "menu.php";

$ns=$_GET['ns'];
//$namesys=dbval("namesys",$ns);
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
include_once "helper.php";

echo "<br>";
echo "<br>";
include_once "datetime.php";



$strSQL ="select 

dt,
".$p_AirTemp.",
".$p_RootTemp.",
".$p_ECtemp.",
".$p_AirHum.",
".$p_Lux.",
".$p_pH.",
".$p_EC.",
".$p_lev.",
".$p_soil."


from sens 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'

order by dt";

echo "<br>";

include "sqltocsv.php";


$text='
set terminal png size 1200,2400
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
//set multiplot layout 7, 1
set multiplot layout 7,1

set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]


############## plot2 temp ######################

set ylabel "градусы"
set title "Температура"
plot    \
	"'.$csv.'" using 1:2 w l title "Воздух", \
	"'.$csv.'" using 1:3 w l title "Корни", \
	"'.$csv.'" using 1:4 w l title "Бак", \


unset ylabel
unset title


set title "Влажность"
set ylabel "%"

plot    \
	"'.$csv.'" using 1:5 w l title "Датчик влажности", \

unset ylabel
unset title


set title "Освещенность"
set ylabel "Киллолюксы"

plot    \
	"'.$csv.'" using 1:6 w l title "Датчик освещенности", \

unset ylabel
unset title

set title "Кислотно-щелочной баланс"


plot    \
	"'.$csv.'" using 1:7 w l title "pH", \

unset ylabel

set title "Электропроводность"
set ylabel "mS/cm"

plot    \
	"'.$csv.'" using 1:8 w l title "EC", \

unset ylabel
unset title


set title "Уровень в питательном баке"
set ylabel "литры"


plot    \
	"'.$csv.'" using 1:9 w l title "Объем в баке", \

unset ylabel
unset title



set title "Колличество растворенных солей"
set ylabel "граммы"

plot    \
	"'.$csv.'" using 1:10 w l title "Остаток солей", \

unset ylabel
unset title





';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';


}
else
{
echo "<h1>Система не выбрана</h1>";
}



?>

