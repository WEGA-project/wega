<?php
echo '<h2>Период анализа</h2>';

echo '<form action="" method="get">';
echo ' <input type="hidden" name="ns" value="'.$_GET['ns'].'"/>';
if ($cl){echo ' <input type="hidden" name="cl" value="'.$cl.'"/>';}
echo ' Дата с: <input type="text" name="wsdt" value="'.$_GET['wsdt'].'"/>';
echo ' по: <input type="text" name="wpdt" value="'.$_GET['wpdt'].'"/>';
echo ' <input type="submit" value="Задать"/>';
echo '</form>';
echo '<a href=?ns='.$ns.'&days=-0%20days>За сегодя </a>';
echo '<a href=?ns='.$ns.'&days=-1%20days>Со вчера</a>';
echo '  <a href=?ns='.$ns.'&days=-2%20days>2 дня</a>';
echo '  <a href=?ns='.$ns.'&days=-7%20days>Неделя</a>';
echo '  <a href=?ns='.$ns.'&days=-14%20days>2 недели</a>';
echo '  <a href=?ns='.$ns.'&days=-1%20month>за месяц</a>';
?>
