<?php
include "menu.php";

echo '<br><a href="mixerbank.php'.$stfind.'">Концентраты</a>';
echo '<br><a href="mixersum.php'.$stfind.'">Статистика</a>';

if ( $_GET['ns'] ){

//include "../config/".$ns.".conf.php";
include "sqvar.php";
//include "funk.php";

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

//include "datetime.php";
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

dt,
s,
v1,
p1,
v2,
p2,
v3,
p3,
v4,
p4,
v5,
p5,
v6,
p6,
v7,
p7,
v8,
p8,
round ((p1-v1)/p1*100,2) as 'P1%',
round ((p2-v2)/p2*100,2) as 'P2%',
round ((p3-v3)/p3*100,2) as 'P3%',
round ((p4-v4)/p4*100,2) as 'P4%',
round ((p5-v5)/p5*100,2) as 'P5%',
round ((p6-v6)/p6*100,2) as 'P6%',
round ((p7-v7)/p7*100,2) as 'P7%',
round ((p8-v8)/p8*100,2) as 'P8%'

from $tb 
where $mixernum = if(s is null,0,s)

 
order by dt desc";


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
        echo "<th>".$property->name."</a></th>";
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
