<?php
include_once "func.php";

$p_AirTemp=dbval("AirTemp",$ns);
$p_AirHum=dbval("AirHum",$ns);
$p_RootTemp=dbval("RootTemp",$ns);
$p_ECtempRAW=dbval("ECtempRAW",$ns);
$p_LightRaw=dbval("LightRaw",$ns);
$p_Dst=dbval("Dst",$ns);
$P_A1=dbval("A1",$ns);
$P_A2=dbval("A2",$ns);
$P_A2=dbval("A2",$ns);

 $namesys=dbval("namesys",$ns);
 $comment=dbcomment("namesys",$ns);
 $LevelFull=dbval("LevelFull",$ns);
 $LevelAdd=dbval("LevelAdd",$ns);
 $La=dbval("La",$ns);
 $ECPlan=dbval("ECPlan",$ns);
 $sEC=dbval("sEC",$ns);
 $rEC=dbval("rEC",$ns);
$Slk=sEC/rEC;
 $konc=dbval("konc",$ns);


?>
