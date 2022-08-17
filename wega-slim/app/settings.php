<?php

$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . "/..");
$dotenv->safeLoad();

if ($_ENV["ENABLE_ERROR_REPORT"]) {
    error_reporting(E_ALL);
    ini_set('display_errors', '1');
}

return [
    'settings' => [
        // Slim Settings
        'determineRouteBeforeAppMiddleware' => true,
        'displayErrorDetails' => $_ENV["ENABLE_ERROR_REPORT"],

        // View settings
        'view' => [
            'template_path' => __DIR__ . '/templates',
            'twig' => [
                'cache' => __DIR__ . '/../cache/twig',
                'debug' => true,
                'auto_reload' => true,
            ],
        ],

        // monolog settings
        // 'logger' => [
        //     'name' => 'app',
        //     'path' => __DIR__ . '/../log/app.log',
        // ],

        'main-db' => [
            'driver' => 'mysql',
            'host' => $_ENV["DB_HOST"],
            'database' =>  $_ENV["DB_MAIN_NAME"],
            'username' => $_ENV["DB_MAIN_USER"],
            'password' =>  $_ENV["DB_MAIN_PASS"],
            'charset'   => 'utf8',
            'collation' => 'utf8_unicode_ci',
            'prefix'    => '',
        ],

        'device-db' => [
            'driver' => 'mysql',
            'host' => $_ENV["DB_HOST"],
            'username' => $_ENV["DB_DEVICE_USER"],
            'password' =>  $_ENV["DB_DEVICE_PASS"],
            'charset'   => 'utf8',
            'collation' => 'utf8_unicode_ci',
            'prefix'    => '',
        ]
    ],
];
