<?php
// Подключаемся к базе
$link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");

if (!$link) {
    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}



$strSQL ="select 

dt,												# 1
@dAirTemp:=".$dAirTemp.",
@dAirHum:=".$dAirHum.",
@RootTemp:=".$RootTemp.",
@EcTempRaw:=".$EcTempRaw.",
@LightRaw:=".$LightRaw.",
@dist:=if(".$dist."<".$distz.",".$distz."-".$dist.",null),
@A1:=if ( ".$A1." < ".$Dr." and ".$A1." > 0 , ".$A1.", null),
@A2:=if ( ".$A2." < ".$Dr." and ".$A2." > 0 , ".$A2.", null),
@aTemp2:=".$f_atemp.",
@R2p:=(((-@A2*".$R1."-@A2*".$Rx1."+".$R1."*".$Dr."+".$Rx1."*".$Dr.")/@A2)),			#10
@R2n:=(-(-(@A1)*".$R1."-(@A1)*".$Rx2."+".$Rx2."*".$Dr.")/(-(@A1)+".$Dr.")),
@R2:=(@R2p+@R2n)/2,
@EC:=".$f_ec.",
@ECt:=@EC/(1+".$k."*(@aTemp2-25)),
@lev:= ".$f_lev.",
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
