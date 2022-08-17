<?php

namespace App\Action;

use Slim\Http\Request;
use Slim\Http\Response;

use App\Action\BaseAction;
use App\Model\Device;
use App\Model\Config;
use App\Model\Sensor;

class DeviceBaseAction extends BaseAction
{

    // protected $name;
    // protected $comment;
    // protected $cnf_instance;
    public function __invoke(Request $request, Response $response, $args)
    {

        // $this->cnf_instance = new Config($args['device']);
        // $name_info = $this->cnf_instance->getByParam('namesys');
        // $this->name = $name_info->value;
        // $this->comment = $name_info->comment;

        parent::__invoke($request,  $response, $args);
    }
}
