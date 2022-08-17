<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class Co2Sensor extends Sensor
{
    protected $template = "alias:CO2";
    protected $validateMinField = 'Ev_Min_CO2';
    protected $validateMaxField = 'Ev_Max_CO2';
    protected $dependAliases = ['CO2'];
    protected $round = 3;
    protected $sensorTitle = 'Датчик CO2';
    protected $valueTitle = 'Уровень CO2';
    protected $units = ' ppm';
}
