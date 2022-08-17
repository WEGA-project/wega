<?php

namespace App\Model;

use Illuminate\Database\Eloquent\Model;



final class Device extends Model
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
    protected $table = 'devices';
    protected $connection = 'main';

    public static function isExist($name)
    {
        return static::where('db', $name)
            ->take(1)
            ->get()
            ->first();
    }
}
