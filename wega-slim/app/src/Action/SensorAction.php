<?php

namespace App\Action;

use Slim\Http\Request;
use Slim\Http\Response;


// use App\Action\DeviceBaseAction;
// use App\Model\Sensor\AirTempSensor;
// use App\Model\Sensor\AirHumSensor;
// use App\Model\Sensor\PaSensor;
// use App\Model\Sensor\AirPressSensor;
// use App\Model\Sensor\RootTempSensor;
// use App\Model\Sensor\EcTempSensor;
// use App\Model\Sensor\EcSensor;
// use App\Model\Sensor\DateSensor;
// use App\Model\Sensor\PhSensor;
// use App\Model\Sensor\LuxSensor;
// use App\Model\Sensor\Co2Sensor;
// use App\Model\Sensor\LevSensor;
// use App\Model\Sensor\LevRestSensor;
use Illuminate\Support\Str;
use \Slim\Exception\NotFoundException;

final class SensorAction extends DeviceBaseAction
{
    protected function onRequest(Request $request, Response $response, $args)
    {

        $sensorClassName = $request->getAttribute('sensor_class');
        $sensor = new $sensorClassName($args['device']);
        $current = $sensor->getRendered();
        // print_r('<br>');
        // $rsp  = $sensor->getValueList();

        // foreach ($rsp as $row) {
        //     var_dump(str_replace(' ', '-', $row['dt']));
        //     var_dump('___');
        //     var_dump($row['value']);

        //     print_r("<br >");
        // }

        $this->view->render($response, 'pages/sensor.twig', [
            "sens_title" => $sensor->getValueTitle() . "($current)",
            "sensor_instance" => $sensor
        ]);

        return $response;
    }
}
