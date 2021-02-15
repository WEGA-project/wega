<?php
include "menu.php";



include "../config/".$ns.".conf.php";

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";


include "datetime.php";

$ns="esp32wega";
$cl="am2320hum";
include "plotdbc.php";


$ns="esp32wega";
$cl="am2320temp";
//include "plotdbc.php";

?>

