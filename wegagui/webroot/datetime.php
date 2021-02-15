<?php
echo '<h2>Период анализа</h2>';


echo '
<form action="" method="get">
 <input type="hidden" name="ns" value="'.$_GET['ns'].'"/>
 Дата с: <input type="text" name="wsdt" value="'.$_GET['wsdt'].'"/>
 по: <input type="text" name="wpdt" value="'.$_GET['wpdt'].'"/>
 <input type="submit" value="Задать"/>
</form>';
echo '<a href=?ns='.$ns.'&days=-0%20days>За сегодя </a>';
echo '<a href=?ns='.$ns.'&days=-1%20days>Со вчера</a>';
echo '  <a href=?ns='.$ns.'&days=-2%20days>2 дня</a>';
echo '  <a href=?ns='.$ns.'&days=-7%20days>Неделя</a>';
echo '  <a href=?ns='.$ns.'&days=-14%20days>2 недели</a>';
echo '  <a href=?ns='.$ns.'&days=-1%20month>за месяц</a>';
?>
