<?php
// Подключаемся к базе
$link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");

if (!$link) {
    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}

include_once "sqvar.php";


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

order by dt";

// and ".$RootTemp." != 85  and ".$RootTemp." != -28.375 and ".$RootTemp." != -0.063

//@lev:=intpl(".$dist."),

// Выполняем запрос
$rs=mysqli_query($link, $strSQL);
$numb=mysqli_num_rows($rs);
mysqli_data_seek($rs,$numb-1);
$row=mysqli_fetch_row($rs);
?>
