<?php

namespace App\Middleware;

use App\Model\Device;
use \Slim\Exception\NotFoundException;
use App\Model\Config;
use Illuminate\Support\Str;

final class SensorLoad
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

        $sensorClassName = "App\Model\Sensor\\" . Str::ucfirst(Str::camel($arguments['sensor']));

        if (!class_exists($sensorClassName) || !$arguments['device']) {
            throw new NotFoundException($request, $response);
        }

        $request = $request->withAttribute('sensor_class', $sensorClassName);
        $response = $next($request, $response);
        return $response;
    }
}
