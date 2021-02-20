<?php
// Подключаемся к базе
$link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");

if (!$link) {
    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}

include "func.php";
//include "dbvar.php";

//$LightRaw=dbval("LightRAW",$ns);
//if(".$dist."<".$distz.",".$distz."-".$dist.",null)
//@A1:=if ( ".$A1." < ".$Dr." and ".$A1." > 0 , ".$A1.", null),
//@A2:=if ( ".$A2." < ".$Dr." and ".$A2." > 0 , ".$A2.", null),
//@EC:=".$f_ec.",
//$tempEC=sensval("ftR(".dbval("ECtempRAW",$ns).")",$ns);
//@aTemp2:=".$f_atemp.",


$p_AirTemp=dbval("AirTemp",$ns);
$p_AirHum=dbval("AirHum",$ns);
$p_RootTemp=dbval("RootTemp",$ns);
$p_ECtempRAW=dbval("ECtempRAW",$ns);
$p_LightRaw=dbval("LightRaw",$ns);
$p_Dst=dbval("Dst",$ns);
$P_A1=dbval("A1",$ns);
$P_A2=dbval("A2",$ns);

$P_A2=dbval("A2",$ns);



$strSQL ="select 

dt,												# 1
@dAirTemp:=".$p_AirTemp.",
@dAirHum:=".$p_AirHum.",
@RootTemp:=if( ".$p_RootTemp."  < 80, ".$p_RootTemp.", null),
@EcTempRaw:=".$p_ECtempRAW.",
@LightRaw:=".$LightRaw.",
@dist,
@A1:=".$P_A1.",
@A2:=".$P_A2.",
@aTemp2:=ftR(".$p_ECtempRAW."),
@R2p,			#10
@R2n,
@R2,
@EC:=EC(".$P_A1.",".$P_A2.",25),
@ECt:=EC(".$P_A1.",".$P_A2.",@aTemp2),
@lev:= intpl(levmin(".$p_Dst.")),
@Lux:=if(@LightRaw=0,null, round(".$apht."*pow(@LightRaw,".$bpht."),0))/1000,
@SoilAll:=".$f_soil.",
@pH:=".$f_ph."


from $tb 
where dt  >  '".$wsdt."'- INTERVAL 1 DAY
 and  dt  <  '".$wpdt."'
 and isnull(".$A1.") = false
 and isnull(".$A2.") = false
 and isnull(".$dist.") = false
 and ".$RootTemp." != 85  and ".$RootTemp." != -28.375 and ".$RootTemp." != -0.063

order by dt";


//@lev:=intpl(".$dist."),

// Выполняем запрос
$rs=mysqli_query($link, $strSQL);
$numb=mysqli_num_rows($rs);
mysqli_data_seek($rs,$numb-1);
$row=mysqli_fetch_row($rs);
?>
