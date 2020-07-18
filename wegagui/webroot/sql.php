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
@A1:=if(".$A1."<1023,".$A1.",null),
@A2:=if(".$A2.">10,".$A2.",null),
@aTemp2:=".$pa."*pow(@EcTempRaw,2) + ".$pb."*@EcTempRaw + ".$pc.",
@R2p:=(((-@A2*".$R1."-@A2*".$Rx1."+".$R1."*".$Dr."+".$Rx1."*".$Dr.")/@A2)),			#10
@R2n:=(-(-(@A1)*".$R1."-(@A1)*".$Rx2."+".$Rx2."*".$Dr.")/(-(@A1)+".$Dr.")),
@R2:=(@R2p+@R2n)/2,
@EC:=if(@R2>0,  ".$ea."*pow(@R2,".$eb.") , 0),
@ECt:=@EC/(1+".$k."*(@aTemp2-25)),
@lev:= ".$f_lev.",
@Lux:=round(".$apht."*pow(@LightRaw,".$bpht."),0),
@SoilAll:=".$f_soil."

from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
 and isnull(".$A1.") = false
 and isnull(".$A2.") = false
 and isnull(".$dist.") = false
 and isnull(thermistor_1_raw) = false
order by dt limit $limit";


//@lev:=intpl(".$dist."),

// Выполняем запрос
$rs=mysqli_query($link, $strSQL);
$numb=mysqli_num_rows($rs);
mysqli_data_seek($rs,$numb-1);
$row=mysqli_fetch_row($rs);
?>
