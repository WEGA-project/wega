<?php
include "menu.php";

include "../config/".$ns.".conf.php";

echo "<h1>".$namesys."</h1>";
echo $comment;
echo "<br>";

echo "<h2>Водородный потенциал pH</h2>";


include "func.php";

if (dbval("pHraw",$ns) != "null") {

$pHraw=dbval("pHraw",$ns);
$RootTemp=dbval("RootTemp",$ns);



//if (dbval("A2",$ns)=='') {setdbval($ns,"A2","An","Имя поля в базе содержащее raw значение ЕС при отрицательной фазе ");}
echo "Калибровка по двум точкам<br>";
pedit("pH_val_p1",$ns,4.01,"Фактическое значение pH точки 1");
$pH_val_p2=floatval(dbval("pH_val_p2",$ns));


pedit("pH_raw_p1",$ns,21897,"Значение АЦП RAW для pH точки 1");
$pH_raw_p2=floatval(dbval("pH_raw_p2",$ns));


pedit("pH_val_p2",$ns,6.86,"Фактическое значение pH точки 2");
$pH_val_p1=floatval(dbval("pH_val_p1",$ns));

pedit("pH_raw_p2",$ns,19360,"Значение АЦП RAW для pH точки 2");
$pH_raw_p1=floatval(dbval("pH_raw_p1",$ns));




// Процедурв интерполяции
$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");
$strSQL ="
CREATE DEFINER=`root`@`localhost` FUNCTION `line2point`(
x1 FLOAT,
y1 FLOAT,
x2 FLOAT,
y2 FLOAT,
x  FLOAT) RETURNS float
BEGIN

set @a:=(-x1*y2+x2*y1)/(x2-x1);
set @k:=(y2-y1)/(x2-x1);
set @y:=@a + @k *  x;
RETURN @y;
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
@pHraw:=".$pHraw.",
@pH:=line2point($pH_raw_p1,$pH_val_p1,$pH_raw_p2,$pH_val_p2,@pHraw),
@atemp:=".dbval("airtemp",$ns).",
@pHt:=@pH/(1+0.002*(@atemp-25))



from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
 and  ".dbval("roottemp",$ns)." <80
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
	"'.$csv.'" using 1:2 w l title "'.dbval("pHraw",$ns).'", \

plot    \
	"'.$csv.'" using 1:3 w l title "pH", \

plot    \
	"'.$csv.'" using 1:4 w l title "temp", \

plot    \
	"'.$csv.'" using 1:5 w l title "pHt", \
	"'.$csv.'" using 1:3 w l title "pH", \




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

