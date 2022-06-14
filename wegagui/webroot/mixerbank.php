<?php
include "menu.php";
//$ns=$_GET['ns'];
//include "func.php";





//include "../config/".$ns.".conf.php";
include "sqvar.php";
echo "<h1>Учет концентратов для миксера".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
echo "<br>";
echo "<h2>Емкости с концентратами</h2>";

// Форма добавления
echo "<br>Добавить концентрат<br>
            <form action='' method='GET'>
                   <input type='text' name='dt' value='".date('Y-m-d H:i:s')."'>
                   <input type='text' name='name' value='' placeholder='Название раствора'>
                   <input type='text' name='volume' value='' placeholder='Имя помпы'>
                   <input type='text' name='v' value='' placeholder='Объем емкости (мл)'>
                   <input type='text' name='fi' value='' placeholder='Концентрация г/л'>
                   <input type='text' name='ro' value='' placeholder='Плотность г/мл'>
                   <input type='text' name='datecreate' value='' placeholder='Дата изготовления'>
                   <input type='text' name='vbase' value='' placeholder='Поле в базе'>
              <input type='submit' value='add' name='s'>
            </form>
      <br>
";


$tb="banks";
$my_db="mixer";

$id=$_GET['id'];
$dt=$_GET['dt'];
$name=$_GET['name'];
$volume=$_GET['volume'];
$v=$_GET['v'];
$fi=$_GET['fi'];
$ro=$_GET['ro'];
$datecreate=$_GET['datecreate'];
$vbase=$_GET['vbase'];

$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");


// Добавляем
if ( $_GET['s'] == 'add' ) {
//mysqli_query($link, "CREATE DATABASE $my_db");
mysqli_query($link, "create table $tb (id INT(11) PRIMARY KEY AUTO_INCREMENT)");
//mysqli_query($link, "create table $tb (dt DATETIME PRIMARY KEY)");
mysqli_query($link, "alter table $tb add column dt DATETIME");
mysqli_query($link, "alter table $tb add column name char(128)");
mysqli_query($link, "alter table $tb add column volume char(128)");
mysqli_query($link, "alter table $tb add column v float");
mysqli_query($link, "alter table $tb add column fi float");
mysqli_query($link, "alter table $tb add column ro float");
mysqli_query($link, "alter table $tb add column datecreate char(128)");
mysqli_query($link, "alter table $tb add column vbase char(16)");

mysqli_query($link, "insert into $tb (
    dt, 
    name, 
    volume,
    v,
    fi,
    ro,
    datecreate,
    vbase
     ) values (
   '$dt', 
   '$name', 
   '$volume',
   $v,
   $fi,
   $ro,
   '$datecreate',
   '$vbase'
     
     )" );
}

// Удаляем
if ( $_GET['s'] == 'del' ) {
mysqli_query($link, "delete from $tb where id='$id'");
}

// Редактируем
if ( $_GET['s'] == 'edit' ) {
mysqli_query($link, "update $tb set 
    dt='$dt', 
    name='".urldecode($name)."', 
    volume='$volume', 
    v='$v',
    fi='$fi',
    ro='$ro',
    datecreate='$datecreate',
    vbase='$vbase'
    where id='$id' " );
}



$strSQL ="select * from $tb  order by vbase";


// Выполняем запрос
$rs=mysqli_query($link, $strSQL);


echo "<table border='1'>";



// Извлекаем значения и формируем таблицу результатов
while($id=mysqli_fetch_row($rs))
        {echo " 
           <form>
              <form action='' method='get'>
                   <input type='hidden' name='id' value='".$id[0]."'>
                   <input type='text' name='dt' value='".$id[1]."'>
                   <input type='text' name='name' value='".$id[2]."'>
                   <input type='text' name='volume' value=".$id[3].">
                   <input type='text' name='v' value=".$id[4].">
                   <input type='text' name='fi' value=".$id[5].">
                   <input type='text' name='ro' value=".$id[6].">
                   <input type='text' name='datecreate' placeholder='Дата изготовления' value=".$id[7]." >
                   <input type='text' name='vbase' placeholder='Поле в базе' value=".$id[8].">
              <input type='submit' value='edit' name='s'>
              <input type='submit' value='del' name='s'>
           </form>
          <br>";


        }




mysqli_close($link);


echo "<br>";

$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");

$strSQL ="select volume,name,ro,dt,v,fi from $tb  where vbase != '' order by volume";
$rs=mysqli_query($link, $strSQL);
while($id=mysqli_fetch_row($rs))
  {
    $pomp = $id[0];   // Имя насоса
    $name = $id[1];   // Название раствора
    $ro = $id[2];     // Плотность раствора в г/мл
    $dt = $id[3];     // Дата установки емкости
    $v = $id[4];      // Объем емкости в мл.
    $fi = $id[5];     // Концентрация раствора г/л

    // Получаем остаток в емкости в
    $Weight = mixer_banks("$pomp")-> sumves; // Израсходованно раствора в граммах
    $Volume = $Weight / $ro;                 // Израсходованно в мл.
    $rWeight  = mixer_banks("$pomp")-> remain; // Остаток в емкости в граммах
    $rPercent = mixer_banks("$pomp")-> procent; // Остаточный процент
    $rVolume = $rWeight / $ro; // Остаток в мл.
   
    $WeightFull = $v*$ro; // Вес полной емкости с раствором
    $date = new DateTime($dt);
    $udate = $date->getTimestamp();
    $age = (time()-$udate); // Время использования раствора в секундах
    $CWeek = $Volume/($age/60/60/24/7); // Расход в неделю в мл
    $SoilWeek = $CWeek * $fi / 1000; // Расход сухих солей в неделю
    $Enough = $rVolume/($Volume/($age/60/60/24)); // Хватит на дней

    echo "<div class='Block'>";
    echo "<b>Насос: ".$pomp."</b></br>";
    echo "Ёмкость: ".$v." мл. (".round($WeightFull,2)." гр.)</br>";
    echo "Содержимое: ".$name." (".$fi."г/л ".$ro."мг/мл)<br>";
    echo "Остаток: <b>".round($rPercent)."%</b>  [".round($rVolume)."мл, ".round($rWeight)."гр.]<br> ";
    echo "Используется: ".showDate( $date->getTimestamp() );
    echo ", расход: ".round($CWeek). " мл. в неделю. Хватит приблизительно на ".round($Enough)." дней<br>";
    echo "Пересчет на сухие соли: ".round($SoilWeek,2)." грамм в неделю";
    echo "</div>";
    gbar($rPercent,$pomp);
  }
mysqli_close($link);
?>


