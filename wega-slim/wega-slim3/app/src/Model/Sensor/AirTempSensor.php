<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class AirTempSensor extends Sensor
{
    protected $template = "if(alias:AirTemp != 0,alias:AirTemp,null)";
    protected $validateMinField = 'Ev_Min_AirTemp';
    protected $validateMaxField = 'Ev_Max_AirTemp';
    protected $dependAliases = ['AirTemp'];
    protected $round = 2;
    protected $sensorTitle = 'Датчик температуры воздуха';
    protected $valueTitle = 'Температура воздуха';
    protected $units = '°C';
}
