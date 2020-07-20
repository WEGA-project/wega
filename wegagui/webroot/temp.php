<?php
include "top.php";


$ns=$_GET['ns'];



if (empty($_GET['days'])){$_GET['days']="-0 days";}
if (empty($_GET['wsdt'])){$_GET['wsdt']=date("Y-m-d",strtotime($_GET['days']))." 00:00:00";}
if (empty($_GET['wpdt'])){$_GET['wpdt']=date("Y-m-d")." 23:59:59";}
if (empty($_GET['limit'])){$_GET['limit']="100000";}

include "../config/".$ns.".conf.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";


$wsdt=$_GET['wsdt'];
$wpdt=$_GET['wpdt'];
$limit=$_GET['limit'];

echo '<a href=rep.php?ns='.$ns.'&days=-1%20days>1 день</a>';
echo '  <a href=rep.php?ns='.$ns.'&days=-2%20days>2 дня</a>';
echo '  <a href=rep.php?ns='.$ns.'&days=-7%20days>Неделя</a>';
echo '  <a href=rep.php?ns='.$ns.'&days=-14%20days>2 недели</a><br>';

echo '
<form action="" method="get">
 <p><input type="text" name="ns" value="'.$_GET['ns'].'"/> </p>
 <p>Дата с: <input type="text" name="wsdt" value="'.$_GET['wsdt'].'"/> </p>
 <p>Дата по: <input type="text" name="wpdt" value="'.$_GET['wpdt'].'"/> можно указать любую часть</p>
 <p>Выводить не более: <input type="text" name="limit" value="'.$_GET['limit'].'"/> строк</p>

 <p><input type="submit" value="Найти"/></p>
</form>';



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
@dAirHum:=".$dAirHum.",
@RootTemp:=".$RootTemp.",
@EcTempRaw:=".$EcTempRaw.",
@LightRaw:=".$LightRaw.",
@dist:=-".$dist.",
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
set terminal png size 1900,1000
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
//set format x "%d.%m %H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 4, 2
set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]



plot    \
	"'.$csv.'" using 1:2 w l title "'.$dAirTemp.'", \

plot    \
	"'.$csv.'" using 1:3 w l title "'.$dAirHum.'", \

plot    \
	"'.$csv.'" using 1:4 w l title "'.$RootTemp.'", \

plot    \
	"'.$csv.'" using 1:5 w l title "'.$EcTempRaw.'", \

plot    \
	"'.$csv.'" using 1:6 w l title "'.$LightRaw.'", \

plot    \
	"'.$csv.'" using 1:7 w l title "'.$dist.'", \

plot    \
	"'.$csv.'" using 1:8 w l title "'.$A1.'", \

plot    \
	"'.$csv.'" using 1:9 w l title "'.$A2.'", \


';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';





?>

