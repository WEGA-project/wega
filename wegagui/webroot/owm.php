<?php
include "menu.php";


$ns=$_GET['ns'];



if (empty($_GET['days'])){$_GET['days']="-0 days";}
if (empty($_GET['wsdt'])){$_GET['wsdt']=date("Y-m-d",strtotime($_GET['days']))." 00:00:00";}
if (empty($_GET['wpdt'])){$_GET['wpdt']=date("Y-m-d")." 23:59:59";}
if (empty($_GET['limit'])){$_GET['limit']="100000";}

include "../config/".$ns.".conf.php";

echo "<h1>".Погода;
echo "</h1>";

$owm="/var/log/sensors/owm.log";


echo "<br>";

include "datetime.php";


mysqli_data_seek($rs,0);


echo "<br><table border='1'>";


$filename=$csv;
$handler = fopen($filename, "w");

while($id=mysqli_fetch_row($rs))
        { 
        for ($x=0; $x<=count($id)-1; $x++) 
                {
		$text= $id[$x].";";
		fwrite($handler, $text);
                }
	fwrite($handler, "\n");


        }



fclose($handler);
$filename=$gnups;
$handler = fopen($filename, "w");



$text='
set terminal png size 1000,2000
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
//set multiplot layout 7, 1
set multiplot layout 4,1

set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]


############## plot2 temp ######################
set title "Погодные условия - облачность"
set ylabel "%"
set yrange[0:100]

plot    \
	"'.$owm.'" using 1:($5) w boxes fs solid 0.01 title "Облачность" lc rgb "grey", \

unset yrange
unset ylabel
unset title



set title "Погодные условия - влажность"
set ylabel "%"

plot    \
	"/var/log/sensors/owm.log" using 1:3 w l title "Относительная влажность", \

unset ylabel
unset title


set title "Погодные условия - Температура"
set ylabel "градусы"
plot    \
	"/var/log/sensors/owm.log" using 1:2 w l title "Улица", \


unset ylabel
unset title


set title "Погодные условия - Атмосферное давление"
set ylabel "мм. ртутного столба"

plot    \
	"/var/log/sensors/owm.log" using 1:($4/1.333333) w l title "Давление", \

unset ylabel
unset title




';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';





?>

