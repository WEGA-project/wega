<?php

$auth="adab637320e5c47624cdd15169276981";

if ($_GET['auth'] == $auth ) {

if ($_GET['db']){
$my_db=$_GET['db'];
include "../db.php";
$tb="sens";

// Create database
$link=mysqli_connect($dbhost, $login, $password);
mysqli_query($link,"CREATE DATABASE $my_db");
mysqli_close($link);

// create table
$link=mysqli_connect($dbhost, $login, $password, $my_db);
$query ="create table $tb (dt datetime PRIMARY KEY)";
$result = mysqli_query($link, $query);



$query  = explode('&', $_SERVER['QUERY_STRING']);

$var="";
foreach($query as $param)
{
    list($name, $value) = explode('=', $param, 2);
  if ($name  != "db" and $name !="auth"){
      echo $name,"=",$value;
      mysqli_query($link,"alter table $tb add column $name double");
      $var=$var . "," . $name;
      $val=$val . ",'" . $value."'";
  }
}
$dt=date('Y.m.d H:i:s');

echo "<br>";
$var=substr($var, 1);
$var = "(dt," . $var . ")";
echo $var;
echo "<br>";
$val=substr($val, 1);
$val = "('$dt'," . $val . ")";
echo $val;

mysqli_query($link,"insert into $tb $var values $val");
mysqli_close($link);

echo "<br>";
}
else
{
echo "Error: DB not set";
}
}
else
{
echo "Access denied!";
}
?>
