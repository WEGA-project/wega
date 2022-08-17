<?php
// DIC configuration
use Twig\Extension\DebugExtension;
use App\Model\Device;
use App\Twig\WegaTwigExtension;


$container = $app->getContainer();

// -----------------------------------------------------------------------------
// Service providers
// -----------------------------------------------------------------------------

// Twig
$container['view'] = function ($c) {
    $settings = $c->get('settings');
    $view = new Slim\Views\Twig($settings['view']['template_path'], $settings['view']['twig']);

    // Add extensions
    $view->addExtension(new Slim\Views\TwigExtension($c->get('router'), $c->get('request')->getUri()));
    $view->addExtension(new DebugExtension());
    $view->addExtension(new WegaTwigExtension());

    return $view;
};

// Flash messages
// $container['flash'] = function ($c) {
//     return new Slim\Flash\Messages;
// };
// -----------------------------------------------------------------------------
// Service factories
// -----------------------------------------------------------------------------

// monolog
// $container['logger'] = function ($c) {
//     $settings = $c->get('settings');
//     $logger = new Monolog\Logger($settings['logger']['name']);
//     $logger->pushProcessor(new Monolog\Processor\UidProcessor());
//     $logger->pushHandler(new Monolog\Handler\StreamHandler($settings['logger']['path'], Monolog\Logger::DEBUG));
//     return $logger;
// };

$container['db'] = function ($container) {
    $capsule = new \Illuminate\Database\Capsule\Manager;

    // $logger = $container->get('logger');

    $capsule->addConnection($container['settings']['main-db'], 'main');
    $capsule->setAsGlobal();
    $capsule->bootEloquent();

    // $capsule->getConnection('main')->setEventDispatcher(new \Illuminate\Events\Dispatcher);
    // $capsule->getConnection('main')->listen(function ($query) {
    //     echo '<pre>' . var_export($query, true) . '</pre>';
    // });

    // $capsule::get

    // $logger->info('attach devices');
    $devices = Device::all();
    // if (count($devices) === 0) {
    //     $logger->warning('no devices');
    // }

    foreach ($devices as $device) {
        $db_name = $device->db;
        // $logger->info("attach $db_name");
        $settings = $container['settings']['device-db'];
        $settings['database'] = $db_name;
        $capsule->addConnection($settings, $db_name);
    }

    return $capsule;
};


$db = $container->get('db');

// $sens = $db->table('sens', 'kostya')->take(10)->get();
// print_r($sens);







// $container['main-db2'] = function ($c) {
//     $db = $c['settings']['main-db'];
//     $pdo = new PDO(
//         "mysql:host=" . $db['host'] . ";dbname=" . $db['database'],
//         $db['username'],
//         $db['password']
//     );
//     $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
//     $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

//     return $pdo;
// };

// $devices = $container->get('main-db')->table('devices');


// print_r($container->get('main-db'));
// print_r($container->get('main-db2'));



// -----------------------------------------------------------------------------
// Action factories
// -----------------------------------------------------------------------------

// $container[App\Action\HomeAction::class] = function ($c) {
//     $view = $c->get('view');
//     $logger = $c->get('logger');
//     $devices_table = $c->get('main-db')->table('devices');

//     return new App\Action\HomeAction($view, $logger, $devices_table);
// };
