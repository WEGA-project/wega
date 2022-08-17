<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class PhSensor extends Sensor
{
    protected $template = "ph(alias:pHraw)";
    protected $validateMinField = 'Ev_Min_pH';
    protected $validateMaxField = 'Ev_Max_pH';
    protected $dependAliases = ['pHraw'];
    protected $round = 3;
    protected $sensorTitle = 'Датчик pH';
    protected $valueTitle = 'Водородный показатель pH';
    protected $units = '';
}
