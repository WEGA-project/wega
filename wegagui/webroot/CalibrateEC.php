<?php
include "menu.php";
include "func.php";

$ns=$_GET['ns'];



if ( $_GET['ns'] ){


include "../config/".$ns.".conf.php";
echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
echo "<br>";
echo "<h2>Калибровка EC</h2>";
echo "<h3>Расчет сопротивления</h3>";


$R1=dbval("R1",$ns); echo "<a href=setpapam.php?ns=".$ns."&parameter=".R1."> R1 </a> = ".$R1." ".dbcomment("R1",$ns)."<br>";
$Rx1=dbval("Rx1",$ns); echo "<a href=setpapam.php?ns=".$ns."&parameter=".Rx1."> Rx1 </a> = ".$Rx1." ".dbcomment("Rx1",$ns)."<br>";
$Rx2=dbval("Rx2",$ns); echo "<a href=setpapam.php?ns=".$ns."&parameter=".Rx2."> Rx1 </a> = ".$Rx2." ".dbcomment("Rx2",$ns)."<br>";
$Dr=dbval("Dr",$ns); echo "<a href=setpapam.php?ns=".$ns."&parameter=".Dr."> Dr </a> = ".$Dr." ".dbcomment("Dr",$ns)."<br>";

$A1=dbval("A1",$ns); echo "<a href=setpapam.php?ns=".$ns."&parameter=".A1."> A1 </a> = ".$A1." ".dbcomment("A1",$ns)."<br>";
$A2=dbval("A2",$ns); echo "<a href=setpapam.php?ns=".$ns."&parameter=".A2."> A2 </a> = ".$A2." ".dbcomment("A2",$ns)."<br>";

echo "aa";
$A1v=sensval($A1,$ns);
echo sensval(An,$ns);

echo $A1v;



if (dbval("Rx1",$ns)=='') {setdbval($ns,"Rx1","-120","Внутреннее сопротивление подбираются таким образом, что-бы во всех калибровочных растворах значения Rp и  Rn сошлись");}
if (dbval("Rx2",$ns)=='') {setdbval($ns,"Rx2","0","Внутреннее сопротивление подбираются таким образом, что-бы во всех калибровочных растворах значения Rp и  Rn сошлись");}
if (dbval("R1",$ns)=='') {setdbval($ns,"R1","509.3","Резистор делителя R1 в омах");}

if (dbval("Dr",$ns)=='') {setdbval($ns,"Dr","4095","Предел АЦП");}
if (dbval("A1",$ns)=='') {setdbval($ns,"A1","Ap","Имя поля в базе содержащее raw значение ЕС при положительной фазе ");}
if (dbval("A2",$ns)=='') {setdbval($ns,"A2","An","Имя поля в базе содержащее raw значение ЕС при отрицательной фазе ");}



}
?>
