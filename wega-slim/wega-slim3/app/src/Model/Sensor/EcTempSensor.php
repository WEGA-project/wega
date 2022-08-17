<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class EcTempSensor extends Sensor
{
    protected $template = "ftR(alias:ECtempRAW)";
    protected $validateMinField = 'Ev_Min_WaterTemp';
    protected $validateMaxField = 'Ev_Max_WaterTemp';
    protected $dependAliases = ['ECtempRAW'];
    protected $round = 2;
    protected $sensorTitle = 'Датчик температуры раствора в баке';
    protected $valueTitle = 'Температура раствора в баке';
    protected $units = '°C';
}
