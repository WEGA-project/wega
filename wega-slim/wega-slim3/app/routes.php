<?php

use App\Middleware\DeviceLoad;
use App\Middleware\ImgHeader;
use App\Middleware\SensorLoad;
use App\Action\StatusAction;
use App\Action\GraphAction;
use App\Action\SensorAction;


$app->get('/', App\Action\HomeAction::class)
    ->setName('home');

$app->group('/device/{device}', function () {

    $this->get('/status', StatusAction::class)->setName('status');
    $this->get('/sensor/{sensor}', SensorAction::class)->setName('sensor')->add(SensorLoad::class);
    $this->get('/sensor/{sensor}/graph', GraphAction::class)->setName('graph')->add(ImgHeader::class)->add(SensorLoad::class);
})->add(DeviceLoad::class);
