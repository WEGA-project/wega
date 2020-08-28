<?php
$ns=$_GET['ns'];



if (empty($_GET['days'])){$_GET['days']="-0 days";}
if (empty($_GET['wsdt'])){$_GET['wsdt']=date("Y-m-d",strtotime($_GET['days']))." 00:00:00";}
if (empty($_GET['wpdt'])){$_GET['wpdt']=date("Y-m-d")." 23:59:59";}
if (empty($_GET['limit'])){$_GET['limit']="100000";}

include "../config/".$ns.".conf.php";


$wsdt=$_GET['wsdt'];
$wpdt=$_GET['wpdt'];
$limit=$_GET['limit'];

echo "<h1>".$namesys;
echo "</h1>";
echo $comment;
echo "<br>";


echo '
<!DOCTYPE html>
<html>
  <head>
    <title>WEGA '.$namesys.'</title>    
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<link href="css/dopstyle.css" rel="stylesheet" media="screen">		
  </head>
  <body>
	<div class="top-menu">
		<ul>
			<li>
				Выбор системы</a>
                                <ul>';

//echo "<li><a href="finderr.php">Недоступныхeee</a></li>";
foreach (glob("../config/*.conf.php") as $filename) {
    //echo "$filename размер " . filesize($filename) . "<br>";
    include $filename;
    $fl=explode("/", $filename);
    $nm=explode(".", $fl[2]);
    $cname=$nm[0];
    //echo "<br>".$cname."<br>";
    echo "<li><a href=rep.php?ns=".$cname.">". $namesys ."</a></li>";

}

echo '



                                </ul>
                        </li>

			<li>Анализ</a>
				<ul>
					<li><a href="temp.php?ns='.$ns.'">Температура</a></li>
					<li><a href="subnet-timeout.php">Влажность</a></li>
					<li><a href="subnet-timeout.php">Влажность</a></li>
					<li><a href="subnet-timeout.php">Освещенность</a></li>
					<li><a href="subnet-timeout.php">EC</a></li>
					<li><a href="subnet-timeout.php">pH</a></li>
				</ul>

			<li>
				Параметры</a>
				<ul>
					<li><a href="subnet.edit.php">Калибровка сенсоров</a></li>
					<li><a href="subnet-timeout.php">Уведомления</a></li>
				</ul>
			</li>
		</ul>
	</div>
    
  </body>
</html>

';



//echo "<a href=subdev.php>Подразделения</a><br>";
//echo "<a href=subnet.php>Подсети</a><br>";
//echo "<a href=find.php>Поиск</a><br><br>";
?>

