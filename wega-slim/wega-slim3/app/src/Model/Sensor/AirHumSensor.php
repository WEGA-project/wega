<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class AirHumSensor extends Sensor
{
    protected $template = "if(alias:AirHum != 0 and alias:AirHum < 100,alias:AirHum,null)";
    protected $validateMinField = 'Ev_Min_AirHum';
    protected $validateMaxField = 'Ev_Max_AirHum';
    protected $dependAliases = ['AirHum'];
    protected $round = 1;
    protected $sensorTitle = 'Датчик влажности воздуха';
    protected $valueTitle = 'Относительная влажность воздуха';
    protected $units = ' %';
}
