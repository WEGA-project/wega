<?php
include "menu.php";

include "../config/".$ns.".conf.php";

echo "<h1>".$namesys."</h1>";
echo $comment;
echo "<br>";

echo "<h2>Калибровка терморезистора</h2>";


include "func.php";

if (dbval("tRraw",$ns) != "null") {

$pHraw=dbval("tRraw",$ns);
$RootTemp=dbval("RootTemp",$ns);


echo "<h4>Калибровка по трём точкам<br></h4>";
echo "<br>Точка 1<br>";
pedit("tR_val_p1",$ns,36,"tR Темература точки 1");
pedit("tR_raw_p1",$ns,2300,"tR Значение АЦП RAW точки 1");

echo "<br>Точка 2<br>";
pedit("tR_val_p2",$ns,23,"tR Темература точки 2");
pedit("tR_raw_p2",$ns,1677,"tR Значение АЦП RAW точки 2");

echo "<br>Точка 3<br>";
pedit("tR_val_p3",$ns,6,"tR Темература точки 3");
pedit("tR_raw_p3",$ns,920,"tR Значение АЦП RAW точки 3");

	$tR_val_p1=floatval(dbval("tR_val_p1",$ns));
	$tR_val_p2=floatval(dbval("tR_val_p2",$ns));
	$tR_val_p3=floatval(dbval("tR_val_p3",$ns));
	$tR_raw_p1=floatval(dbval("tR_raw_p1",$ns));
	$tR_raw_p2=floatval(dbval("tR_raw_p2",$ns));
	$tR_raw_p3=floatval(dbval("tR_raw_p3",$ns));




// Процедурв интерполяции
$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");
$strSQL ="
CREATE DEFINER=`root`@`localhost` FUNCTION `int3point`(
px1 FLOAT,
py1 FLOAT,
px2 FLOAT,
py2 FLOAT,
px3 FLOAT,
py3 FLOAT,


x  FLOAT) RETURNS float
BEGIN
set @pa:=-(-px1*py3 + px1*py2 - px3*py2 + py3*px2 + py1*px3 - py1*px2) /  (-pow(px1,2)*px3 + pow(px1,2)*px2 - px1*pow(px2,2) + px1*pow(px3,2) - pow(px3,2)*px2 + px3*pow(px2,2) ); 
set @pb:=( py3*pow(px2,2) - pow(px2,2)*py1 + pow(px3,2)*py1 + py2*pow(px1,2) - py3*pow(px1,2) - py2 * pow(px3,2) ) /  ( (-px3+px2) * (px2*px3 - px2*px1 + pow(px1,2) - px3*px1 ) );
set @pc:=( py3*pow(px1,2)*px2 - py2*pow(px1,2)*px3 - pow(px2,2)*px1*py3 + pow(px3,2)*px1*py2 + pow(px2,2)*py1*px3 - pow(px3,2)*py1*px2 ) /  ( (-px3+px2) * (px2*px3 - px2*px1 + pow(px1,2) - px3*px1 ) );

RETURN @pa*pow(x,2) + @pb*x + @pc;
END
";
$rs=mysqli_query($link, $strSQL);



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
@ECtempRAW:=".dbval('ECtempRAW',$ns).",
int3point(".$tR_raw_p1.",".$tR_val_p1.",".$tR_raw_p2.",".$tR_val_p2.",".$tR_raw_p3.",".$tR_val_p3.",@ECtempRAW),
".dbval('RootTemp',$ns)."



from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
 and ".dbval("RootTemp",$ns)." < 80
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
	"'.$csv.'" using 1:2 w l title "'.dbval("ECtempRAW",$ns).'", \

plot    \
	"'.$csv.'" using 1:3 w l title "ECtemp", \

plot    \
	"'.$csv.'" using 1:4 w l title "'.dbval("RootTemp",$ns).'", \

plot    \
	"'.$csv.'" using 1:3 w l title "ECtemp", \
	"'.$csv.'" using 1:4 w l title "'.dbval("RootTemp",$ns).'", \

';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';

}
else
{
echo "Датчик pH не задан. Если он есть сопоставьте соответсвующее поле в базе";
}


?>

