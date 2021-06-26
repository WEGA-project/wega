<?php
include_once "menu.php";

include_once "../config/".$ns.".conf.php";

if ($ns){

include_once "func.php";
echo "<br><b>Описание установки</b><br>";
pedit("namesys",$ns,'Гидропонная система',"Краткое наименование системы");
 $namesys=dbval("namesys",$ns);
 $comment=dbcomment("namesys",$ns);

echo "<br><b>Объем питательного бака</b><br>";
pedit("LevelFull",$ns,20,"Полный объем бака с питательным раствором");
 $LevelFull=dbval("LevelFull",$ns);

 echo "<br><b>ЕС чистой воды для изготовления расвтора</b><br>";
 pedit("helper_ecwater",$ns,0.01,"ЕС чистой воды");

echo "<br><b>Запас раствора вне бака в литрах в трубках коробах в субстрате</b><br>";
pedit("LevelAdd",$ns,2.5,"Запас раствора вне бака");
 $LevelAdd=dbval("LevelAdd",$ns);

echo "<br><b>Аварийная защита от перелива в литрах (это сколько литров сольется назад в бак при внезапной остановке циркуляции)</b><br>";
pedit("La",$ns,1,"Аварийный запас");
 $La=dbval("La",$ns);

echo "<br><b>Плановое значение ЕС в мСм/см</b><br>";
pedit("ECPlan",$ns,2,"Плановое значение ЕС");
 $ECPlan=dbval("ECPlan",$ns);

echo "<br><b>Суммарный вес сухих солей в граммах в литре раствора</b><br>";
pedit("sEC",$ns,2,"Вес солей в литре");
 $sEC=dbval("sEC",$ns);

echo "<br><b>Расчетный ЕС раствора</b><br>";
pedit("rEC",$ns,2,"Расчетный ЕС раствора");
 $rEC=dbval("rEC",$ns);

$Slk=sEC/rEC;

echo "<br><b>Кратность концентратов А и B XXX:1 </b><br>";
pedit("konc",$ns,100,"Кратность концентратов");
 $konc=dbval("konc",$ns);

}
else
{
echo "<h1>Система не выбрана</h1>";

}


?>

