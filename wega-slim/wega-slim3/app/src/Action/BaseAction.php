<?php

namespace App\Action;

use Slim\Http\Request;
use Slim\Http\Response;
use Psr\Container\ContainerInterface;
// use App\Model\Device;
// use App\Model\Config;
// use App\Model\Sensor;

class BaseAction
{
    protected $view;
    // protected $logger;
    protected $container;

    public function __construct(ContainerInterface $container)
    {
        $this->container = $container;
        $this->view = $this->container->get('view');
        // $this->logger = $this->container->get('logger');
    }

    public function __invoke(Request $request, Response $response, $args)
    {

        return $response = $this->onRequest($request,  $response, $args);
    }

    protected function onRequest(Request $request, Response $response, $args)
    {
        return $response;
    }
}
