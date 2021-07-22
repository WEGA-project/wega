<?php
include "menu.php";

if ( $_GET['ns'] ){

//include "../config/".$ns.".conf.php";
include "sqvar.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
echo "<h2>Миксер ".$my_db."</h2>";

echo "<br><b>Имя базы миксера</b><br>";
pedit("mixerdb",$ns,"mixer","Имя базы миксера");
 $mixerdb=dbval("mixerdb",$ns);

echo "<br><b>Номер системы в базе миксера</b><br>";
pedit("mixernum",$ns,0,"Номер системы в базе миксера (0 - все)");
 $mixernum=dbval("mixernum",$ns); 

include "datetime.php";
$my_db="mixer";

// Подключаемся к базе
$link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");

if (!$link) {
    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}

$tb="weght";

$strSQL ="select 
year(dt),
month(dt),
round(sum(v1)) as P1,
round(sum(v2)) as P2,
round(sum(v3)) as P3,
round(sum(v4)) as P4,
round(sum(v5)) as P5,
round(sum(v6)) as P6,
round(sum(v7)) as P7,
round(sum(v8)) as P8

from $tb 
group by year(dt),month(dt)
";



// Выполняем запрос
$rs=mysqli_query($link, $strSQL);
$numb=mysqli_num_rows($rs);
mysqli_data_seek($rs,$numb-1);
$row=mysqli_fetch_row($rs);
mysqli_data_seek($rs,0);


echo "<table border='1'>";
// Вытаскиваем имена полей и формируем заголовок таблицы результатов
echo "<tr>";
while ($property = mysqli_fetch_field($rs)) 
        { 
        echo "<th><a href='plotdb.php?ns=".$ns."&cl=".$property->name."&wsdt=".$wsdt."&wpdt=".$wpdt."'>";
        echo $property->name;
        echo "</a></th>"; 
        }
echo "</td></tr>";
// Извлекаем значения и формируем таблицу результатов
while($id=mysqli_fetch_row($rs))
        { 
        echo "<tr>";
        for ($x=0; $x<=count($id)-1; $x++) 
                {
                echo "<td>".$id[$x];
                }
        echo "</td>";
        }
echo "</td></table>";
}

else
{
echo "Не выбрана система";
}


?>
