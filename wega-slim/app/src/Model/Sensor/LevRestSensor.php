<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class LevRestSensor extends Sensor
{
    protected $template = "intpl(levmin(alias:Dst)) + alias:LevelAdd";
    protected $dependAliases = ['Dst'];
    protected $round = 1;
    protected $sensorTitle = 'Датчик уровня раствора';
    protected $valueTitle = 'Общий остаток раствора в системе';
    protected $units = ' литр.';
  
}
