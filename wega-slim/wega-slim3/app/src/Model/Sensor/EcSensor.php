<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;
use App\Model\Sensor\EcTempSensor;
use App\Model\Sensor\DateSensor;

class EcSensor extends Sensor
{
    protected $template = "EC(cnf:A1,cnf:A2,ftR(alias:ECtempRAW))";
    protected $validateMinField = 'Ev_Min_EC';
    protected $validateMaxField = 'Ev_Max_EC';
    protected $dependAliases = ['A1', 'A2'];
    protected $round = 3;
    protected $sensorTitle = 'Датчик температуры раствора в баке';
    protected $valueTitle = 'Удельная электропроводность ЕС';
    protected $units = ' mS/cm';
}
