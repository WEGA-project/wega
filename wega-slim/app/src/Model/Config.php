<?php

namespace App\Model;

use App\Model\Base;


final class Config extends Base
{
    // public function __construct($connection, array $attributes = array())
    // {

    //     parent::__construct($attributes);

    //     $this->setConnection($connection);
    // }
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'config';
    // protected $connection = 'main';

    public function getVal($param)
    {
        $resp = $this->getByParam($param);

        $val = ($resp) ? $resp->value : $resp;

        return $val === 'null' ? false : $val;
    }

    public function getComment($param)
    {
        $resp = $this->getByParam($param);

        return ($resp) ? $resp->comment : $resp;
    }

    public function getByParam($param)
    {
        try {
            $rsp = $this->newQuery()->where('parameter', $param)->take(1)->get()->first();
        } catch (\Exception $e) {
            $rsp = false;
        }

        return $rsp;
    }
}
