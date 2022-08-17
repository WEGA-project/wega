<?php

namespace App\Model\Sensor;

use App\Model\Sensor\Sensor;

class DateSensor extends Sensor
{

    protected $validateMaxField = 'Ev_Max_Dt';
    protected $valueTitle = 'Дата и время замера';

    public function getOutDate()
    {
        return strtotime("now") - strtotime($this->getValue());
    }

    public function getValue()
    {
        return $this->getDate();
    }

    public function getStatus()
    {
        return $this->getStatusByRange(
            $this->getOutDate(),
            0,
            $this->config->getVal($this->validateMaxField)
        );
    }
}
