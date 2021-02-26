<?php
include "menu.php";

if ($ns){

include "../config/".$ns.".conf.php";
include "sqvar.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";


include "datetime.php";


$strSQL ="select 

dt,												# 1
".$p_AirTemp.",
".$p_RootTemp.",
".$p_ECtemp."


from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt limit $limit";


include "sqltocsv.php";



$text='
set terminal png size 1200,800
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 1,1
set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]



plot    \
	"'.$csv.'" using 1:2 w l title "Температура воздуха", \
	"'.$csv.'" using 1:3 w l title "Температура корней", \
	"'.$csv.'" using 1:4 w l title "Температура бака", \





';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';




}
else
{
echo "Не выбрана система";
}


?>

