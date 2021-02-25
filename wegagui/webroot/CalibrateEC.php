<?php
include "menu.php";

include "../config/".$ns.".conf.php";

echo "<h1>".$namesys."</h1>";
echo $comment;
echo "<br>";



include_once "func.php";
if (dbval("A1",$ns) != "null" and dbval("A2",$ns) != "null") {
echo "<h2>Калибровка EC</h2>";


echo "<h3>Параметры цепи измерения</h3>";

pedit("EC_R1",$ns,500,"EC Резистор делителя R1 в омах");
pedit("EC_Rx1",$ns,-120,"EC Внутреннее сопротивление порта 1");
pedit("EC_Rx2",$ns,0,"EC Внутреннее сопротивление порта 2");
pedit("Dr",$ns,4095,"Разрядность АЦП");

	$R1=floatval(dbval("EC_R1",$ns));
	$Rx1=floatval(dbval("EC_Rx1",$ns));
	$Rx2=floatval(dbval("EC_Rx2",$ns));
	$Dr=floatval(dbval("Dr",$ns));

echo "<h3>Калибровка ЕС по сопротивлению и температуре</h3>";
pedit("EC_val_p1",$ns,1.08,"Фактическое значение EC точки 1");
pedit("EC_R2_p1",$ns,538,"Значение R2 для точки 1");
echo "<br>";

pedit("EC_val_p2",$ns,4.89,"Фактическое значение EC точки 2");
pedit("EC_R2_p2",$ns,155,"Значение R2 для точки 2");

$ec1=floatval(dbval("EC_val_p1",$ns));
$ec2=floatval(dbval("EC_val_p2",$ns));

$ex1=floatval(dbval("EC_R2_p1",$ns));
$ex2=floatval(dbval("EC_R2_p2",$ns));

echo "<br>";
pedit("EC_kT",$ns,0.02,"Значение коэфициента термокомпенсации ЕС");
	$k=floatval(dbval("EC_kT",$ns));

// Функция нелинейной апроксимации по трем точкам одна из которых нулевая
$eb=(-log($ec1/$ec2))/(log($ex2/$ex1));
$ea=pow($ex1,(-$eb))*$ec1;



echo "<br>";
echo "<br>";
echo "<h3>Текущие контрольные показания</h3>";
echo "Дата и время замера: ".sensval("dt",$ns);
echo "<br>";
$P_A1=dbval("A1",$ns);
$A1=sensval($P_A1,$ns);

$P_A2=dbval("A2",$ns);
$A2=sensval($P_A2,$ns);
echo "<br>Значения замеров АЦП при положительной и отрицательной фазе:";
echo "<br>";
echo "A1.RAW(-)=".$A1;
echo "<br>";
echo "A2.RAW(+)=".$A2;

echo "<br>";

echo "<br>Расчетное значение сопротивлений электрода<br>";
$R2p=round( sensval("(-(-($P_A1)*$R1-$P_A1*$Rx2+$Rx2*$Dr)/(-$P_A1+$Dr))",$ns), 1);
echo "R2(+)=".$R2p."Ω";
echo "<br>";

$R2n=round( sensval("(((-$P_A2*$R1-$P_A2*$Rx1+$R1*$Dr+$Rx1*$Dr)/$P_A2))",$ns), 1);
echo "R2(-)=".$R2n."Ω";

echo "<br><br>Значение сопротивления с коррекцией поляризации<br>";
$R2=($R2p+$R2n)/2;
echo "R2=".$R2."Ω";


        $tR_val_p1=floatval(dbval("tR_val_p1",$ns));
        $tR_val_p2=floatval(dbval("tR_val_p2",$ns));
        $tR_val_p3=floatval(dbval("tR_val_p3",$ns));
        $tR_raw_p1=floatval(dbval("tR_raw_p1",$ns));
        $tR_raw_p2=floatval(dbval("tR_raw_p2",$ns));
        $tR_raw_p3=floatval(dbval("tR_raw_p3",$ns));

echo "<br><br>Расчетная удельная электропроводность<br>";
$ec=sensval("EC($P_A1,$P_A2,25)",$ns);
 echo "EC=".round($ec,3)."mS/cm";

echo "<br><br>Температура раствора<br>";
$tempEC=sensval("ftR(".dbval("ECtempRAW",$ns).")",$ns);
 echo "tR=".round($tempEC,3)."°C";

echo "<br><br>EC с учетом температурной компенсации<br>";
$ec=sensval("EC($P_A1,$P_A2,".$tempEC.")",$ns);
 echo "ECt=".round($ec,3)."mS/cm";
echo "<br>";
echo "<br>";
include "sqfunc.php";


include "datetime.php";

$strSQL ="select 

dt,
@A1:=".dbval('A1',$ns).",
@A2:=".dbval('A2',$ns).",
@ECtempRAW:=".dbval('ECtempRAW',$ns).",
@R2p:=(((-@A2*".$R1."-@A2*".$Rx1."+".$R1."*".$Dr."+".$Rx1."*".$Dr.")/@A2)),
@R2n:=(-(-(@A1)*".$R1."-(@A1)*".$Rx2."+".$Rx2."*".$Dr.")/(-(@A1)+".$Dr.")),
@R2:=(@R2p+@R2n)/2,
@EC:=if (@R2>0,".$ea."*pow(@R2,".$eb."),null),
@tR:=int3point(".$tR_raw_p1.",".$tR_val_p1.",".$tR_raw_p2.",".$tR_val_p2.",".$tR_raw_p3.",".$tR_val_p3.",@ECtempRAW),
@ECt:=@EC/(1+".$k."*(@tR-25))



from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt limit $limit";

include "sqltocsv.php";



$text='
set terminal png size 1000,3500
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 10,1
set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]



plot    \
	"'.$csv.'" using 1:2 w l title "RAW(-)", \


plot    \
	"'.$csv.'" using 1:3 w l title "RAW(+)", \

plot    \
	"'.$csv.'" using 1:5 w l title "R2(-)", \


plot    \
	"'.$csv.'" using 1:6 w l title "R2(+)", \

plot    \
	"'.$csv.'" using 1:5 w l title "R2(+)", \
	"'.$csv.'" using 1:6 w l title "R2(-)", \
	"'.$csv.'" using 1:7 w l title "R2", \

plot    \
	"'.$csv.'" using 1:7 w l title "R2", \

plot    \
	"'.$csv.'" using 1:8 w l title "EC", \

plot    \
	"'.$csv.'" using 1:9 w l title "tR", \

plot    \
	"'.$csv.'" using 1:8 w l title "EC", \
	"'.$csv.'" using 1:10 w l title "ECt", \

plot    \
	"'.$csv.'" using 1:10 w l title "ECt", \


';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';

}
else
{
echo "Датчик EC не задан. Если он есть сопоставьте соответсвующее поле в базе";
}

?>

