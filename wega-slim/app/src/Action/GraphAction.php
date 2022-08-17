<?php

namespace App\Action;

use Slim\Http\Request;
use Slim\Http\Response;

use Gregwar\GnuPlot\GnuPlot;


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

class GnuPlotCustom extends GnuPlot
{
    protected function sendData()
    {
        foreach ($this->values as $index => $data) {
            foreach ($data as $xy) {
                list($x, $y) = $xy;
                $this->sendCommand($x . ';' . $y);
            }
            $this->sendCommand('e');
        }
    }

    protected function sendInit()
    {
        $this->sendCommand('set grid');
        $this->sendCommand('set terminal dumb');
        $this->sendCommand('set datafile separator ";"');

        if ($this->title) {
            $this->sendCommand('set title "' . $this->title . '"');
        }

        if ($this->xlabel) {
            $this->sendCommand('set xlabel "' . $this->xlabel . '"');
        }

        if ($this->timeFormat) {
            $this->sendCommand('set xdata time');
            $this->sendCommand('set timefmt "' . $this->timeFormat . '"');
            // $this->sendCommand('set xtics rotate by 45 offset -6,-3');
            if ($this->timeFormatString) {
                $this->sendCommand('set format x "' . $this->timeFormatString . '"');
            }
        }

        if ($this->ylabel) {
            $this->sendCommand('set ylabel "' . $this->ylabel . '"');
        }

        if ($this->yformat) {
            $this->sendCommand('set format y "' . $this->yformat . '"');
        }

        if ($this->xrange) {
            $this->sendCommand('set xrange [' . $this->xrange[0] . ':' . $this->xrange[1] . ']');
        }

        if ($this->yrange) {
            $this->sendCommand('set yrange [' . $this->yrange[0] . ':' . $this->yrange[1] . ']');
        }

        foreach ($this->labels as $label) {
            $this->sendCommand('set label "' . $label[2] . '" at ' . $label[0] . ', ' . $label[1]);
        }
    }
}
final class GraphAction extends DeviceBaseAction
{
    protected function onRequest(Request $request, Response $response, $args)
    {

        $sensorClassName = $request->getAttribute('sensor_class');
        $sensor = new $sensorClassName($args['device']);
        // print_r($sensor->getRendered());
        // print_r('<br>');
        //2022-08-10 18:17:51
        $items  = $sensor->getValueList();

        $plot = new GnuPlotCustom;



        $image = $plot
            // ->setGraphTitle($sensor->getValueTitle())
            // ->setXLabel('Date')
            ->setYLabel($sensor->getUnits())
            ->setWidth(800)
            ->setHeight(500)
            // ->setYRange(-1, 100)
            ->setXTimeFormat('%Y-%m-%d %H:%M:%S')
            ->setTitle(0, $sensor->getValueTitle())
            ->setTimeFormatString('%d.%m\n%H:%M');
        // ->enableHistogram()

        // $image = $image->push('2022-08-11-18:17:51', 0)
        //     ->push('2022-08-11-18:18:51', 1)
        //     ->push('2022-08-11-18:19:51', 4)
        //     ->push('2022-08-11-18:20:51', 3)
        //     ->push('2022-08-11-18:21:51', 2)
        //     ->push('2022-08-11-18:22:51', 6)
        //     ->push('2022-08-11-18:23:51', 7)
        //     ->push('2022-08-11-18:24:51', 4)
        //     ->push('2022-08-11-18:25:51', 3);



        foreach ($items as $row) {
            $image->push($row['dt'], $row['value']);
            // $image->push(str_replace(' ', '-', $row['dt']), $row['value']);
        }

        // ->writePng('date.png')


        $response->write($image->get());
        return $response;
    }
}
