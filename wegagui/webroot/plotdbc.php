<?php
//include "menu.php";

//$ns=$_GET['ns'];


//if (empty($_GET['days'])){$_GET['days']="-0 days";}
//if (empty($_GET['wsdt'])){$_GET['wsdt']=date("Y-m-d",strtotime($_GET['days']))." 00:00:00";}
//if (empty($_GET['wpdt'])){$_GET['wpdt']=date("Y-m-d")." 23:59:59";}
//if (empty($_GET['limit'])){$_GET['limit']="100000";}

//include "../config/".$ns.".conf.php";
//include version.php;
//$version="123";
//$version=date("d M Y H:i:s", filemtime('../../.git/index'));

//$wsdt=$_GET['wsdt'];
//$wpdt=$_GET['wpdt'];
//$limit=$_GET['limit'];

//$stfind="?ns=".$ns."&wsdt=".$wsdt."&wpdt=".$wpdt;

//include "../config/".$ns.".conf.php";

//echo "<h1>".$namesys;
//echo "</h1>";
//echo $comment;
//echo "<br>";


//include "datetime.php";


// Подключаемся к базе
$link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");

if (!$link) {
    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}

//$cl=$_GET['cl'];

$strSQL ="select 

dt,												# 1
".$cl."

from $tb 
where dt  >  '".$wsdt."'
 and  dt  <  '".$wpdt."'
order by dt";



// Выполняем запрос
$rs=mysqli_query($link, $strSQL);
$numb=mysqli_num_rows($rs);
mysqli_data_seek($rs,$numb-1);
$row=mysqli_fetch_row($rs);
mysqli_data_seek($rs,0);




echo "<br><table border='1'>";


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

$text='
set terminal png size 1900,700
set output "'.$gimg.'"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 1,1
set lmargin 10
set rmargin 10
set y2label
set xrange ["'.$wsdt.'" : "'.$wpdt.'"]



plot    \
	"'.$csv.'" using 1:2 w l title "'.$cl.'", \
';

fwrite($handler, $text);
fclose($handler);

$err=shell_exec('cat '.$gnups.'|gnuplot');
echo $err;

echo '<img src="'.$img.'" alt="альтернативный текст">';
shell_exec('rm '.$gnups);





?>

