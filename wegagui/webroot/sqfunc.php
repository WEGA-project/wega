<?php
$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");

// Процедурв линейной интерполяции по двум точкам
mysqli_query($link, "

CREATE FUNCTION `line2point`(
x1 FLOAT,
y1 FLOAT,
x2 FLOAT,
y2 FLOAT,
x  FLOAT) RETURNS float
BEGIN
# test
set @a:=(-x1*y2+x2*y1)/(x2-x1);
set @k:=(y2-y1)/(x2-x1);
set @y:=@a + @k *  x;
RETURN @y;
END

");

// Функция sql процедура перевода фоторезистора в люксы 
mysqli_query($link, "

CREATE DEFINER=`root`@`localhost` FUNCTION `fpR`(rawP FLOAT) RETURNS float
BEGIN

IF @fpRf is null THEN

set @ppx1:=(select value from config where parameter='pR_raw_p1' limit 1);
set @ppx2:=(select value from config where parameter='pR_raw_p2' limit 1);
set @ppx3:=(select value from config where parameter='pR_raw_p3' limit 1);

set @ppy1:=(select value from config where parameter='pR_val_p1' limit 1);
set @ppy2:=(select value from config where parameter='pR_val_p2' limit 1);
set @ppy3:=(select value from config where parameter='pR_val_p3' limit 1);


set @ppa:=-(-@ppx1*@ppy3 + @ppx1*@ppy2 - @ppx3*@ppy2 + @ppy3*@ppx2 + @ppy1*@ppx3 - @ppy1*@ppx2) /  (-pow(@ppx1,2)*@ppx3 + pow(@ppx1,2)*@ppx2 - @ppx1*pow(@ppx2,2) + @ppx1*pow(@ppx3,2) - pow(@ppx3,2)*@ppx2 + @ppx3*pow(@ppx2,2) ); 
set @ppb:=( @ppy3*pow(@ppx2,2) - pow(@ppx2,2)*@ppy1 + pow(@ppx3,2)*@ppy1 + @ppy2*pow(@ppx1,2) - @ppy3*pow(@ppx1,2) - @ppy2 * pow(@ppx3,2) ) /  ( (-@ppx3+@ppx2) * (@ppx2*@ppx3 - @ppx2*@ppx1 + pow(@ppx1,2) - @ppx3*@ppx1 ) );
set @ppc:=( @ppy3*pow(@ppx1,2)*@ppx2 - @ppy2*pow(@ppx1,2)*@ppx3 - pow(@ppx2,2)*@ppx1*@ppy3 + pow(@ppx3,2)*@ppx1*@ppy2 + pow(@ppx2,2)*@ppy1*@ppx3 - pow(@ppx3,2)*@ppy1*@ppx2 ) /  ( (-@ppx3+@ppx2) * (@ppx2*@ppx3 - @ppx2*@ppx1 + pow(@ppx1,2) - @ppx3*@ppx1 ) );


set @fpRf:=1;
END IF;

RETURN @ppa*pow(rawP,2) + @ppb*rawP + @ppc;

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
set @pa:=-(-px1*py3 + px1*py2 - px3*py2 + py3*px2 + py1*px3 - py1*px2) /  (-pow(px1,2)*px3 + pow(px1,2)*px2 - px1*pow(px2,2) + px1*pow(px3,2) - pow(px3,2)*px2 + px3*pow(px2,2) ); 
set @pb:=( py3*pow(px2,2) - pow(px2,2)*py1 + pow(px3,2)*py1 + py2*pow(px1,2) - py3*pow(px1,2) - py2 * pow(px3,2) ) /  ( (-px3+px2) * (px2*px3 - px2*px1 + pow(px1,2) - px3*px1 ) );
set @pc:=( py3*pow(px1,2)*px2 - py2*pow(px1,2)*px3 - pow(px2,2)*px1*py3 + pow(px3,2)*px1*py2 + pow(px2,2)*py1*px3 - pow(px3,2)*py1*px2 ) /  ( (-px3+px2) * (px2*px3 - px2*px1 + pow(px1,2) - px3*px1 ) );

RETURN @pa*pow(x,2) + @pb*x + @pc;
END
");


// Калибровка EC 
mysqli_query($link, "

CREATE FUNCTION `EC`(A1 FLOAT,A2 FLOAT, Temp FLOAT) RETURNS float
BEGIN

IF @ECf is null THEN

set @R1 := (select value from config where parameter='EC_R1' limit 1);
set @Rx1 := (select value from config where parameter='EC_Rx1' limit 1);
set @Rx2 := (select value from config where parameter='EC_RX2' limit 1);
set @Dr := (select value from config where parameter='Dr' limit 1);

set @ec1 := (select value from config where parameter='EC_val_p1' limit 1);
set @ec2 := (select value from config where parameter='EC_val_p2' limit 1);
set @ex1 := (select value from config where parameter='EC_R2_p1' limit 1);
set @ex2 := (select value from config where parameter='EC_R2_p2' limit 1);

set @kt := (select value from config where parameter='EC_kT' limit 1);
set @eckorr := (select value from config where parameter='EC_val_korr' limit 1);

set @eb:=(-log(@ec1/@ec2))/(log(@ex2/@ex1));
set @ea:=pow(@ex1,(-@eb))*@ec1;

set @ECf:=1;
END IF;

set @R2p:=(((-A2*@R1-A2*@Rx1+@R1*@Dr+@Rx1*@Dr)/A2));
set @R2n:=(-(-A1*@R1-A1*@Rx2+@Rx2*@Dr)/(-A1+@Dr));
set @R2:=(@R2p+@R2n)/2;



set @ec:=if(@R2>0,@ea*pow(@R2,@eb),null);

set @ECt:=@ec/(1+@kt*(Temp-25));
RETURN @ECt+@eckorr;
END
");

// Перевод терморезистора 3950 в градусы

mysqli_query($link, "

CREATE FUNCTION `R3950`(Uraw FLOAT, Udcraw FLOAT) RETURNS float
BEGIN

set @B:=3950;
set @t0:=25;
set @Kelvin:=273.15;

set @lnv:=ln( (-Uraw + Udcraw )/Uraw);

RETURN -(-@B * @t0 + @Kelvin * @lnv * @t0 + @lnv * pow(@Kelvin,2) ) / (@B + @lnv * @t0 +  @lnv * @Kelvin);

END

");


// Калибровка терморезистора 
mysqli_query($link, "

CREATE FUNCTION `ftR`(rawT FLOAT) RETURNS float
BEGIN

IF @ftRf is null THEN

set @tR_type:=(select value from config where parameter='tR_type' limit 1);
set @tR_U:=(select value from config where parameter='tR_U' limit 1);
set @tR_DAC:=(select value from config where parameter='tR_DAC' limit 1);
set @tR_B:=(select value from config where parameter='tR_B' limit 1);
set @lkorr:=(select value from config where parameter='tR_val_korr' limit 1);


set @px1:=(select value from config where parameter='tR_raw_p1' limit 1);
set @px2:=(select value from config where parameter='tR_raw_p2' limit 1);
set @px3:=(select value from config where parameter='tR_raw_p3' limit 1);

set @py1:=(select value from config where parameter='tR_val_p1' limit 1);
set @py2:=(select value from config where parameter='tR_val_p2' limit 1);
set @py3:=(select value from config where parameter='tR_val_p3' limit 1);



set @ftRf:=1;
END IF;

set @pa:=-(-@px1*@py3 + @px1*@py2 - @px3*@py2 + @py3*@px2 + @py1*@px3 - @py1*@px2) /  (-pow(@px1,2)*@px3 + pow(@px1,2)*@px2 - @px1*pow(@px2,2) + @px1*pow(@px3,2) - pow(@px3,2)*@px2 + @px3*pow(@px2,2) ); 
set @pb:=( @py3*pow(@px2,2) - pow(@px2,2)*@py1 + pow(@px3,2)*@py1 + @py2*pow(@px1,2) - @py3*pow(@px1,2) - @py2 * pow(@px3,2) ) /  ( (-@px3+@px2) * (@px2*@px3 - @px2*@px1 + pow(@px1,2) - @px3*@px1 ) );
set @pc:=( @py3*pow(@px1,2)*@px2 - @py2*pow(@px1,2)*@px3 - pow(@px2,2)*@px1*@py3 + pow(@px3,2)*@px1*@py2 + pow(@px2,2)*@py1*@px3 - pow(@px3,2)*@py1*@px2 ) /  ( (-@px3+@px2) * (@px2*@px3 - @px2*@px1 + pow(@px1,2) - @px3*@px1 ) );

set @rftr:=@pa*pow(rawT,2) + @pb*rawT + @pc+@lkorr;

# Если датчик цифровой не требует дорасчета
if @tR_type = 'digital' THEN
set @rftr:= rawT+@lkorr;
END IF;

# Аналоговый мост прямое включение терморезистора
if @tR_type = 'reverse' THEN
set @B:=@tR_B;
set @t0:=25;
set @K:=237.15;
set @Uraw:=rawT;
#set @Umax:=@tR_U;
#set @Badc:=@tR_U/@tR_DAC;

#set @r:=ln(-@Uraw*@Badc / (@Uraw*@Badc-@Umax));

set @r:=ln(@Uraw/(-@Uraw+@tR_DAC));
set @rftr:= -(-@B*@t0+@r*@K*@t0+@r*pow(@K,2))/(@B+@r*@t0+@r*@K)+@lkorr;

END IF;

# Аналоговый мост обратное включение терморезистора
if @tR_type = 'direct' THEN
set @B:=@tR_B;
set @t0:=25;
set @K:=237.15;
set @Uraw:=rawT;
#set @Umax:=@tR_U;
#set @Badc:=@tR_U/@tR_DAC;

#set @r:=ln(-(@Uraw*@Badc-@Umax)/(@Uraw*@Badc) );

set  @r:=ln((-@Uraw+@tR_DAC)/@Uraw);
set @rftr:= (@B*@t0-@r*@K*@t0-@r*pow(@K,2))/(@B+@r*@t0+@r*@K)+@lkorr;

END IF;


RETURN @rftr;

END

");

// Калибровка уровня
mysqli_query($link, "

CREATE FUNCTION `intpl`(x FLOAT) RETURNS float
BEGIN

set @x1:=(SELECT cm FROM level 
         where cm <= x
         order by cm desc 
         limit 1 );
set @y1:=(SELECT lev FROM level 
         where cm <= x
         order by cm desc
         limit 1 );
set @x2:=(SELECT cm FROM level 
         where cm > x
         order by cm
         limit 1 );
set @y2:=(SELECT lev FROM level 
         where cm > x
         order by cm
         limit 1 ); 

set @y:=(@y2*@x1-@x2*@y1+x*@y1-x*@y2)/(-@x2+@x1);

RETURN @y;
END
");


// Процедурв фильтрации мини
mysqli_query($link, "

CREATE FUNCTION `levmin`(my_arg FLOAT) RETURNS float
BEGIN

set @levmin:=if (isnull(@levmin),1000,@levmin);
set @Dist_min_k1:=(select value from config where parameter='Dist_min_k1' limit 1);
set @levmin:= if (@levmin-my_arg > @Dist_min_k1,  my_arg, @levmin);
set @levmin:= if (@levmin-my_arg < 0,  my_arg, @levmin);

RETURN (@levmin);
END

");

// Функция расчета pH
mysqli_query($link, "

CREATE FUNCTION `ph`(x float) RETURNS float
BEGIN

IF @phf is null THEN

set @px1:=(select value from config where parameter='pH_raw_p1' limit 1);
set @py1:=(select value from config where parameter='pH_val_p1' limit 1);
set @px2:=(select value from config where parameter='pH_raw_p2' limit 1);
set @py2:=(select value from config where parameter='pH_val_p2' limit 1);
set @px3:=(select value from config where parameter='pH_raw_p3' limit 1);
set @py3:=(select value from config where parameter='pH_val_p3' limit 1);


set @pa:=-(-@px1*@py3 + @px1*@py2 - @px3*@py2 + @py3*@px2 + @py1*@px3 - @py1*@px2) /  (-pow(@px1,2)*@px3 + pow(@px1,2)*@px2 - @px1*pow(@px2,2) + @px1*pow(@px3,2) - pow(@px3,2)*@px2 + @px3*pow(@px2,2) ); 
set @pb:=( @py3*pow(@px2,2) - pow(@px2,2)*@py1 + pow(@px3,2)*@py1 + @py2*pow(@px1,2) - @py3*pow(@px1,2) - @py2 * pow(@px3,2) ) /  ( (-@px3+@px2) * (@px2*@px3 - @px2*@px1 + pow(@px1,2) - @px3*@px1 ) );
set @pc:=( @py3*pow(@px1,2)*@px2 - @py2*pow(@px1,2)*@px3 - pow(@px2,2)*@px1*@py3 + pow(@px3,2)*@px1*@py2 + pow(@px2,2)*@py1*@px3 - pow(@px3,2)*@py1*@px2 ) /  ( (-@px3+@px2) * (@px2*@px3 - @px2*@px1 + pow(@px1,2) - @px3*@px1 ) );


set @phf:=1;
END IF;

RETURN @pa*pow(x,2) + @pb*x + @pc;


END
");

// Функция расчета абсолюютной влажности
mysqli_query($link, "

CREATE FUNCTION `Pa`(tt float, rh float) RETURNS float
BEGIN

RETURN (4.579*pow(2.71828,((17.14*tt)/(235.3+tt))))*rh/100;


END
");


////////////////////////
mysqli_close($link);


?>
