<?php
include "menu.php";
echo "<img src='wega.png'>";
echo "<h1>Список доступных систем</h1>";
foreach (glob("../config/*.conf.php") as $filename) {
  include $filename;
  $fl=explode("/", $filename);
  $nm=explode(".", $fl[2]);
  $cname=$nm[0];
  echo "<li>";
  echo " <a href=".$_SERVER['PHP_SELF']."?ns=".$cname." > " .$namesys."</a>";
  echo " ";
  echo $comment;
  echo "</li>";
}

?>
