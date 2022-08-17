<?php

namespace App\Action;

// use Slim\Views\Twig;
// use Psr\Log\LoggerInterface;

use Slim\Http\Request;
use Slim\Http\Response;
// use Illuminate\Database\Query\Builder;
use Psr\Container\ContainerInterface;
use App\Action\BaseAction;

use App\Model\Device;
use App\Model\Config;
use App\Model\Sensor\AirTempSensor;
use App\Model\Sensor\AirHumSensor;
use App\Model\Sensor\EcSensor;
use App\Model\Sensor\DateSensor;
use App\Model\Sensor\PhSensor;
use App\Model\Sensor\LevSensor;

final class HomeAction extends BaseAction
{

    public function onRequest(Request $request, Response $response, $args)
    {

        $devices = Device::all();
        $air_temp_sensor = new AirTempSensor();
        $air_hum_sensor = new AirHumSensor();
        $ec_sensor = new EcSensor();
        $date_sensor = new DateSensor();
        $ph_sensor = new PhSensor();
        $lev_sensor = new LevSensor();
        $cnf_instance = new Config();

        $rsp = [];
        foreach ($devices as $device) {

            $cnf_instance->__construct($device->db);
            $air_temp_sensor->__construct($device->db);
            $air_hum_sensor->__construct($device->db);
            $ec_sensor->__construct($device->db);
            $date_sensor->__construct($device->db);
            $ph_sensor->__construct($device->db);
            $lev_sensor->__construct($device->db);

            $name = $cnf_instance->getByParam('namesys');
            $rsp[] = [
                "db" => $device->db,
                "namesys" => $name->value,
                "comment" => $name->comment,
                "name" => $device->name,
                "air_temp" => $air_temp_sensor->getValue(),
                "air_hum" => $air_hum_sensor->getValue(),
                "ec" => $ec_sensor->getValue(),
                "ph" => $ph_sensor->getValue(),
                "lev" => $lev_sensor->getValue(),
                "date" => $date_sensor->getValue()
            ];
        }

        $this->view->render($response, 'pages/home.twig', [
            'devices' =>  $rsp
        ]);

        // $response->getBody()->write("hello");
        return $response;
    }
}
