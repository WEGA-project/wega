<?php
include "menu.php";

//include "../config/".$ns.".conf.php";


if ($ns){
include "sqvar.php";

echo "<br>Пересоздание функций расчета";
$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");
echo "<br> для базы: ";
echo $my_db;
mysqli_query($link, "DROP FUNCTION IF EXISTS line2point;");
mysqli_query($link, "DROP FUNCTION IF EXISTS fpR;");
mysqli_query($link, "DROP FUNCTION IF EXISTS int3point;");
mysqli_query($link, "DROP FUNCTION IF EXISTS EC;");
mysqli_query($link, "DROP FUNCTION IF EXISTS ftR;");
mysqli_query($link, "DROP FUNCTION IF EXISTS intpl;");
mysqli_query($link, "DROP FUNCTION IF EXISTS levmin;");
mysqli_query($link, "DROP FUNCTION IF EXISTS ph;");
mysqli_query($link, "DROP FUNCTION IF EXISTS R3950;");


mysqli_close($link);

include "sqfunc.php";

}
else
{
echo "Не выбрана система";
}



?>
