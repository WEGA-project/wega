<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class LuxSensor extends Sensor
{
    protected $template = "fpR(alias:LightRAW)";
    protected $dependAliases = ['LightRAW'];
    protected $round = 1;
    protected $sensorTitle = 'Датчик освещенности';
    protected $valueTitle = 'Освещенность';
    protected $units = ' kLux';
}
