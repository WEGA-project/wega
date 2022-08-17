<?php

namespace App\Model;

use Illuminate\Database\Eloquent\Model;




class Base extends Model
{
    public function __construct($connection = false, array $attributes = array())
    {
        parent::__construct($attributes);

        if ($connection) {
            $this->setConnection($connection);
        }
    }
}
