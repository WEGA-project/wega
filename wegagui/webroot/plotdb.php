<?php
include "menu.php";


if ( $_GET['ns'] ){


include "../config/".$ns.".conf.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
$cl=$_GET['cl'];

echo "<h1>".$cl;
echo "</h1>";

$stfind="?ns=".$ns."&cl=".$cl;


echo '<h2>Период анализа</h2>';


echo '
<form action="" method="get">
 <input type="hidden" name="ns" value="'.$_GET['ns'].'"/>
 <input type="hidden" name="cl" value="'.$_GET['cl'].'"/>
 Дата с: <input type="text" name="wsdt" value="'.$_GET['wsdt'].'"/>
 по: <input type="text" name="wpdt" value="'.$_GET['wpdt'].'"/>
 <input type="submit" value="Задать"/>
</form>';
echo '<a href='.$stfind.'&days=-0%20days>За сегодя </a>';
echo '<a href='.$stfind.'&days=-1%20days>Со вчера</a>';
echo '  <a href='.$stfind.'&days=-2%20days>2 дня</a>';
echo '  <a href='.$stfind.'&days=-7%20days>Неделя</a>';
echo '  <a href='.$stfind.'&days=-14%20days>2 недели</a>';
echo '  <a href='.$stfind.'&days=-1%20month>за месяц</a>';


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



$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");


//mysqli_query($link, "CREATE DATABASE $my_db");
mysqli_query($link, "create table $tb (parameter VARCHAR(50)  PRIMARY KEY)");
mysqli_query($link, "alter table $tb add column value VARCHAR(50)");
mysqli_query($link, "alter table $tb add column comment VARCHAR(255)");


echo '
<form action="" method="get">
 <input type="hidden" name="ns" value="'.$_GET['ns'].'"/>
 <input type="hidden" name="cl" value="'.$_GET['cl'].'"/>
 Параметр: <input type="text" name="parameter" value="'.$_GET['parameter'].'"/>
 <input type="submit" value="Задать"/>
</form>';


$parameter=$_GET['parameter'];

// Добавляем
mysqli_query($link, "insert into $tb (parameter, value ) values ( '$parameter', '$cl' )");
//}




//mysqli_query($link, "create table $tb");
//mysqli_query($link, "alter table $tb add column val sting");


// Добавляем
//if ( $_GET['add'] == 'add' ) {
//mysqli_query($link, "CREATE DATABASE $my_db");
//mysqli_query($link, "create table $tb (cm double PRIMARY KEY)");
//mysqli_query($link, "alter table $tb add column lev double");
//mysqli_query($link, "insert into $tb (cm, lev) values ( $cm, $lev )");
//}

// Удаляем
//if ( $_GET['del'] == 'del' ) {
//mysqli_query($link, "delete from $tb where cm=$cm");
//}

// Редактируем
//if ( $_GET['edit'] == 'edit' ) {
//mysqli_query($link, "update $tb set lev=$lev where cm=$cm");
//}





}

else
{
echo "Не выбрана система";
}


?>

