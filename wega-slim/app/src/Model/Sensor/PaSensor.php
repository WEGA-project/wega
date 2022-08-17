<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;
use App\Model\Sensor\AirHumSensor;
use App\Model\Sensor\AirTempSensor;

class PaSensor extends Sensor
{
    protected $template = "Pa(if(alias:AirTemp != 0,alias:AirTemp,null),if(alias:AirHum != 0 and alias:AirHum < 100,alias:AirHum,null))";
    protected $validateMinField = 'Ev_Min_AirHum';
    protected $validateMaxField = 'Ev_Max_AirHum';
    protected $dependAliases = ['AirTemp', 'AirHum'];
    protected $round = 2;
    protected $sensorTitle = 'Датчик влажности воздуха';
    protected $valueTitle = 'Абсолютная влажность воздуха';
    protected $units = ' г/м³';
}
