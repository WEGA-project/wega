<?php

$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");


// Процедурв линейной интерполяции по двум точкам
//CREATE DEFINER=`root`@`localhost` FUNCTION `line2point`(

mysqli_query($link, "

CREATE FUNCTION `line2point`(
x1 FLOAT,
y1 FLOAT,
x2 FLOAT,
y2 FLOAT,
x  FLOAT) RETURNS float
BEGIN

set @a:=(-x1*y2+x2*y1)/(x2-x1);
set @k:=(y2-y1)/(x2-x1);
set @y:=@a + @k *  x;
RETURN @y;
END

");



// Функция sql процедура перевода фоторезистора в люксы 
mysqli_query($link, "

CREATE FUNCTION `fpR`(rawP FLOAT) RETURNS float
BEGIN

set @px1:=(select value from config where parameter='pR_raw_p1' limit 1);
set @px2:=(select value from config where parameter='pR_raw_p2' limit 1);
set @px3:=(select value from config where parameter='pR_raw_p3' limit 1);

set @py1:=(select value from config where parameter='pR_val_p1' limit 1);
set @py2:=(select value from config where parameter='pR_val_p2' limit 1);
set @py3:=(select value from config where parameter='pR_val_p3' limit 1);

set @pa:=-(-@px1*@py3 + @px1*@py2 - @px3*@py2 + @py3*@px2 + @py1*@px3 - @py1*@px2) /  (-pow(@px1,2)*@px3 + pow(@px1,2)*@px2 - @px1*pow(@px2,2) + @px1*pow(@px3,2) - pow(@px3,2)*@px2 + @px3*pow(@px2,2) ); 
set @pb:=( @py3*pow(@px2,2) - pow(@px2,2)*@py1 + pow(@px3,2)*@py1 + @py2*pow(@px1,2) - @py3*pow(@px1,2) - @py2 * pow(@px3,2) ) /  ( (-@px3+@px2) * (@px2*@px3 - @px2*@px1 + pow(@px1,2) - @px3*@px1 ) );
set @pc:=( @py3*pow(@px1,2)*@px2 - @py2*pow(@px1,2)*@px3 - pow(@px2,2)*@px1*@py3 + pow(@px3,2)*@px1*@py2 + pow(@px2,2)*@py1*@px3 - pow(@px3,2)*@py1*@px2 ) /  ( (-@px3+@px2) * (@px2*@px3 - @px2*@px1 + pow(@px1,2) - @px3*@px1 ) );

RETURN @pa*pow(rawP,2) + @pb*rawP + @pc;

END
");




// Процедура интерполяции по трем точкам
mysqli_query($link, "

CREATE FUNCTION `int3point`(
px1 FLOAT,
py1 FLOAT,
px2 FLOAT,
py2 FLOAT,
px3 FLOAT,
py3 FLOAT,


x  FLOAT) RETURNS float
BEGIN
set @pa:=-(-px1*py3 + px1*py2 - px3*py2 + py3*px2 + py1*px3 - py1*px2) /  (-pow(px1,2)*px3 + pow(px1,2)*px2 - px1*pow(px2,2) + px1*pow$
set @pb:=( py3*pow(px2,2) - pow(px2,2)*py1 + pow(px3,2)*py1 + py2*pow(px1,2) - py3*pow(px1,2) - py2 * pow(px3,2) ) /  ( (-px3+px2) * ($
set @pc:=( py3*pow(px1,2)*px2 - py2*pow(px1,2)*px3 - pow(px2,2)*px1*py3 + pow(px3,2)*px1*py2 + pow(px2,2)*py1*px3 - pow(px3,2)*py1*px2$

RETURN @pa*pow(x,2) + @pb*x + @pc;
END
");


// Калибровка EC 
mysqli_query($link, "

CREATE FUNCTION `EC`(A1 FLOAT,A2 FLOAT, Temp FLOAT) RETURNS float
BEGIN
set @R1 := (select value from config where parameter='EC_R1' limit 1);
set @Rx1 := (select value from config where parameter='EC_Rx1' limit 1);
set @Rx2 := (select value from config where parameter='EC_RX2' limit 1);
set @Dr := (select value from config where parameter='Dr' limit 1);

set @ec1 := (select value from config where parameter='EC_val_p1' limit 1);
set @ec2 := (select value from config where parameter='EC_val_p2' limit 1);
set @ex1 := (select value from config where parameter='EC_R2_p1' limit 1);
set @ex2 := (select value from config where parameter='EC_R2_p2' limit 1);

set @kt := (select value from config where parameter='EC_kT' limit 1);

set @R2p:=(((-A2*@R1-A2*@Rx1+@R1*@Dr+@Rx1*@Dr)/A2));
set @R2n:=(-(-A1*@R1-A1*@Rx2+@Rx2*@Dr)/(-A1+@Dr));
set @R2:=(@R2p+@R2n)/2;

set @eb:=(-log(@ec1/@ec2))/(log(@ex2/@ex1));
set @ea:=pow(@ex1,(-@eb))*@ec1;

set @ec:=if(@R2>0,@ea*pow(@R2,@eb),null);

set @ECt:=@ec/(1+@kt*(Temp-25));
RETURN @ECt;
END
");

// Калибровка терморезистора 
mysqli_query($link, "

CREATE FUNCTION `ftR`(rawT FLOAT) RETURNS float
BEGIN

set @px1:=(select value from config where parameter='tR_raw_p1' limit 1);
set @px2:=(select value from config where parameter='tR_raw_p2' limit 1);
set @px3:=(select value from config where parameter='tR_raw_p3' limit 1);

set @py1:=(select value from config where parameter='tR_val_p1' limit 1);
set @py2:=(select value from config where parameter='tR_val_p2' limit 1);
set @py3:=(select value from config where parameter='tR_val_p3' limit 1);

set @pa:=-(-@px1*@py3 + @px1*@py2 - @px3*@py2 + @py3*@px2 + @py1*@px3 - @py1*@px2) /  (-pow(@px1,2)*@px3 + pow(@px1,2)*@px2 - @px1*pow(@px2,2) + @px1*pow(@px3,2) - pow(@px3,2)*@px2 + @px3*pow(@px2,2) ); 
set @pb:=( @py3*pow(@px2,2) - pow(@px2,2)*@py1 + pow(@px3,2)*@py1 + @py2*pow(@px1,2) - @py3*pow(@px1,2) - @py2 * pow(@px3,2) ) /  ( (-@px3+@px2) * (@px2*@px3 - @px2*@px1 + pow(@px1,2) - @px3*@px1 ) );
set @pc:=( @py3*pow(@px1,2)*@px2 - @py2*pow(@px1,2)*@px3 - pow(@px2,2)*@px1*@py3 + pow(@px3,2)*@px1*@py2 + pow(@px2,2)*@py1*@px3 - pow(@px3,2)*@py1*@px2 ) /  ( (-@px3+@px2) * (@px2*@px3 - @px2*@px1 + pow(@px1,2) - @px3*@px1 ) );

RETURN @pa*pow(rawT,2) + @pb*rawT + @pc;

END

");

mysqli_close($link);


?>
