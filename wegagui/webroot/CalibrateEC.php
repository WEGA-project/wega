<?php
include "menu.php";
//include "../config/".$ns.".conf.php";

$start = microtime(true);

if ($ns){
include "sqvar.php";


echo "<h1>".$namesys."</h1>";
echo $comment;
echo "<br>";



include_once "func.php";
if (dbval("A1",$ns) != "null" and dbval("A2",$ns) != "null") {
// Получение констант калибровки из базы
    $ec1=floatval(dbval("EC_val_p1",$ns));
    $ec2=floatval(dbval("EC_val_p2",$ns));
    $eckorr=floatval(dbval("EC_val_korr",$ns));
    $ex1=floatval(dbval("EC_R2_p1",$ns));
    $ex2=floatval(dbval("EC_R2_p2",$ns));
    $k=floatval(dbval("EC_kT",$ns));
    $tR_val_p1=floatval(dbval("tR_val_p1",$ns));
    $tR_val_p2=floatval(dbval("tR_val_p2",$ns));
    $tR_val_p3=floatval(dbval("tR_val_p3",$ns));
    $tR_raw_p1=floatval(dbval("tR_raw_p1",$ns));
    $tR_raw_p2=floatval(dbval("tR_raw_p2",$ns));
    $tR_raw_p3=floatval(dbval("tR_raw_p3",$ns));


	// Функция нелинейной апроксимации по трем точкам одна из которых нулевая
    $eb=(-log($ec1/$ec2))/(log($ex2/$ex1));
    $ea=pow($ex1,(-$eb))*$ec1;

echo "<h2>Калибровка EC</h2>";
echo "Дата и время последнего замера: ".sensval("dt",$ns);


include "sqfunc.php";
include "datetime.php";


$P_A1=dbval("A1",$ns);
$A1=sensval($P_A1,$ns);

$P_A2=dbval("A2",$ns);
$A2=sensval($P_A2,$ns);


echo "<br>";

// График АЦП
if ($P_A1 != 'null' and $P_A2 != 'null') {
    $pref="ecraw";    
    $xsize=1000;
    $ysize=400;
    

    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select
    dt,
    ".$P_A1.",
    ".$P_A2."

    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="АЦП электродов измерения электропроводности";
    $dimens="RAW";
    $nplot1="A1.RAW(-)";
	$nplot2="A2.RAW(+)";
    
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);

    echo "<br>Текущие значения АЦП при положительной и отрицательной фазе:";
    echo "<br>";
    echo "A1.RAW(-)=".$A1;
    echo "<br>";
    echo "A2.RAW(+)=".$A2;

}
    
    echo "<br>";
    echo "<br><h3>Параметры цепи измерения</h3>";

    pedit("EC_R1",$ns,500,"EC Резистор делителя R1 в омах");
    pedit("EC_Rx1",$ns,-110,"EC Внутреннее сопротивление порта 1");
    pedit("EC_Rx2",$ns,-10,"EC Внутреннее сопротивление порта 2");
    pedit("Dr",$ns,4095,"Разрядность АЦП");
// График сопротивлений
if ($P_A1 != 'null' and $P_A2 != 'null') {
    $pref="ecR";    
    $xsize=1000;
    $ysize=400;
    

    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
	".$P_R2n.",
	".$P_R2p.",
	".$P_R2."

    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
	 and ".$P_R2." < 10000 
    order by dt";
    include "sqltocsv.php";
    
    $name="Расчетное сопротивление R2";
    $dimens="Ω";
	$nplot1="R2(-)";
    $nplot2="R2(+)";

    
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);
	echo "<br>Расчетное значение сопротивлений электрода<br>";
	echo "R2(+)=".$R2p."Ω";
	echo "<br>";
	echo "R2(-)=".$R2n."Ω";
	echo "<br><br>Значение сопротивления с коррекцией поляризации<br>";
	echo "R2=".$R2."Ω";

    }


// График поляризации
if ($P_A1 != 'null' and $P_A2 != 'null') {
    $pref="ec";    
    $xsize=1000;
    $ysize=400;
    

    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
	(".$P_R2p."-".$P_R2n.")/".$P_R2n."*100

    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'

    order by dt";
    include "sqltocsv.php";
    
    $name="Поляризация R2, погрешность в схождении измерений сопротивления среды в разных фазах полярности";
    $dimens="%";
    $nplot1="";
	$nplot2="";
    
    gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens);

    echo "<br><br>Текущее значение поляризации<br>";
    echo "R2_polarity=".$R2_polarity."Ω ".round(($R2p-$R2n)/$R2n*100,2)."%";
    
}

    echo "<br><br><h3>Калибровка ЕС по сопротивлению и температуре</h3>";
    pedit("EC_val_p1",$ns,1.114,"Фактическое значение EC точки 1");
    pedit("EC_R2_p1",$ns,678,"Значение R2 для точки 1");
    echo "<br>";
    
    pedit("EC_val_p2",$ns,4.988,"Фактическое значение EC точки 2");
    pedit("EC_R2_p2",$ns,177,"Значение R2 для точки 2");
    
    pedit("EC_val_korr",$ns,0,"Линейная коррекция");


    echo "<br><br>Расчетная удельная электропроводность<br>";
    $ec=sensval("EC($P_A1,$P_A2,25)",$ns);
     echo "EC=".round($ec,3)."mS/cm";
    
    echo "<br><br>Температура раствора<br>";
    $tempEC=sensval("ftR(".dbval("ECtempRAW",$ns).")",$ns);
     echo "tR=".round($tempEC,3)."°C";
    echo "<br>";
    pedit("EC_kT",$ns,0.02,"Значение коэфициента термокомпенсации ЕС");
 
    echo "<br><br>EC с учетом температурной компенсации<br>";
    $ec=sensval("EC($P_A1,$P_A2,".$tempEC.")",$ns);
     echo "ECt=".round($ec,3)."mS/cm";
    echo "<br>";



// График EC
if ($P_A1 != 'null' and $P_A2 != 'null') {
    $pref="ec";    
    $xsize=1000;
    $ysize=400;
    

    $gimg=$gimg.$pref;
    $img=$img.$pref;
    
    $strSQL ="select 
    dt,
    ".$p_EC.",
	EC(".$P_A1.",".$P_A2.",25)
    
    from sens 
    where dt  >  '".$wsdt."'
     and  dt  <  '".$wpdt."'
    order by dt";
    include "sqltocsv.php";
    
    $name="EC (Удельная электропроводность раствора)";
    $dimens="мСм/см";
    $nplot1="ЕС";
    $nplot2="ЕС без Термокомпенсации";
    
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


// // Калибровочный график
// if ($ea != 'null' and $eb != 'null') {

//     $gpfunc="x**".$eb."*".$ea;
//     //$gpfunc="1611.2184*x**-1.116";
//     $pref="eccalibr";
//     $xsize=1000;
//     $ysize=400;


// $gimg=$gimg.$pref;
// $img=$img.$pref;


// $text='
// set terminal png size '.$xsize.','.$ysize.'
// set title "График калибровочной кривой EC (mS*cm) по 1/R2 (mS)"
// set terminal png size 800,800
// set output "'.$gimg.'"
// set grid

// set ylabel "мСм/см"
// set xlabel "мСм (1/Ω*1000)"

// set xrange [0:10]
// set yrange [0:10]
// #set logscale x
// #set logscale y

// set label "   EC '.$ec1.'" at '.(1/$ex1*1000).','.$ec1.' point pointtype 7
// set label "   EC '.$ec2.'" at '.(1/$ex2*1000).','.$ec2.' point pointtype 7
// set label "   EC '.round($ec,3).'   " right at '.(1/$R2*1000).','.$ec.' point pointtype 4

// f(x)= '.$gpfunc.'
// plot f(1/x*1000) w l title "Кривая калибровки ЕС"
// ';

// fwrite($handler, $text);
// fclose($handler);
// $err=shell_exec('cat '.$gnups.'|gnuplot');
// echo "<br>";
// echo '<img src="'.$img.'" alt="альтернативный текст">';
// }


// Калибровочный график
if ($ea != 'null' and $eb != 'null') {

    $gpfunc="x**".$eb."*".$ea;
    //$gpfunc="1611.2184*x**-1.116";
    $pref="eccalibr";
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

$text='
set terminal png size '.$xsize.','.$ysize.'
set title "График калибровочной кривой EC"
set terminal png size 800,800
set output "'.$gimg.'"
set grid

set ylabel "мСм/см"
set xlabel "Ω"

set xrange [0:1500]
set yrange [0:8]
//set logscale x
//set logscale y

set label "   EC '.$ec1.'" at '.($ex1).','.$ec1.' point pointtype 7
set label "   EC '.$ec2.'" at '.($ex2).','.$ec2.' point pointtype 7
set label "   EC '.round($ec,3).'   " right at '.($R2).','.$ec.' point pointtype 4

f(x)= '.$gpfunc.'
plot f(x) w l title "Кривая калибровки ЕС"
';

fwrite($handler, $text);
fclose($handler);
$err=shell_exec('cat '.$gnups.'|gnuplot');
echo "<br>";
echo '<img src="'.$img.'" alt="альтернативный текст">';
}





}



else
{
echo "Датчик EC не задан. Если он есть сопоставьте соответсвующее поле в базе";
}


}
else
{
echo "Не выбрана система";
}

$time = microtime(true) - $start;
echo "<h0>".$time."</h0>";



?>

