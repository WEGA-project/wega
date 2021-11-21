<?php
include "menu.php";


if ( $_GET['ns'] ){

        include "sqvar.php";
//include "../config/".$ns.".conf.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
$cl=$_GET['cl'];

echo "<h1>".$cl;
echo "</h1>";

$ns=$ns."&cl=".urlencode($cl);

include_once "datetime.php";

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
".$cl."

from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt limit $limit";



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
set terminal png size 1900,700
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
	"'.$csv.'" using 1:2 w l title "'.$cl.'", \




';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';




include "../config/".$ns.".conf.php";


$tb="config";



// $link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");


// //mysqli_query($link, "CREATE DATABASE $my_db");
// mysqli_query($link, "create table $tb (parameter VARCHAR(50)  PRIMARY KEY)");
// mysqli_query($link, "alter table $tb add column value VARCHAR(50)");
// mysqli_query($link, "alter table $tb add column comment VARCHAR(255)");


// echo '
// <form action="" method="get">
//  <input type="hidden" name="ns" value="'.$_GET['ns'].'"/>
//  <input type="hidden" name="cl" value="'.$_GET['cl'].'"/>
//  Параметр: <input type="text" name="parameter" value="'.$_GET['parameter'].'"/>
//  <input type="submit" value="Задать"/>
// </form>';


// $parameter=$_GET['parameter'];

// // Добавляем
// mysqli_query($link, "insert into $tb (parameter, value ) values ( '$parameter', '$cl' )");
// //}







}

else
{
echo "Не выбрана система";
}


?>

