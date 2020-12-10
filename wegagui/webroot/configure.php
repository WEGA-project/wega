<?php
include "menu.php";


echo "<b>привет вика</b>";


include "../config/".$ns.".conf.php";


echo '
<form action="" method="get">
 <p>Температура воздуха: <input type="text" name="AirTemp" value='.$_GET["AirTemp"].'></p>
 <p>Температура раствора: <input type="text" name="WaterTemp" value=""></p>
 <p>Температура корней: <input type="text" name="RootTemp" value=""></p>
 <p><input type="submit" value="Задать"/>
</form>';

echo $_GET['AirTemp'];

// Подключаемся к базе
$link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");

if (!$link) {
    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}


?>
