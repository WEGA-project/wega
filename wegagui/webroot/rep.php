<?php
include_once "menu.php";

$ns=$_GET['ns'];
include_once "func.php";
//$namesys=dbval("namesys",$ns);


if ($ns){

if (empty($_GET['days'])){$_GET['days']="-0 days";}
if (empty($_GET['wsdt'])){$_GET['wsdt']=date("Y-m-d",strtotime($_GET['days']))." 00:00:00";}
if (empty($_GET['wpdt'])){$_GET['wpdt']=date("Y-m-d")." 23:59:59";}
if (empty($_GET['limit'])){$_GET['limit']="100000";}

include_once "../config/".$ns.".conf.php";
include_once "sqvar.php";
//$comment=dbcomment("namesys",$ns);
//$LevelFull=dbval("LevelFull",$ns);
// $LevelAdd=dbval("LevelAdd",$ns);
// $La=dbval("La",$ns);
// $ECPlan=dbval("ECPlan",$ns);
// $sEC=dbval("sEC",$ns);
// $rEC=dbval("rEC",$ns);
//$Slk=sEC/rEC;
// $konc=dbval("konc",$ns);



//include "func.php";
//dbval("namesys",$ns);

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
echo "<br>";





include_once "helper.php";
echo "<br>";
echo "<br>";

include_once "datetime.php";


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
set terminal png size 1200,2400
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
//set multiplot layout 7, 1
set multiplot layout 6,1

set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]


############## plot2 temp ######################


set title "Освещенность"
set ylabel "Киллолюксы"

plot    \
	"'.$csv.'" using 1:17 w l title "Датчик освещенности", \

unset ylabel
unset title

set title "Влажность"
set ylabel "%"

plot    \
	"'.$csv.'" using 1:3 w l title "Датчик влажности", \

unset ylabel
unset title




set ylabel "градусы"
set title "Температура"
plot    \
	"'.$csv.'" using 1:4 w l title "Корни", \
	"'.$csv.'" using 1:10 w l title "Бак", \
	"'.$csv.'" using 1:2 w l title "Воздух", \


unset ylabel
unset title


set title "Электропроводность"
set ylabel "mS/cm"

plot    \
	"'.$csv.'" using 1:14 w l title "EC", \
	"'.$csv.'" using 1:15 w l title "ECt", \

unset ylabel
unset title


set title "Уровень в питательном баке"
set ylabel "литры"


plot    \
	"'.$csv.'" using 1:16 w l title "Объем в баке", \

unset ylabel
unset title



set title "Колличество растворенных солей"
set ylabel "граммы"

plot    \
	"'.$csv.'" using 1:18 w l title "Остаток солей", \

unset ylabel
unset title


set title "Кислотно-щелочной баланс"


plot    \
	"'.$csv.'" using 1:19 w l title "pH", \

unset ylabel



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

