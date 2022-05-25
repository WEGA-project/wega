<?php
include "../db.php";
$my_db="mixer";
$tb="weght";


$con=mysqli_connect($dbhost, $login, $password);

// Create database
$sql="CREATE DATABASE $my_db";
mysqli_query($con,$sql);

// create table
$link=mysqli_connect($dbhost, $login, $password, $my_db);


$query ="create table $tb (dt datetime PRIMARY KEY)";
$result = mysqli_query($link, $query);

mysqli_close($link);


$link=mysqli_connect($dbhost, $login, $password, $my_db);

$query  = explode('&', $_SERVER['QUERY_STRING']);
$var="";
foreach($query as $param)
{
    list($name, $value) = explode('=', $param, 2);
    echo $name,"=",$value;
    mysqli_query($link,"alter table $tb add column $name double");

   $var=$var . "," . $name;
   $val=$val . ",'" . $value."'";
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

echo "<br>";
?>
