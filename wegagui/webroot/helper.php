<?php



$ns=$_GET['ns'];
if ($ns){
//include "../config/".$ns.".conf.php";

include_once "func.php";
include "sqvar.php";


echo '<br><br><h2>Помощник</h2>';


echo ("Для получения ЕС=".$ECPlan." мСм/см нужно долить: <b>". round($L2,1)."л.</b> до уровня ".($LevelFull-$La).", c ЕС=".round( $ECn   ,2)." мСм/см" );
echo ("<br>Это: <b>".round($Soiln,2)." грамм</b> солей или по ".round( $Soiln/2/$konc*1000,0)." мл концентратов ".$konc.":1 с каждого");
}

?>

