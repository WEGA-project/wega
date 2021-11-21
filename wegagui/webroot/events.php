<?php
include "menu.php";
if ( $_GET['ns'] ){

    include "sqvar.php";
    include "tstatus.php";  
    echo "<br>";
    

    echo "<h3>Общие параметры уведомлений</h3>";
    pedit("Ev_Max_Dt",$ns,3600,"Максимальная продолжительность отсуствия данных в секундах");
    
    echo "<br>";
    
    echo "<h3>Параметры пороговых и критических значений</h3>";

    pedit("Ev_Max_AirTemp",$ns,35,"Максимальная темература воздуха");
    pedit("Ev_Min_AirTemp",$ns,10,"Минимальная темература воздуха");
    pedit("Ev_Max_WaterTemp",$ns,28,"Максимальная темература раствора");
    pedit("Ev_Min_WaterTemp",$ns,15,"Минимальная темература раствора");
    pedit("Ev_Max_RootTemp",$ns,28,"Максимальная темература корней");
    pedit("Ev_Min_RootTemp",$ns,15,"Минимальная темература корней");
    pedit("Ev_Max_AirHum",$ns,80,"Максимальная влажность воздуха");
    pedit("Ev_Min_AirHum",$ns,10,"Минимальная влажность воздуха");
    pedit("Ev_Min_Level",$ns,10,"Минимальный остаток раствора в баке для уведомления о доливе");
    pedit("Ev_Crit_Level",$ns,1,"Критический остаток раствора в баке для уведомления о доливе");
    pedit("Ev_Max_EC",$ns,3,"Максимальный ЕС");
    pedit("Ev_Min_EC",$ns,0.5,"Минимальный ЕС");
    pedit("Ev_Max_pH",$ns,7,"Максимальный pH");
    pedit("Ev_Min_pH",$ns,5,"Минимальный pH");
    pedit("Ev_Max_CO2",$ns,3000,"Максимальный CO2");
    pedit("Ev_Min_CO2",$ns,300,"Минимальный CO2");

    echo "<br>";
    
    echo "<h3>Настройки телеграм</h3>";
    echo "<a href=https://t.me/BotFather>Регистрация бота</a><br><br>";

        

    pedit("Ev_token",$ns,"","Токен");
    pedit("Ev_chat_id",$ns,"","Идентификатор чата");
    echo "<br><a href=telegrambot.php?ns=".$ns.">Проверить входящие</a>";
    echo "<br>";
    
    echo "<br><a href=send.php?ns=".$ns.">Проверить отправку</a>";
echo "<br>";
 
}

else
{
echo "Не выбрана система";
}

?>