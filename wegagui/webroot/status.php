<?php
include_once "menu.php";

$ns=$_GET['ns'];

if ($ns){

include_once "func.php";
include "sqvar.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
echo "<br>";

echo "<h3>Текущие контрольные показания</h3>";

include "tstatus.php";

}
else
{
echo "<h1>Система не выбрана</h1>";
}


?>
