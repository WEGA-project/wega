<?php
include "menu.php";


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
 <p><input type="hidden" name="ns" value="'.$_GET['ns'].'"/> </p>
 <p>Дата с: <input type="text" name="wsdt" value="'.$_GET['wsdt'].'"/> </p>
 <p>Дата по: <input type="text" name="wpdt" value="'.$_GET['wpdt'].'"/> </p>
 <p>Число измерений не более: <input type="text" name="limit" value="'.$_GET['limit'].'"/></p>

 <p><input type="submit" value="Найти"/></p>
</form>';



// Подключаемся к базе

include "sql.php";




$AirTemp=$row[1];
$Humidity=$row[2];
$WaterTemp=$row[3];
$WaterTempEC=round($row[9],3);
$WaterTempECraw=$row[4];
$EC=$row[14];
$Level=$row[15];
$LightRaw=round($row[5],0);
$Lux=round($row[16],0);
$L1=$Level+$LevelAdd;
$L2=$LevelFull-$Level-$La;
$ECn=(-($EC*$L1 - $ECPlan*$L1 - $ECPlan*$L2 )/$L2);
$Soiln=$ECn*$Slk*($L2);
$levsm=$row[6];
$lasttime=date("U") - date("U",strtotime($row[0]) );


echo ("Дата: ".$row[0]." обновлено: ".$lasttime." сек. назад");
echo "<br>";
echo ("<br>Температура воздуха: ".$AirTemp."°C");
echo ("<br>Температура раствора (корни): ".$WaterTemp."°C");
echo ("<br>Температура раствора (бак): ".$WaterTempEC."°C (raw=".$WaterTempECraw.")");
echo ("<br>Влажность воздуха: ".$Humidity."%");
echo ("<br>Освещенность: ".$Lux." lux (raw: ".$LightRaw.")<br>");
echo ("<br>Текущий ЕС: ".round($EC,3)." мСм/см");
echo ("<br>Остаток в баке: <b>".round($Level,1)." л.</b> (".round($levsm,2)." см) ".round(100-($LevelFull-$Level)/$LevelFull*100,0)."%");
echo ("<br>Дополнительно в системе: ".round($LevelAdd,1)." л. Общий остаток раствора: ".round($L1,1)." л");
echo ("<br>Предельный объем бака: ".round($LevelFull,1)." л. Защита от аварийного перелива: ".round($La,1));
echo ("<br>Для получения ЕС=".$ECPlan." мСм/см нужно долить: <b>". round($L2,1)."л.</b> до уровня ".($LevelFull-$La).", c ЕС=".round( $ECn   ,2)." мСм/см" );
echo ("<br>Это: <b>".round($Soiln,2)." грамм</b> солей или по ".round( $Soiln/2/$konc*1000,0)." мл концентратов ".$konc.":1 с каждого");



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
set terminal png size 1900,6080
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m %H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 10, 1
set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]


############## plot2 temp ######################


set ylabel "градусы"
set title "Температура"
plot    \
	"'.$csv.'" using 1:4 w l title "Корни", \
	"'.$csv.'" using 1:10 w l title "Бак", \
	"'.$csv.'" using 1:2 w l title "Воздух", \
	"/var/log/sensors/owm.log" using 1:2 w l title "Улица", \


unset ylabel
unset title

set ylabel "%"
set yrange[0:100]

plot    \
	"/var/log/sensors/owm.log" using 1:($5) w l  title "Облачность", \
	"'.$csv.'" using 1:3 w l title "Влажность", \

unset yrange
unset ylabel


set title "Освещенность"
set ylabel "Люксы"

plot    \
	"'.$csv.'" using 1:17 w l title "Lux", \

unset ylabel
unset title



set ylabel "mS/cm"

plot    \
	"'.$csv.'" using 1:14 w l title "EC", \
	"'.$csv.'" using 1:15 w l title "ECt", \

unset ylabel

plot    \
	"'.$csv.'" using 1:16 w l title "Объем в баке", \

plot    \
	"'.$csv.'" using 1:18 w l title "Остаток солей", \
	"'.$csv.'" using 1:19 w l title "k", \




plot    \
	"'.$csv.'" using 1:5 w l title "aTemp", \

plot    \
	"'.$csv.'" using 1:11 w l title "R2p", \
	"'.$csv.'" using 1:12 w l title "R2n", \
	"'.$csv.'" using 1:13 w l title "R2 среднее", \




plot    \
	"'.$csv.'" using 1:8 w l title "An", \

plot    \
	"'.$csv.'" using 1:9 w l title "Ap", \

plot    \
	"'.$csv.'" using 1:19 w l title "pH", \



';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';





?>

