<?php
echo "<table border='1'>";
// Вытаскиваем имена полей и формируем заголовок таблицы результатов
echo "<tr>";
while ($property = mysqli_fetch_field($rs)) 
        { 
        echo "<th>";
        echo $property->name;
        echo "</th>"; 
        }
echo "</td></tr>";
// Извлекаем значения и формируем таблицу результатов
while($id=mysqli_fetch_row($rs))
        { 
        echo "<tr>";
        for ($x=0; $x<=count($id)-1; $x++) 
                {
                echo "<td>".$id[$x];
                }
        echo "</td>";
        }
echo "</td></table>";

?>
