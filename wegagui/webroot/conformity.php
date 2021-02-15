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
echo "<h2>Сопоставление полей в базе данных</h2>";

//if (dbval("A1",$ns)=='') {setdbval($ns,"A1","Ap","Имя поля в базе содержащее raw значение ЕС при положительной фазе ");}
//if (dbval("A2",$ns)=='') {setdbval($ns,"A2","An","Имя поля в базе содержащее raw значение ЕС при отрицательной фазе ");}
//if (dbval("pHraw",$ns)=='') {setdbval($ns,"pHraw","pHraw","Имя поля в базе содержащее raw значение pH");}


//$A1=dbval("A1",$ns); echo "<a href=setpapam.php?ns=".$ns."&parameter=".A1."> A1 </a> = ".$A1." ".dbcomment("A1",$ns)."<br>";
//$A2=dbval("A2",$ns); echo "<a href=setpapam.php?ns=".$ns."&parameter=".A2."> A2 </a> = ".$A2." ".dbcomment("A2",$ns)."<br>";
//$pHraw=dbval("pHraw",$ns); echo "<a href=setpapam.php?ns=".$ns."&parameter=".pHraw."> pHraw </a> = ".$pHraw." ".dbcomment("pHraw",$ns)."<br>";



form($ns,"A1","Датчик ЕС при положительной фазе (RAW)");
form($ns,"A2","Датчик ЕС при отрицательной фазе (RAW)");
form($ns,"ECtempRAW","Датчик EC температура (RAW)");
form($ns,"pHraw","Датчик pH (RAW)");
form($ns,"LightRAW","Датчик яркости света (RAW)");
form($ns,"RootTemp","Температура в зоне корней (град.)");
form($ns,"AirTemp","Температура воздуха (град.)");
form($ns,"AirHum","Влажность воздуха (%)");
form($ns,"Dst","Уровнемер (см)");


}



function dbpsel($ns,$p,$comment){

include "../config/".$ns.".conf.php";

// Подключаемся к базе
$link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");

$strSQL ="select * from $tb order by dt limit 1";


// Выполняем запрос
$rs=mysqli_query($link, $strSQL);
$numb=mysqli_num_rows($rs);
mysqli_data_seek($rs,$numb-1);
$row=mysqli_fetch_row($rs);
mysqli_data_seek($rs,0);

echo "<option selected>".dbval($p,$ns)."</option>";

while ($property = mysqli_fetch_field($rs)) 
        { 
        echo "<option>";
        echo $property->name;
        echo "</option>"; 
        }
echo "<option>null</option>";
}


function form($ns,$parm,$comment){
//$parm="A1";
echo " <form action='' method='get'>";
echo "   <input type='hidden' name='ns' value='".$ns."'>";
//echo "   <input type='text' value='".$parm."'>";
echo "   <select size='1' name='".$parm."'>";
dbpsel($ns,$parm);
echo $comment;
echo "   </select>";
//echo $parm;

echo "  <input type='submit' value='Задать'>";
//echo " (". $parm.") ".$comment;
echo " ".$comment;
echo "</p></form>";

if ( $_GET[$parm] ){ 
$value="$_GET[$parm]";
setdbval($ns,$parm,$value,$comment);


echo "SAVE: ".$parm."=".$_GET[$parm]." ".$comment;
echo "
  <head>
   <meta http-equiv='Refresh' content='0; URL=".$_SERVER['HTTP_REFERER']."'>
  </head>
";


}


}


?>
