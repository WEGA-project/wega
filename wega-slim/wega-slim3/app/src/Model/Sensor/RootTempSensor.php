<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class RootTempSensor extends Sensor
{
    protected $template = "if(alias:RootTemp != -127 and alias:RootTemp != 85,alias:RootTemp,null)";
    protected $validateMinField = 'Ev_Min_RootTemp';
    protected $validateMaxField = 'Ev_Max_RootTemp';
    protected $dependAliases = ['RootTemp'];
    protected $round = 2;
    protected $sensorTitle = 'Датчик температуры корней';
    protected $valueTitle = 'Температура в зоне корней';
    protected $units = '°C';
}
