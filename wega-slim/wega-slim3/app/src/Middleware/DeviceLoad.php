<?php

namespace App\Middleware;

use App\Model\Device;
use \Slim\Exception\NotFoundException;
use App\Model\Config;

final class DeviceLoad
{
    private $container;

    public function __construct($container)
    {
        $this->container = $container;
    }

    public function __invoke($request, $response, $next)
    {



        $route = $request->getAttribute('route');
        $arguments = $route->getArguments();

        if (!Device::isExist($arguments['device'])) {
            throw new NotFoundException($request, $response);
        }

        $cnf = new Config($arguments['device']);
        $name_info = $cnf->getByParam('namesys');

        $view_env = $this->container->get('view')->getEnvironment();
        $view_env->addGlobal('device_db_name', $arguments['device']);
        $view_env->addGlobal('device_name',  $name_info->value);
        $view_env->addGlobal('device_comment', $name_info->comment);

        $response = $next($request, $response);

        return $response;
    }
}
