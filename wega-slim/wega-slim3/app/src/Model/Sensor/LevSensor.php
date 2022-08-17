<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class LevSensor extends Sensor
{
    protected $template = "intpl(levmin(alias:Dst))";
    protected $validateMinField = 'Ev_Min_Level';
    // protected $validateMaxField = 'Ev_Max_EC';
    protected $dependAliases = ['Dst'];
    protected $round = 1;
    protected $sensorTitle = 'Датчик уровня раствора';
    protected $valueTitle = 'Уровень раствора в баке';
    protected $units = ' литр.';

    protected function getMaxRange()
    {
        $full = floatval($this->config->getVal('LevelFull'));
        $La = $this->config->getVal('La');
        return $full - $La;
    }

    public function getStatus()
    {
        $status = parent::getStatus();
        $crit = floatval($this->config->getVal('Ev_Crit_Level'));

        if ($this->getValue() < $crit) {
            $status['valid'] = false;
            $status['info'] = 'fail';
        }

        return   $status;
    }
}
