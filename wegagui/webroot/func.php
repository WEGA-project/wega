<?php
function dbval($p_name,$ns)
{
   include "../config/".$ns.".conf.php";
   $tb="config";
   $link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");
   $sqlstr="select value from $tb where parameter = '$p_name' limit 1";
   $result=mysqli_query($link, $sqlstr);
   $value = mysqli_fetch_object($result)->value;
   mysqli_close($link);
   return $value;
}

function dbcomment($p_name,$ns)
{
   include "../config/".$ns.".conf.php";
   $tb="config";
   $link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");
   $sqlstr="select comment from $tb where parameter = '$p_name' limit 1";
   $result=mysqli_query($link, $sqlstr);
   $comment = mysqli_fetch_object($result)->comment;
   mysqli_close($link);
   return $comment;
}

function setdbval($ns,$p_name,$p_value,$p_comment)
{
   include "../config/".$ns.".conf.php";
   $link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");

   $tb="config";
   mysqli_query($link, "create table IF NOT EXISTS $tb (parameter varchar(50) PRIMARY KEY) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci");
   mysqli_query($link, "alter table $tb add column value varchar(255) ");
   mysqli_query($link, "alter table $tb add column comment varchar(255) ");
   mysqli_query($link, "insert into $tb (parameter, value, comment) values ( '$p_name', '$p_value', '$p_comment' )" );
   mysqli_query($link, "update $tb set value = '$p_value', comment = '$p_comment'  where parameter ='$p_name' ");
   mysqli_close($link);
}

function sensval($p_name,$ns)
{
   include "../config/".$ns.".conf.php";
   $tb="sens";
   $link=mysqli_connect("$dbhost", "$login", "$password", "$my_db");
   $sqlstr="select ".$p_name." from sens order by dt desc  limit 1";
   $result=mysqli_query($link, $sqlstr);
   return mysqli_fetch_object($result)->$p_name;
   mysqli_close($link);
}

function vallast($p_name,$sec,$ns)
{
   include "../config/".$ns.".conf.php";
   $tb="sens";
   $link=mysqli_connect("$dbhost", "$login", "$password", "$my_db"); 
   return mysqli_fetch_object(mysqli_query($link, "select ".$p_name." as val,dt as dt from sens order by dt desc  limit 1"));
   mysqli_close($link);
}

function valprev($p_name,$sec,$ns)
{
   include "../config/".$ns.".conf.php";
   $tb="sens";
   $link=mysqli_connect("$dbhost", "$login", "$password", "$my_db"); 
   return mysqli_fetch_object(mysqli_query($link, "select ".$p_name." as val,dt as dt from sens where UNIX_TIMESTAMP(now())-UNIX_TIMESTAMP(dt) > ".$sec." order by dt desc  limit 1"));
   mysqli_close($link);
}

function valpred($p_name,$sec,$ns)
{
   include "../config/".$ns.".conf.php";
   $tb="sens";
   $link=mysqli_connect("$dbhost", "$login", "$password", "$my_db"); 
   return mysqli_fetch_object(mysqli_query($link, "select max(".$p_name.") as valmax,min(".$p_name.") as valmin from sens where UNIX_TIMESTAMP(now())-UNIX_TIMESTAMP(dt) > ".$sec." limit 1"));
   mysqli_close($link);
}

function valdate($p_name,$date,$ns)
{
   include "../config/".$ns.".conf.php";
   $link=mysqli_connect("$dbhost", "$login", "$password", "$my_db"); 
   return mysqli_fetch_object(mysqli_query($link, "select ".$p_name." as value,dt as dt from sens where dt > '".$date."' order by dt limit 1"));
   mysqli_close($link);
}


function pedit($str,$ns,$defv,$defc)
{
   include "../config/".$ns.".conf.php";
   $tb="config";
   $strv=dbval($str,$ns); echo "<a href=setpapam.php?ns=".$ns."&parameter=".$str."> ".$str." </a> = ".$strv." ".dbcomment($str,$ns)."<br>";
   if (dbval($str,$ns)=='') {setdbval($ns,$str,$defv,$defc);}
   mysqli_close($link);

}

function dbpsel($ns,$p,$comment)
{

 include "../config/".$ns.".conf.php";

// Подключаемся к базе
   $link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");
   $strSQL ="select * from $tb order by dt limit 1";
// Выполняем запрос
   $rs=mysqli_query($link, $strSQL);
   $numb=mysqli_num_rows($rs);
   mysqli_data_seek($rs,$numb-1);
   $row=mysqli_fetch_row($rs);
   mysqli_data_seek($rs,0);

   echo "<option selected>".dbval($p,$ns)."</option>";

while ($property = mysqli_fetch_field($rs)) 
        { 
        echo "<option>";
        echo $property->name;
        echo "</option>"; 
        }
echo "<option>null</option>";
}





function form($ns,$parm,$comment)
{
   echo " <form action='' method='get'>";
   echo "   <input type='hidden' name='ns' value='".$ns."'>";
   echo "   <select size='1' name='".$parm."'>";
   dbpsel($ns,$parm,$comment);
   echo $comment;
   echo "   </select>";
   echo "  <input type='submit' value='Задать'>";
   echo " ".$comment. ", имя парамтера: <b>".$parm."</b> ";
   echo "</p></form>";

   if ( $_GET[$parm] )
    { 
    $value="$_GET[$parm]";
    setdbval($ns,$parm,$value,$comment);
    echo "SAVE: ".$parm."=".$_GET[$parm]." ".$comment;
    echo "
     <head>
     <meta http-equiv='Refresh' content='0; URL=".$_SERVER['HTTP_REFERER']."'>
    </head>";
   }
}

function gplotgen($xsize,$ysize,$gimg,$wsdt,$wpdt,$csv,$handler,$text,$gnups,$img,$name,$nplot1,$nplot2,$nplot3,$nplot4,$nplot5,$dimens)
{
global $LimitUP;
global $LimitDOWN; 

$text='
set terminal png size '.$xsize.','.$ysize.'
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
#set yrange [" '.$LimitDOWN.' ":" '.$LimitUP.' "]
#set yrange ['.$LimitDOWN.':'.$LimitUP.']
set title "'.$name.'"
set ylabel "'.$dimens.'"

fmax(x) = '.$LimitUP.'
fmin(x) ='.$LimitDOWN.'

plot    \
	"'.$csv.'" using 1:2 w l title "'.$nplot1.'", \
    "'.$csv.'" using 1:3 w l title "'.$nplot2.'", \
    "'.$csv.'" using 1:4 w l title "'.$nplot3.'", \
    "'.$csv.'" using 1:5 w l title "'.$nplot4.'", \
    "'.$csv.'" using 1:6 w l title "'.$nplot5.'" ';

if($LimitUP != ""){ $text=$text.',fmax(x) w l title ""'; }
if($LimitDOWN != ""){ $text=$text.',fmin(x) w l title ""'; }

//echo $text;
fwrite($handler, $text);
fclose($handler);
$err=shell_exec('cat '.$gnups.'|gnuplot');
echo "<br>";
echo '<img src="'.$img.'" alt="альтернативный текст">';
}

function mixer_banks($pname)
{
include "../../db.php";
$mixerdb="mixer";

$link=mysqli_connect("$dbhost", "$login", "$password", "$mixerdb");
$sqlstr="
select 
   dt as mdt, 
   v as v, 
   vbase as vbase,
   v*ro as ves    
from banks 
   where volume = '".$pname."' 
   order by dt desc 
   limit 1";
$result=mysqli_query($link, $sqlstr);

/* получение ассоциативного массива */
$obj = mysqli_fetch_object($result);
mysqli_close($link);
  $mdt = $obj -> mdt; // Дата установки раствора на миксер
  $v =  $obj -> v; // Объем емкости в мл
  $vname = $obj -> vbase; // Поле содержащее отмеренный вес
  $ves = $obj -> ves; // Вес полной емксти

$link=mysqli_connect("$dbhost", "$login", "$password", "$mixerdb");
$sqlstr="select
    if(sum($vname) is not null,sum($vname),0) as sumves, # Суммарный расход из емкости в граммах
    $ves-if(sum($vname) is not null,sum($vname),0) as remain, # Остаток в емкости в граммах
    ($ves-if(sum($vname) is not null,sum($vname),0))/$ves*100 as procent # Остаток в процентах

from weght 
where dt > '".$mdt."' 
limit 1";

$result=mysqli_query($link, $sqlstr);
$obj = mysqli_fetch_object($result);
mysqli_close($link);
return $obj;
}

function gbar($prcnt,$name){
echo "
<style>
.battery{
  position: relative;
  top: 30px;
  border: 1px solid;
  width: 70px;
  height: 120px;
  margin: 20px;
    margin-bottom: 0px;
  content: '';
  border-radius: 15px;
  line-height: 50px;
  text-align: center;
  text-shadow: white 1px 1px 1px;
     }
.battery::after{
  content: '';
  background: gray;
  position: absolute;
  width: 20px;
  height: 6px;
  top: -10px;
  left: 25px;
}

.low_".$name." {
  background: linear-gradient(0deg, #1ddede ".$prcnt."%, white 0%);
}
.Block{
   position: absolute;
   display: inline;
   margin: 0px;
   padding: 50px 100px;
   
      }
</style>

<body>
    <div class='battery low_".$name."'>".$name."</div>
    
</body>

";

}

function showDate( $date ) // $date --> время в формате Unix time
{
    $stf      = 0;
    $cur_time = time();
    $diff     = $cur_time - $date;
    $seconds = array( 'секунда', 'секунды', 'секунд' );
    $minutes = array( 'минута', 'минуты', 'минут' );
    $hours   = array( 'час', 'часа', 'часов' );
    $days    = array( 'день', 'дня', 'дней' );
    $weeks   = array( 'неделя', 'недели', 'недель' );
    $months  = array( 'месяц', 'месяца', 'месяцев' );
    $years   = array( 'год', 'года', 'лет' );
    $decades = array( 'десятилетие', 'десятилетия', 'десятилетий' );
 
    $phrase = array( $seconds, $minutes, $hours, $days, $weeks, $months, $years, $decades );
    $length = array( 1, 60, 3600, 86400, 604800, 2630880, 31570560, 315705600 );
 
    for ( $i = sizeof( $length ) - 1; ( $i >= 0 ) && ( ( $no = $diff / $length[ $i ] ) <= 1 ); $i -- ) {
        ;
    }
    if ( $i < 0 ) {
        $i = 0;
    }
    $_time = $cur_time - ( $diff % $length[ $i ] );
    $no    = floor( $no );
    $value = sprintf( "%d %s ", $no, getPhrase( $no, $phrase[ $i ] ) );
 
    if ( ( $stf == 1 ) && ( $i >= 1 ) && ( ( $cur_time - $_time ) > 0 ) ) {
        $value .= time_ago( $_time );
    }
 
    return $value;
}
 
function getPhrase( $number, $titles ) {
    $cases = array( 2, 0, 1, 1, 1, 2 );
 
    return $titles[ ( $number % 100 > 4 && $number % 100 < 20 ) ? 2 : $cases[ min( $number % 10, 5 ) ] ];
}

?>
