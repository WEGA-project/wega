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
   dbpsel($ns,$parm);
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
set title "'.$name.'"
set ylabel "'.$dimens.'"
plot    \
	"'.$csv.'" using 1:2 w l title "'.$nplot1.'", \
    "'.$csv.'" using 1:3 w l title "'.$nplot2.'", \
    "'.$csv.'" using 1:4 w l title "'.$nplot3.'", \
    "'.$csv.'" using 1:5 w l title "'.$nplot4.'", \
    "'.$csv.'" using 1:6 w l title "'.$nplot5.'", \
    ';

fwrite($handler, $text);
fclose($handler);
$err=shell_exec('cat '.$gnups.'|gnuplot');
echo "<br>";
echo '<img src="'.$img.'" alt="альтернативный текст">';
}



?>
