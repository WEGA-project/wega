<?php
include "menu.php";
$ns=$_GET['ns'];



if ( $_GET['ns'] ){

$cm=$_GET['cm'];
$lev=$_GET['lev'];

include "../config/".$ns.".conf.php";
echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";
echo "<br>";
echo "<h2>Калибровка уровня</h2>";

echo "Таблица калибровки (RAW уровня, Объем в литрах)<br>";

$tb="level";



$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");

// Добавляем
if ( $_GET['add'] == 'add' ) {
mysqli_query($link, "CREATE DATABASE $my_db");
mysqli_query($link, "create table $tb (cm double PRIMARY KEY)");
mysqli_query($link, "alter table $tb add column lev double");
mysqli_query($link, "insert into $tb (cm, lev) values ( $cm, $lev )");
}

// Удаляем
if ( $_GET['del'] == 'del' ) {
mysqli_query($link, "delete from $tb where cm=$cm");
}

// Редактируем
if ( $_GET['edit'] == 'edit' ) {
mysqli_query($link, "update $tb set lev=$lev where cm=$cm");
}



$strSQL ="select * from level order by cm";


// Выполняем запрос
$rs=mysqli_query($link, $strSQL);



echo "<table border='1'>";




// Извлекаем значения и формируем таблицу результатов
while($id=mysqli_fetch_row($rs))
        {echo " 
           <form>
              <form action='' method='get'>
                   <input type='text' name='cm' value=".$id[0].">
                   <input type='text' name='lev' value=".$id[1].">
                   <input type='hidden' name='ns' value=$ns>
              <input type='submit' value='edit' name='edit'>
              <input type='submit' value='del' name='del'>
           </form>
          <br>";


        }

// Параметры RAW
echo "<br>";

$id=mysqli_fetch_row(mysqli_query($link, "select $dist,intpl($dist) from sens order by dt desc limit 1"));
$raw=$id[0];
$intpl_raw=$id[1];
echo "Текущее значение RAW: ".$dist." = ".$raw;
echo "<br>";
echo "Интерполированное текущее значение объема: ".round($intpl_raw,3)." Литр.";
echo "<br>";


// Форма добавления
echo "<br>Добавить точку интерполяции<br>
            <form action='' method='get'>
                   <input type='text' name='cm' value=$raw>
                   <input type='text' name='lev' value=''>
                   <input type='hidden' name='ns' value=$ns>
              <input type='submit' value='add' name='add'>
            </form>
      <br>
";



mysqli_close($link);


// Процедурв интерполяции
$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");
$strSQL ="
CREATE FUNCTION `intpl`(x FLOAT) RETURNS float
BEGIN

set @x1:=(SELECT cm FROM $tb 
         where cm <= x
         order by cm desc 
         limit 1 );
set @y1:=(SELECT lev FROM $tb 
         where cm <= x
         order by cm desc
         limit 1 );
set @x2:=(SELECT cm FROM $tb 
         where cm > x
         order by cm
         limit 1 );
set @y2:=(SELECT lev FROM $tb 
         where cm > x
         order by cm
         limit 1 ); 

set @y:=(@y2*@x1-@x2*@y1+x*@y1-x*@y2)/(-@x2+@x1);

RETURN @y;
END
";

$rs=mysqli_query($link, $strSQL);

// Процедурв фильтрации мини
$link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");
$strSQL ="
CREATE DEFINER=`root`@`localhost` FUNCTION `levmin`(my_arg FLOAT) RETURNS float
BEGIN
set @levmin:=if (isnull(@levmin),1000,@levmin);


set @levmin:= if (@levmin-my_arg > 1.6,  my_arg, @levmin);

set @levmin:= if (@levmin-my_arg < 0,  my_arg, @levmin);

RETURN (@levmin-0);
END
";

$rs=mysqli_query($link, $strSQL);


// Рисуем калибровочный график
// составление csv калибровки
$rs=mysqli_query($link, "select cm, lev from $tb order by cm");

$filename=$csv;
$handler = fopen($filename, "w");

while($id=mysqli_fetch_row($rs))
        { 
        for ($x=0; $x<=count($id)-1; $x++) 
                {
		$text= $id[$x].";";
		fwrite($handler, $text);
                }
	fwrite($handler, "\n");
        }

fclose($handler);
$filename=$gnups;
$handler = fopen($filename, "w");


// составление csv уровня
$rs=mysqli_query($link, "select dt,$dist,@a:=intpl($dist),levmin(@a) from sens order by dt desc limit 100");

$csv2="tmp/lev.csv";
$filename=$csv2;
$handler = fopen($filename, "w");

while($id=mysqli_fetch_row($rs))
        { 
        for ($x=0; $x<=count($id)-1; $x++) 
                {
		$text= $id[$x].";";
		fwrite($handler, $text);
                }
	fwrite($handler, "\n");
        }

fclose($handler);
$filename=$gnups;
$handler = fopen($filename, "w");


// рисование gnuplot

$text='
set terminal png size 1400,800
set output "'.$gimg.'"
set datafile separator ";"
set grid
set xlabel "RAW"
set ylabel "Объем в литрах"
set multiplot layout 2,2

set label "Текущий уровень" at '.$raw.','.$intpl_raw.' point pointtype 7

plot    \
	"'.$csv.'" using 1:2 w l title "", \
	"'.$csv.'" using 1:2 w p pt 6 title "", \

set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set xlabel "Дата/Время"
set ylabel "RAW"

plot    \
	"'.$csv2.'" using 1:2 w l title "", \

set grid ytics mytics
set mytics 2

set ylabel "Объем в литрах"
plot    \
	"'.$csv2.'" using 1:3 w l title "", \
	"'.$csv2.'" using 1:4 w l title "", \

set grid ytics mytics
set mytics 2

set ylabel "Объем в литрах"
plot    \
	"'.$csv2.'" using 1:4 w l title "", \




';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="график">';



mysqli_close($link);

}
else
{
echo "Не выбрана система";
}


?>

