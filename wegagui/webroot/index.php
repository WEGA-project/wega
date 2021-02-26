<?php
include "menu.php";
echo "<img src='wega.png'>";
echo "<h1>Список доступных систем</h1>";

echo "<table border=1>";

echo "
<th>Краткое имя
<th>Подробное описание
<th>t°C
<th>RH
<th>EC
<th>pH
<th>V
<th>Обновлено
</th>";

foreach (glob("../config/*.conf.php") as $filename) {

  include $filename;
  $fl=explode("/", $filename);
  $nm=explode(".", $fl[2]);
  $cname=$nm[0];

//  echo " <a href=".$_SERVER['PHP_SELF']."?ns=".$cname." > " .$namesys."</a>";
  echo " ";
 $ns=$cname;
include "sqvar.php"; 
echo "<tr>";

echo "<td>";
  echo "<a href=status.php?ns=".$ns.">";
  echo dbval("namesys",$cname);
  echo "</a>";
echo "<td>";
  echo dbcomment("namesys",$cname);
echo "<td>";
  echo round($AirTemp,1);
echo "<td>";
  echo round($AirHum,0)."%";
echo "<td>";
  echo round($ec,1);
echo "<td>";
  if ($p_pHraw != 'null'){echo round($ph,1);}
echo "<td>";
  echo round($lev,1);
echo "<td>";
  echo $dt;

echo "</tr>";

}

echo "</table>";


?>
