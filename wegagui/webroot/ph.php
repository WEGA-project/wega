<?php
include "menu.php";


$ns=$_GET['ns'];
include_once "func.php";
include "sqvar.php";


echo "<h1>".$namesys."</h1>";
echo $comment;
echo "<br>";

echo "<h2>Водородный потенциал pH</h2>";




if (dbval("pHraw",$ns) != "null") {

$pHraw=dbval("pHraw",$ns);
$RootTemp=dbval("RootTemp",$ns);

echo "<h2>Калибровка pH</h2>";
echo "Дата и время последнего замера: ".sensval("dt",$ns);

echo "<br><br>";

pedit("pH_date1",$ns,"2022-05-20 11:00:00","Дата/время контрольной точки 1");
$dateval=dbval("pH_date1",$ns);
echo "pH в точке 1 = ".valdate($p_pH,$dateval,$ns) -> value;
echo "<br>Прошло: ".showDate( strtotime($dateval) );
echo "<br><br>";

pedit("pH_date2",$ns,"2022-05-20 12:00:00","Дата/время контрольной точки 2");
$dateval=dbval("pH_date2",$ns);
echo "pH в точке 2 = ".valdate($p_pH,$dateval,$ns) -> value;
echo "<br>Прошло: ".showDate( strtotime($dateval) );
echo "<br><br>";

pedit("pH_date3",$ns,"2022-05-20 13:00:00","Дата/время контрольной точки 3");
$dateval=dbval("pH_date3",$ns);
echo "pH в точке 3 = ".valdate($p_pH,$dateval,$ns) -> value;
echo "<br>Прошло: ".showDate( strtotime($dateval) );
echo "<br><br>";


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

$pa=-(-$pH_raw_p1*$pH_val_p3 + $pH_raw_p1*$pH_val_p2 - $pH_raw_p3*$pH_val_p2 + $pH_val_p3*$pH_raw_p2 + $pH_val_p1*$pH_raw_p3 - $pH_val_p1*$pH_raw_p2) /  (-pow($pH_raw_p1,2)*$pH_raw_p3 + pow($pH_raw_p1,2)*$pH_raw_p2 - $pH_raw_p1*pow($pH_raw_p2,2) + $pH_raw_p1*pow($pH_raw_p3,2) - pow($pH_raw_p3,2)*$pH_raw_p2 + $pH_raw_p3*pow($pH_raw_p2,2) ); 
$pb=( $pH_val_p3*pow($pH_raw_p2,2) - pow($pH_raw_p2,2)*$pH_val_p1 + pow($pH_raw_p3,2)*$pH_val_p1 + $pH_val_p2*pow($pH_raw_p1,2) - $pH_val_p3*pow($pH_raw_p1,2) - $pH_val_p2 * pow($pH_raw_p3,2) ) /  ( (-$pH_raw_p3+$pH_raw_p2) * ($pH_raw_p2*$pH_raw_p3 - $pH_raw_p2*$pH_raw_p1 + pow($pH_raw_p1,2) - $pH_raw_p3*$pH_raw_p1 ) );
$pc=( $pH_val_p3*pow($pH_raw_p1,2)*$pH_raw_p2 - $pH_val_p2*pow($pH_raw_p1,2)*$pH_raw_p3 - pow($pH_raw_p2,2)*$pH_raw_p1*$pH_val_p3 + pow($pH_raw_p3,2)*$pH_raw_p1*$pH_val_p2 + pow($pH_raw_p2,2)*$pH_val_p1*$pH_raw_p3 - pow($pH_raw_p3,2)*$pH_val_p1*$pH_raw_p2 ) /  ( (-$pH_raw_p3+$pH_raw_p2) * ($pH_raw_p2*$pH_raw_p3 - $pH_raw_p2*$pH_raw_p1 + pow($pH_raw_p1,2) - $pH_raw_p3*$pH_raw_p1 ) );

echo "<br>";
pedit("pH_lkorr",$ns,0,"Линейная коррекция pH");
$pH_lkorr=floatval(dbval("pH_lkorr",$ns));


echo "<br>Функция калибровки<br>";
$phfuncint = round($pa,10).' * X² + '.round($pb,10).' * X + '.round($pc,3);
//echo 'f(X) = '.round($pa,10).' * X² + '.round($pb,10).' * X + '.round($pc,3);
echo 'f(X) = '.$phfuncint;

echo "<br>";
echo "<br><b>Текущие значения</b>";
$phraw=sensval(dbval("pHraw",$ns),$ns);
echo "<br>pH(mV)=".round($phraw,3)." <br>";

$ph=sensval("ph(".dbval("pHraw",$ns).")",$ns);
echo "pH=".round($ph,3)." <br><br>";


// График калибровочной кривой
$text='
set title "График калибровочной кривой pH"
set terminal png size 800,600
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set grid
set y2label

set xrange ['.$pH_raw_p1*1.4.':'.$pH_raw_p3*1.4.']

unset format
set label "   pH '.$pH_val_p1.'" at '.$pH_raw_p1.','.$pH_val_p1.'+'.$pH_lkorr.' point pointtype 7
set label "   pH '.$pH_val_p2.'" at '.$pH_raw_p2.','.$pH_val_p2.'+'.$pH_lkorr.' point pointtype 7
set label "   pH '.$pH_val_p3.'" at '.$pH_raw_p3.','.$pH_val_p3.'+'.$pH_lkorr.' point pointtype 7
set label "pH '.round($ph,4).'   " right at '.$phraw.','.$ph.' point pointtype 4

f(x)= '.$pa.'*x**2 + '.$pb.'*x + '.$pc.'+'.$pH_lkorr.'
plot f(x) w l title "'.$phfuncint.'"
';

$filename=$gnups;
$handler = fopen($filename, "w");
fwrite($handler, $text);
fclose($handler);
shell_exec('cat '.$gnups.'|gnuplot');
echo '<img src="'.$img.'">';


include "sqfunc.php";
include "datetime.php";


// График pH

if ($p_pHraw != 'null') {
        $pref="ph";
        $xsize=1000;
        $ysize=400;
        
    
        $gimg=$gimg.$pref;
        $img=$img.$pref;
        
        $strSQL ="select 
        dt,
        if (".$p_pH." < 10 and ".$p_pH." > 1, ".$p_pH.", null)
        
        from sens 
        where dt  >  '".$wsdt."'
         and  dt  <  '".$wpdt."'
    
        order by dt";
        include "sqltocsv.php";
        
        $name="pH (Кислотно-щелочной баланс)";
        $dimens="";
        $nplot1="";
    
        
        gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
        }

// Графики температур
if ($p_AirTemp != 'null' or $p_RootTemp != 'null' or $p_ECtemp !='null') {
        $pref="temper";
        $xsize=1000;
        $ysize=400;
    
    
    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
    ".$p_AirTemp.",
    ".$p_RootTemp.",
    ".$p_ECtemp."
    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="Температура";
    $dimens="°C";
    $nplot1="Воздух";
    $nplot2="Зона корней";
    $nplot3="Бак";
    
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
    }


}
else
{
echo "Датчик pH не задан. Если он есть сопоставьте соответсвующее поле в базе";
}


?>

