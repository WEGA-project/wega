<?php
include "menu.php";



include "../config/".$ns.".conf.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";


include "datetime.php";


// Подключаемся к базе
$link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");

if (!$link) {
    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}

//my_arg FLOAT, varVolt FLOAT, up1 FLOAT, max1 FLOAT,min1 FLOAT
echo "<h3>Аргументы функций:</h3>";
echo "\$DistC0=".$DistC0."<br>";
echo "\$DistC1=".$DistC1."<br>";
echo "\$DistC2=".$DistC2."<br>";
echo "\$DistC3=".$DistC3."<br>";
echo "\$DistC4=".$DistC4."<br>";
echo "<br>";

$strSQL ="select 

dt,
".$DistC0.",
".$DistC1.",
levmin(".$DistC1.")

from $tb 
where dt  >  '".$wsdt." '- INTERVAL 1 DAY
 and  dt  <  '".$wpdt."'
order by dt limit $limit";

//@dist:='".$dist." '

//@lev:='".$f_lev." '

//@Dist:=( 20.046796*sqrt(273.15+WaterTemp) )/10000*(us/2),
//@DistF:=kalman(@dist,19,0.8,3,1)

// @DistF:=kalman(@dist,10,30,140,35)

// Выполняем запрос
$rs=mysqli_query($link, $strSQL);
$numb=mysqli_num_rows($rs);
mysqli_data_seek($rs,$numb-1);
$row=mysqli_fetch_row($rs);
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
set terminal png size 1800,2000
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
	"'.$csv.'" using 1:2 w l title "Dist", \
	"'.$csv.'" using 1:3 w l title "g1", \
	"'.$csv.'" using 1:(19) w l , \


#	"'.$csv.'" using 1:4 w l title "g2", \
#	"'.$csv.'" using 1:5 w l title "g3", \
#	"'.$csv.'" using 1:6 w l title "g4", \

plot    \
	"'.$csv.'" using 1:3 w l title "g1", \


';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';





?>

