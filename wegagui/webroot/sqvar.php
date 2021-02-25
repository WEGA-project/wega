<?php
include_once "func.php";

$p_AirTemp=dbval("AirTemp",$ns);
$p_AirHum=dbval("AirHum",$ns);
$p_RootTemp=dbval("RootTemp",$ns);
$p_ECtempRAW=dbval("ECtempRAW",$ns);
$p_pHraw=dbval("pHraw",$ns);
$p_LightRaw=dbval("LightRaw",$ns);
$p_Dst=dbval("Dst",$ns);
$P_A1=dbval("A1",$ns);
$P_A2=dbval("A2",$ns);

$p_ECtemp="ftr(".$p_ECtempRAW.")";
$p_Lux="fpr(".$p_LightRaw.")";
$p_pH="pH(".$p_pHraw.")";
$p_EC="EC(".$P_A1.",".$P_A2.",".$p_ECtemp.")";
$p_lev="intpl(levmin(".$p_Dst."))";

 $namesys=dbval("namesys",$ns);
 $comment=dbcomment("namesys",$ns);
 $LevelFull=dbval("LevelFull",$ns);
 $LevelAdd=dbval("LevelAdd",$ns);
 $La=dbval("La",$ns);
 $ECPlan=dbval("ECPlan",$ns);
 $sEC=dbval("sEC",$ns);
 $rEC=dbval("rEC",$ns);
 $Slk=($sEC/$rEC);
 $konc=dbval("konc",$ns);


$A1=sensval($P_A1,$ns);
$A2=sensval($P_A2,$ns);
$AirHum=sensval($p_AirHum,$ns);
$AirTemp=sensval($p_AirTemp,$ns);
$RootTemp=sensval($p_RootTemp,$ns);
$tempEC=sensval("ftR(".dbval("ECtempRAW",$ns).")",$ns);
$Lux=sensval("fpR(".dbval("LightRAW",$ns).")",$ns);
$ec=sensval("EC($P_A1,$P_A2,".$tempEC.")",$ns);
$ph=sensval("ph(".dbval("pHraw",$ns).")",$ns);
$lev=sensval("intpl(levmin(".$p_Dst."))",$ns);

$L1=$lev+$LevelAdd;
$L2=$LevelFull-$lev-$La;
$ECn=(-($EC*$L1 - $ECPlan*$L1 - $ECPlan*$L2 )/$L2);
$Soiln=$ECn*$Slk*($L2);

$p_soil="($p_lev+".$L1.")*$p_EC*$Slk";

?>
