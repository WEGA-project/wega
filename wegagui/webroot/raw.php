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



$strSQL ="select 

dt,												# 1
@dAirTemp:=".$dAirTemp.",
@RootTemp:=".$RootTemp.",
@EcTempRaw:=".$EcTempRaw.",
@LightRaw:=".$LightRaw.",
@dist:=".$dist.",
@A1:=".$A1.",
@A2:=".$A2."


from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt limit $limit";


//@lev:=intpl(".$dist."),

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
set terminal png size 900,2000
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 8,1
set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]



plot    \
	"'.$csv.'" using 1:2 w l title "dAirTemp", \
	"'.$csv.'" using 1:3 w l title "RootTemp", \

plot    \
	"'.$csv.'" using 1:4 w l title "EcTempRaw", \

plot    \
	"'.$csv.'" using 1:5 w l title "LightRaw", \

plot    \
	"'.$csv.'" using 1:6 w l title "dist", \

plot    \
	"'.$csv.'" using 1:7 w l title "A1", \

plot    \
	"'.$csv.'" using 1:8 w l title "A2", \




';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';





?>

