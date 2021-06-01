<?php
include "menu.php";


$ns=$_GET['ns'];
include_once "func.php";
include "sqvar.php";

//include "../config/".$ns.".conf.php";


echo "<h1>".$namesys."</h1>";
echo $comment;
echo "<br>";

echo "<h2>Водородный потенциал pH</h2>";




if (dbval("pHraw",$ns) != "null") {

$pHraw=dbval("pHraw",$ns);
$RootTemp=dbval("RootTemp",$ns);



//if (dbval("A2",$ns)=='') {setdbval($ns,"A2","An","Имя поля в базе содержащее raw значение ЕС при отрицательной фазе ");}
echo "<h3>Калибровка по трем точкам</h3>";

echo "<br>Точка 1<br>";
pedit("pH_val_p1",$ns,4.01,"Фактическое значение pH точки 1");
$pH_val_p1=floatval(dbval("pH_val_p1",$ns));

pedit("pH_raw_p1",$ns,14192,"Значение АЦП RAW для pH точки 1");
$pH_raw_p1=floatval(dbval("pH_raw_p1",$ns));

echo "<br>Точка 2<br>";
pedit("pH_val_p2",$ns,6.86,"Фактическое значение pH точки 2");
$pH_val_p2=floatval(dbval("pH_val_p2",$ns));

pedit("pH_raw_p2",$ns,13344,"Значение АЦП RAW для pH точки 2");
$pH_raw_p2=floatval(dbval("pH_raw_p2",$ns));

echo "<br>Точка 3<br>";
pedit("pH_val_p3",$ns,9.18,"Фактическое значение pH точки 3");
$pH_val_p3=floatval(dbval("pH_val_p3",$ns));

pedit("pH_raw_p3",$ns,12720,"Значение АЦП RAW для pH точки 3");
$pH_raw_p3=floatval(dbval("pH_raw_p3",$ns));



//set @pa:=-(-@px1*@py3 + @px1*@py2 - @px3*@py2 + @py3*@px2 + @py1*@px3 - @py1*@px2) /  (-pow(@px1,2)*@px3 + pow(@px1,2)*@px2 - @px1*pow(@px2,2) + @px1*pow(@px3,2) - pow(@px3,2)*@px2 + @px3*pow(@px2,2) ); 
//set @pb:=( @py3*pow(@px2,2) - pow(@px2,2)*@py1 + pow(@px3,2)*@py1 + @py2*pow(@px1,2) - @py3*pow(@px1,2) - @py2 * pow(@px3,2) ) /  ( (-@px3+@px2) * (@px2*@px3 - @px2*@px1 + pow(@px1,2) - @px3*@px1 ) );
//set @pc:=( @py3*pow(@px1,2)*@px2 - @py2*pow(@px1,2)*@px3 - pow(@px2,2)*@px1*@py3 + pow(@px3,2)*@px1*@py2 + pow(@px2,2)*@py1*@px3 - pow(@px3,2)*@py1*@px2 ) /  ( (-@px3+@px2) * (@px2*@px3 - @px2*@px1 + pow(@px1,2) - @px3*@px1 ) );


$pa=-(-$pH_raw_p1*$pH_val_p3 + $pH_raw_p1*$pH_val_p2 - $pH_raw_p3*$pH_val_p2 + $pH_val_p3*$pH_raw_p2 + $pH_val_p1*$pH_raw_p3 - $pH_val_p1*$pH_raw_p2) /  (-pow($pH_raw_p1,2)*$pH_raw_p3 + pow($pH_raw_p1,2)*$pH_raw_p2 - $pH_raw_p1*pow($pH_raw_p2,2) + $pH_raw_p1*pow($pH_raw_p3,2) - pow($pH_raw_p3,2)*$pH_raw_p2 + $pH_raw_p3*pow($pH_raw_p2,2) ); 
$pb=( $pH_val_p3*pow($pH_raw_p2,2) - pow($pH_raw_p2,2)*$pH_val_p1 + pow($pH_raw_p3,2)*$pH_val_p1 + $pH_val_p2*pow($pH_raw_p1,2) - $pH_val_p3*pow($pH_raw_p1,2) - $pH_val_p2 * pow($pH_raw_p3,2) ) /  ( (-$pH_raw_p3+$pH_raw_p2) * ($pH_raw_p2*$pH_raw_p3 - $pH_raw_p2*$pH_raw_p1 + pow($pH_raw_p1,2) - $pH_raw_p3*$pH_raw_p1 ) );
$pc=( $pH_val_p3*pow($pH_raw_p1,2)*$pH_raw_p2 - $pH_val_p2*pow($pH_raw_p1,2)*$pH_raw_p3 - pow($pH_raw_p2,2)*$pH_raw_p1*$pH_val_p3 + pow($pH_raw_p3,2)*$pH_raw_p1*$pH_val_p2 + pow($pH_raw_p2,2)*$pH_val_p1*$pH_raw_p3 - pow($pH_raw_p3,2)*$pH_val_p1*$pH_raw_p2 ) /  ( (-$pH_raw_p3+$pH_raw_p2) * ($pH_raw_p2*$pH_raw_p3 - $pH_raw_p2*$pH_raw_p1 + pow($pH_raw_p1,2) - $pH_raw_p3*$pH_raw_p1 ) );

echo "<br>Функция калибровки<br>";
echo 'f(X) = '.round($pa,10).' * X² + '.round($pb,10).' * X + '.round($pc,3);
echo "<br>";
echo "<br><b>Текущие значения</b>";
$phraw=sensval(dbval("pHraw",$ns),$ns);
echo "<br>pH(RAW)=".round($phraw,3)." <br>";

$ph=sensval("ph(".dbval("pHraw",$ns).")",$ns);
echo "pH=".round($ph,3)." <br><br>";

//f(x)= '.$pa.'*x**2 + '.$pb.'*x + '.$pc.'

include "sqfunc.php";
include "datetime.php";


// Подключаемся к базе
$link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");

if (!$link) {
    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}


//@pH:=line2point($pH_raw_p1,$pH_val_p1,$pH_raw_p2,$pH_val_p2,@pHraw)
$t0_ph=25;
$K_ph=273.15;
$B_ph=3950;
$R1_ph=100000;
$DC_ph=32768;
$vk=0.45;
//@pHraw:=(".$p_pHraw."+".$p_VddRaw."-13976)/(1+0.9*(@Vdd-2.62)),
//".$p_pHraw."-(".$p_VddRaw."-1000)+12970

$strSQL ="select 

dt,												# 1
@pHraw:=".$p_pHraw.",
@pH:=ph(".$p_pHraw.")


from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt limit $limit";


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
set terminal png size 1000,1500
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 5,1
set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]


plot    \
"'.$csv.'" using 1:2 w l title "pHraw", \

plot    \
	"'.$csv.'" using 1:3 w l title "pH", \

plot    \
	"'.$csv.'" using 1:6 w l title "IntTemp", \
        "'.$csv.'" using 1:7 w l title "18b20", \

set xrange ['.$pH_raw_p1.'+1000:'.$pH_raw_p3.'-1000]

unset format
set label "pH '.$pH_val_p1.'" at '.$pH_raw_p1.','.$pH_val_p1.' point pointtype 7
set label "pH '.$pH_val_p2.'" at '.$pH_raw_p2.','.$pH_val_p2.' point pointtype 7
set label "pH '.$pH_val_p3.'" at '.$pH_raw_p3.','.$pH_val_p3.' point pointtype 7

f(x)= '.$pa.'*x**2 + '.$pb.'*x + '.$pc.'
plot f(x)
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

