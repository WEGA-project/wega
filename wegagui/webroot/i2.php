<?php
include "top.php";
echo "<img src='wega.png'>";
//<a href="rep.php?ns=balkon-r">Балкон правый</a>
//<br><a href="rep.php?ns=balkon-l">Балкон левый</a>
foreach (glob("../config/*.conf.php") as $filename) {
    //echo "$filename размер " . filesize($filename) . "<br>";
    include $filename;
    $fl=explode("/", $filename);
    $nm=explode(".", $fl[2]);
    $cname=$nm[0];
    //echo "<br>".$cname."<br>";
    echo "<a href=rep.php?ns=".$cname.">". $namesys ."</a><br>";

}

?>
