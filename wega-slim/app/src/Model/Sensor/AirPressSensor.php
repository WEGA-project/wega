<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class AirPressSensor extends Sensor
{
    protected $template = "if(alias:AirPress != 0,alias:AirPress,null)";
    protected $validateMinField = 'Ev_Max_AirPress';
    protected $validateMaxField = 'Ev_Min_AirPress';
    protected $dependAliases = ['AirPress'];
    protected $round = 2;
    protected $sensorTitle = 'Датчик давления';
    protected $valueTitle = 'Давление воздуха';
    protected $units = ' мм. рт. ст.';
}
