<?php

namespace App\Action;

use Slim\Http\Request;
use Slim\Http\Response;

use App\Action\DeviceBaseAction;
use App\Model\Sensor\AirTempSensor;
use App\Model\Sensor\AirHumSensor;
use App\Model\Sensor\PaSensor;
use App\Model\Sensor\AirPressSensor;
use App\Model\Sensor\RootTempSensor;
use App\Model\Sensor\EcTempSensor;
use App\Model\Sensor\EcSensor;
use App\Model\Sensor\DateSensor;
use App\Model\Sensor\PhSensor;
use App\Model\Sensor\LuxSensor;
use App\Model\Sensor\Co2Sensor;
use App\Model\Sensor\LevSensor;
use App\Model\Sensor\LevRestSensor;

final class StatusAction extends DeviceBaseAction
{
    protected function onRequest(Request $request, Response $response, $args)
    {

        $sensors_fields = [];
        $sensors = [
            new DateSensor,
            new AirHumSensor,
            new PaSensor,
            new AirTempSensor,
            new AirPressSensor,
            new RootTempSensor,
            new EcTempSensor,
            new EcSensor,
            new PhSensor,
            new LuxSensor,
            new Co2Sensor,
            new LevSensor,
            new LevRestSensor,
        ];

        foreach ($sensors as $sensor) {
            $sensor->__construct($args['device']);
            $sensors_fields[] = [
                "instance" => $sensor,
                "configured" => $sensor->isConfigured(),
                "title" => $sensor->hasData() ? $sensor->getValueTitle() : $sensor->getSensorTitle(),
                "rendered" => $sensor->getRendered(),
                "status" => $sensor->getStatus(),
                "changes" => $sensor->getChnages()
            ];
        }

        $this->view->render($response, 'pages/status.twig', [
            "sensors" =>  $sensors_fields,
        ]);

        return $response;
    }
}
