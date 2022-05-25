<?php
  if ( $_GET['act'] == 'set' )
  {
    $ns=$_GET['ns'];
    include "sqvar.php";
    $EC_Rx1_comment = $_GET['EC_Rx1_comment'];
    $EC_Rx2_comment = $_GET['EC_Rx2_comment'];
    setdbval($ns,"EC_Rx1",$_GET['set_rx1'],$EC_Rx1_comment);
    setdbval($ns,"EC_Rx2",$_GET['set_rx2'],$EC_Rx2_comment);
    header("Location: ".$_GET['return_url']);
  }

include "menu.php";

if ( $_GET['ns'] )
{
  include "sqvar.php";
  echo "<h1>".$namesys;
  echo "</h1>";
  echo $comment;
  echo "<br>";
  echo "<h2>База ".$my_db."</h2>";
  echo "<br>";
  include "datetime.php";
  // Подключаемся к базе
  $link = mysqli_connect("$dbhost", "$login", "$password", "$my_db");
  if (!$link) {
    echo "Ошибка: Невозможно установить соединение с MySQL." . PHP_EOL;
    echo "Код ошибки errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Текст ошибки error: " . mysqli_connect_error() . PHP_EOL;
    exit;
  }
  $strSQL ="select * from $tb where dt  >  '".$wsdt."' and  dt  <  '".$wpdt."' order by dt limit $limit";

  // Выполняем запрос
  $rs=mysqli_query($link, $strSQL);

  while( $row = mysqli_fetch_assoc( $rs)){
    $dataset[] = $row; // Inside while loop
  }

  $r1 = floatval(dbval("EC_R1",$ns));
  $dr = floatval(dbval("Dr",$ns));

  $delta = 0;
  $precisions = array(100, 10, 1);
  $min_delta = 100000000000;
  $best_rx1 = 0;
  $best_rx2 = 0;

  foreach($precisions as $precision)
  {
    $rx1_min = -20*$precision+$best_rx1;
    $rx1_max = 20*$precision+$best_rx1;
    $rx2_min = -20*$precision+$best_rx2;
    $rx2_max = 20*$precision+$best_rx2;
    for($rx1 = $rx1_min; $rx1 <= $rx1_max; $rx1=$rx1+$precision)
    {
      for($rx2 = $rx2_min; $rx2 <= $rx2_max; $rx2=$rx2+$precision)
      {
        $delta = 0;
        foreach($dataset as $row)
        {
          $a1 = $row['Ap'];
          $a2 = $row['An'];
          $R2p = -1 * (-1 * $a1 * $r1 - $a1 * $rx2 + $rx2 * $dr) / (-1 * $a1 + $dr);
          $R2n = (-1 * $a2 * $r1 - $a2 * $rx1 + $r1 * $dr + $rx1 * $dr) / $a2;
          $delta += abs($R2p - $R2n);
        }
        if($delta < $min_delta)
        {
          $min_delta = $delta;
          $best_rx1 = $rx1;
          $best_rx2 = $rx2;
        }
      }
    }
  }
  //echo $_SERVER['HTTP_REFERER'];
  //$return_url = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
  $return_url = $_SERVER['HTTP_REFERER'];
  $return_url = str_replace("rx1rx2.php", "CalibrateEC.php", $return_url);
  echo "<form><form action='' method='get'>";
  echo "<input type='hidden' name='ns' value='".$ns."'>";
  echo "<input type='hidden' name='return_url' value='".$return_url."'>";
  echo "<input type='hidden' name='set_rx1' value='".$best_rx1."'>";
  echo "<input type='hidden' name='set_rx2' value='".$best_rx2."'>";
  echo "<input type='hidden' name='EC_Rx1_comment' value='".dbcomment("EC_Rx1",$ns)."'>";
  echo "<input type='hidden' name='EC_Rx2_comment' value='".dbcomment("EC_Rx2",$ns)."'>";
  echo "<input type='hidden' name='wsdt' value='".$_GET['wsdt']."'>";
  echo "<input type='hidden' name='wpdt' value='".$_GET['wpdt']."'>";
  echo "<p>EC_Rx1: ".$best_rx1;
  echo "<p>EC_Rx2: ".$best_rx2;
  echo "<p><input type='submit' value='set' name='act'>";
}
else
{
  echo "Не выбрана система";
}
?>
