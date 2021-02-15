��<?php
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



$y1=6.86;    $x1=12282;
$y2=4.01;    $x2=15070;

$a=(-$x1*$y2+$x2*$y1)/($x2-$x1);
$k=($y2-$y1)/($x2-$x1);


include "func.php";
//$phraw=dbval("pHraw",$ns);


$strSQL ="select 

dt,												# 1
@pHraw:=".dbval("pHraw",$ns).",
@pH:=line2point(19360,6.86,21897,4.01,@pHraw),
@RootTemp:=".$RootTemp.",
@EcTempRaw:=".$EcTempRaw."




from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt limit $limit";

//@pHraw:=".$phraw.",

//@pH:=".$a." + ".$k." * @pHraw

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
set terminal png size 900,1000
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
	"'.$csv.'" using 1:2 w l title "'.dbval("pHraw",$ns).'", \

plot    \
	"'.$csv.'" using 1:3 w l title "pH", \

plot    \
	"'.$csv.'" using 1:5 w l title "RAW-Temperature", \

plot    \
	"'.$csv.'" using 1:4 w l title "Temperature", \



';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';




?>

