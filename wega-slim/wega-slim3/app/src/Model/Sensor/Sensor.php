<?php

namespace App\Model\Sensor;

use App\Model\Base;
use App\Model\Config;

class Sensor extends Base
{
    protected $table = 'sens';
    protected $template = '';
    protected $date_template = 'dt';
    protected $changes_range = 60 * 60 * 24 * 1; //one day
    // protected $field;
    protected $validateMinField;
    protected $validateMaxField;
    protected $config;
    protected $dependAliases = []; //what aliases needed for cofigure
    protected $round;
    protected $sensorTitle;
    protected $valueTitle;
    protected $units = '';
    protected $from_seconds = 0; //how old data get
    protected $default_limit = 15000;


    public function __construct($connection = false, array $attributes = array())
    {
        parent::__construct($connection, $attributes);
        $this->config = new Config($connection);
    }

    public function getSensorTitle()
    {
        return  $this->sensorTitle;
    }

    public function getTemplate()
    {
        return  $this->template;
    }

    public function getUnits()
    {
        return  $this->units;
    }

    public function setOldSeconds(int $sec)
    {
        return  $this->from_seconds = (int)$sec;
    }

    public function getValueTitle()
    {
        return  $this->valueTitle;
    }

    public function getValue()
    {
        if ($this->isConfigured()) {
            // var_dump(get_class($this));
            // var_dump($this->getTemplate());
            return $this->getLastOne($this->getTemplate());
        }

        return null;
    }

    public function getValueList()
    {
        if ($this->isConfigured()) {
            return $this->getList($this->getTemplate());
        }

        return [];
    }

    public function getRendered(): string
    {
        $val = $this->getValue();
        if ($val) {
            if (is_int($this->round)) {
                $val = round($val, $this->round);
            }

            if ($this->units) {
                $val .= $this->units;
            }
        }

        return (string) $val ? $val : 'нет данных';
    }

    public function getDate()
    {
        return $this->getLastOne($this->date_template);
    }

    protected function getMaxRange()
    {
        return floatval($this->config->getVal($this->validateMaxField));
    }

    protected function getMinRange()
    {
        return floatval($this->config->getVal($this->validateMinField));
    }

    public function getStatus()
    {
        return $this->getStatusByRange(
            $this->getValue(),
            $this->getMinRange(),
            $this->getMaxRange(),
        );
    }

    public function hasData(): bool
    {
        return (bool)$this->getValue();
    }

    public function isConfigured(): bool
    {
        $valid = true;
        foreach ($this->dependAliases as $alias_name) {

            if (!$this->getAlias($alias_name)) {

                $valid = false;
                break;
            }
        }

        return $valid;
    }

    protected function getAlias($name)
    {
        return $this->config->getVal($name);
    }

    protected function getList(string $template): array
    {

        $select = $this->replaceInTemplate($template);

        if ($select) {

            $query = $this->selectRaw($select)->addSelect('dt');
            return $this->getRows($query);
        }

        return  [];
    }

    protected function getLastOne(string $template)
    {

        $select = $this->replaceInTemplate($template);

        if ($select) {
            $query = $this->selectRaw($select);
            $rsp = $this->getLastRow($query);
            return $rsp ? $rsp['value'] : null;
        }

        return  null;
    }

    protected function getLastRow($query): array
    {
        try {
            $rsp =  $this->getRows($query, 1);

            if ($rsp) {
                // var_dump(array_shift($rsp));
                $rsp = array_shift($rsp);
            }
        } catch (\Exception $e) {
            print_r($e->getMessage());
            $rsp = [];
        }

        return $rsp;
    }

    protected function getRows($query, $count = false): array
    {
        if (!$count) {
            $count = $this->default_limit;
        }
        try {
            $query = $this->addDtRestriction($query);
            $query = $query->take($count);
            $query = $this->addDefaultSort($query);
            $rsp = $query->get()->toArray();
        } catch (\Exception $e) {

            print_r($e->getMessage());
            $rsp = [];
        }

        return $rsp;
    }

    protected function addDtRestriction($query)
    {
        if ($this->from_seconds > 0) {
            $query = $query->whereRaw("UNIX_TIMESTAMP(now())-UNIX_TIMESTAMP(dt) > $this->from_seconds");
        }

        return $query;
    }

    protected function addDefaultSort($query)
    {
        return $query->orderBy('dt', 'desc');
    }

    protected function getStatusByRange($raw_val,  $raw_min,  $raw_max): array
    {
        $rsp = ["valid" => true, "info" => ""];

        $val = $raw_val ? (float)$raw_val : false;
        $min = $raw_val ? (float)$raw_min : false;
        $max = $raw_val ? (float)$raw_max : false;

        if (!$val) {
            $rsp['valid'] = false;
            $rsp['info'] = 'no data';
        } else if ($max && $val >= $max) {
            $rsp['valid'] = false;
            $rsp['info'] = "$val >= $max";
        } else if ($min && $val <= $min) {
            $rsp['valid'] = false;
            $rsp['info'] = "$val <= $min";
        }

        return $rsp;
    }

    public function getChnages()
    {
        $val_last = $this->getValue();
        $dt_last = $this->getDate();
        $this->setOldSeconds($this->changes_range);

        $val_prev = $this->getValue();
        $dt_prev = $this->getDate();
        $this->setOldSeconds(0);

        if (!$val_prev || !$dt_prev || !$val_last || !$dt_last) {
            return false;
        }

        $sec = strtotime($dt_last) - strtotime($dt_prev);

        if ($sec > 0) {
            return round((($val_last - $val_prev) / $sec) * 60 * 60 * 24, 3);
        }

        return 0;
    }

    // protected function getSensValue($field_name, $where = [])
    // {
    //     $query = $this->newQuery();
    //     foreach ($where as $condition) {
    //         $query = $query->where($condition);
    //     }
    //     return $this->getLastField($query, $field_name);
    // }

    // protected function getWithTemplate(string $template)
    // {

    //     $sql = $this->replaceInTemplate($template);

    //     if (!$sql) {
    //         return false;
    //     }

    //     return  $this->getRawValue($sql);
    // }



    // protected function getRawValue($sql_select)
    // {
    //     $query = $this->selectRaw($sql_select);

    //     // foreach ($where as $condition) {
    //     //     $query = $query->where($condition);
    //     // }

    //     return $this->getLastField($query, $sql_select);
    // }

    protected function replaceInTemplate(string $template)
    {
        preg_match_all('/(alias|cnf)\:[a-zA-Z_0-9]*+/', $template, $matches);

        $validated = true;
        $markers = [];

        foreach ($matches[0] as $marker) {
            // print_r($marker);
            if (array_key_exists($marker, $markers)) {
                continue;
            }

            if (strpos($marker, 'alias:') !== false) {
                $val = $this->getAlias(str_replace('alias:', '', $marker));
                if (!$val) {
                    $validated = false;
                    break;
                }
            } else if (strpos($marker, 'cnf:') !== false) {
                $val = $this->config->getVal(str_replace('cnf:', '', $marker));
                // }

                // else if (strpos($marker, 'sens:') !== false) {
                //     $name = str_replace('sens:', '', $marker);

                //     $val = $this->{$name}();
                // } else if (strpos($marker, 'fnc:') !== false) {
                //     // print_r();
                //     $name = str_replace('fnc:', '', $marker);

                //     $val = $this->{$name}();
                // } else if (strpos($marker, 'tpl:') !== false) {
                //     $name = str_replace('tpl:', '', $marker);

                //     if (method_exists($this, $name)) {

                //         $val = $this->replaceInTemplate($this->{$name}());
                //     } else {
                //         $val = $this->replaceInTemplate($this->{$name});
                //     }
            }

            $markers[$marker] =  $val;
        }

        if (!$validated) {
            return '';
        }

        foreach ($markers as $marker => $value) {
            $template = str_replace($marker, $value, $template);
        }

        return "$template as value";
    }

    // private function getWithAlias(string $alias_name, $template = false)
    // {

    //     $alias = $this->getAlias($alias_name);

    //     if (!$alias) {
    //         return false;
    //     }

    //     if ($template) {
    //         $sql = str_replace(':alias', $alias, $template);
    //         $rsp =  $this->getRawValue($sql);
    //     } else {
    //         $rsp = $this->getValue($alias);
    //     }

    //     return $rsp;
    // }
}



// if ($AirHum < $Max_AirHum and $AirHum > $Min_AirHum ) {$AirHum_Status = "Норма";} else {$AirHum_Status = "Проблема";}