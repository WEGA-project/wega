<?php
include "menu.php";
echo "<img src='wega.png'>";
echo "<h1>Список доступных систем</h1>";

echo "<table border=1; width=1000px>";

echo "
<th style=color:red>Краткое имя
<th style=color:red>Подробное описание
<th style=color:red>t°C
<th style=color:red>RH
<th style=color:red>EC
<th style=color:red>pH
<th style=color:red>V
<th style=color:red>Обновлено
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

  if (dbval("namesys",$cname)){
    echo dbval("namesys",$cname);
  }
  else{
    echo $cname;
  }

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
