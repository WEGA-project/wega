<?php

use Twig\Environment;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Extension\SandboxExtension;
use Twig\Markup;
use Twig\Sandbox\SecurityError;
use Twig\Sandbox\SecurityNotAllowedTagError;
use Twig\Sandbox\SecurityNotAllowedFilterError;
use Twig\Sandbox\SecurityNotAllowedFunctionError;
use Twig\Source;
use Twig\Template;

/* nav.html.twig */
class __TwigTemplate_f229f8968a7ef96ed2ae5789143e086a1f0d582b5f2a0c3aa9e1b26a9fa26bb5 extends \Twig\Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->parent = false;

        $this->blocks = [
        ];
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 1
        echo "<link href='";
        echo twig_escape_filter($this->env, $this->extensions['Slim\Views\TwigExtension']->baseUrl(), "html", null, true);
        echo "/css/nav.css' rel='stylesheet' type='text/css' crossorigin=\"anonymous|use-credentials\">
<nav role=\"navigation\">
\t<ul>
\t\t<li>
\t\t\t<img src=\"";
        // line 5
        echo twig_escape_filter($this->env, $this->extensions['Slim\Views\TwigExtension']->baseUrl(), "html", null, true);
        echo "/img/wega-mini.png\" width=\"30\" height=\"32.5\" crossorigin=\"anonymous|use-credentials\"/>
\t\t\t<span style=\"vertical-align: 0.60em\">

\t\t\t\tWB4 PEPPER

\t\t\t</span>
\t\t\t<ul>
\t\t\t\t<li><a href=\"/\">Общий</a></li>
\t\t\t\t<li><a href=\"/\">NAMESYS 1</a></li>
\t\t\t</ul>
\t\t</li>


\t\t<li>
\t\t\t<a href=\"#\">Анализ</a>
\t\t\t<ul>
\t\t\t\t<li><a href=\"status.phpSTFIND\">Текущие измерения</a></li>
\t\t\t\t<li><a href=\"rep.phpSTFIND\">Сводный анализ</a></li>
\t\t\t\t<li><a href=\"helperprev.phpSTFIND\">Помощник</a></li>
\t\t\t\t<li><a href=\"temp.phpSTFIND\">Температура</a></li>
\t\t\t\t<li><a href=\"owm.phpSTFIND\">Погода</a></li>
\t\t\t\t<li><a href=\"mixer.phpSTFIND\">Миксер</a></li>
\t\t\t\t<li><a href=\"tmp/s.NS.csv\">Скачать csv</a></li>
\t\t\t</ul>
\t\t</li>
\t\t<li>
\t\t\t<a href=\"#\">Параметры</a>
\t\t\t<ul>
\t\t\t\t<li><a href=\"main.phpSTFIND\">Основные параметры</a></li>
\t\t\t\t<li><a href=\"srctbl.phpSTFIND\">База</a></li>
\t\t\t\t<li><a href=\"conformity.phpSTFIND\">Сопоставление полей</a></li>
\t\t\t\t<li><a href=\"termoresistor.phpSTFIND\">Температурная компенсация</a></li>
\t\t\t\t<li><a href=\"CalibrateEC.phpSTFIND\">Калибровка EC</a></li>
\t\t\t\t<li><a href=\"photoresistor.phpSTFIND\">Калибровка фоторезистора</a></li>
\t\t\t\t<li><a href=\"createlev.phpSTFIND\">Калибровка уровня</a></li>
\t\t\t\t<li><a href=\"level.phpSTFIND\">Фильтрация уровня</a></li>
\t\t\t\t<li><a href=\"ph.phpSTFIND\">Калибровка pH</a></li>
\t\t\t\t<li><a href=\"events.phpSTFIND\">Настройка уведомлений</a></li>
\t\t\t\t<li><a href=\"rmfunc.phpSTFIND\">Пересоздание функций</a></li>
\t\t\t</ul>
\t\t</li>
\t\t<li>
\t\t\t<a href=\"owm.phpSTFIND\">Погода</a>
\t\t\t<ul>
\t\t\t\t<li><a href=\"#\">Настройка</a></li>
\t\t\t</ul>
\t\t</li>
\t\t<li>
\t\t\t<a href=\"#\">О проекте</a>
\t\t\t<ul>
\t\t\t\t<li>
\t\t\t\t\t<strong style=\"font-size: 10px\">Версия от: VERSION</strong>
\t\t\t\t</li>
\t\t\t\t<li>
\t\t\t\t\t<a href=\"https://github.com/WEGA-project/wega\">Обновления GIT</a>
\t\t\t\t</li>
\t\t\t\t<li>
\t\t\t\t\t<a href=\"https://t.me/WEGA_SERVER\">Группа поддержки</a>
\t\t\t\t</li>
\t\t\t\t<li>
\t\t\t\t\t<a href=\"https://github.com/WEGA-project/wega/wiki\">WiKI проекта</a>
\t\t\t\t</li>
\t\t\t</ul>
\t\t</li>
\t</ul>
</nav>
";
    }

    public function getTemplateName()
    {
        return "nav.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  45 => 5,  37 => 1,);
    }

    public function getSourceContext()
    {
        return new Source("<link href='{{ base_url() }}/css/nav.css' rel='stylesheet' type='text/css' crossorigin=\"anonymous|use-credentials\">
<nav role=\"navigation\">
\t<ul>
\t\t<li>
\t\t\t<img src=\"{{ base_url() }}/img/wega-mini.png\" width=\"30\" height=\"32.5\" crossorigin=\"anonymous|use-credentials\"/>
\t\t\t<span style=\"vertical-align: 0.60em\">

\t\t\t\tWB4 PEPPER

\t\t\t</span>
\t\t\t<ul>
\t\t\t\t<li><a href=\"/\">Общий</a></li>
\t\t\t\t<li><a href=\"/\">NAMESYS 1</a></li>
\t\t\t</ul>
\t\t</li>


\t\t<li>
\t\t\t<a href=\"#\">Анализ</a>
\t\t\t<ul>
\t\t\t\t<li><a href=\"status.phpSTFIND\">Текущие измерения</a></li>
\t\t\t\t<li><a href=\"rep.phpSTFIND\">Сводный анализ</a></li>
\t\t\t\t<li><a href=\"helperprev.phpSTFIND\">Помощник</a></li>
\t\t\t\t<li><a href=\"temp.phpSTFIND\">Температура</a></li>
\t\t\t\t<li><a href=\"owm.phpSTFIND\">Погода</a></li>
\t\t\t\t<li><a href=\"mixer.phpSTFIND\">Миксер</a></li>
\t\t\t\t<li><a href=\"tmp/s.NS.csv\">Скачать csv</a></li>
\t\t\t</ul>
\t\t</li>
\t\t<li>
\t\t\t<a href=\"#\">Параметры</a>
\t\t\t<ul>
\t\t\t\t<li><a href=\"main.phpSTFIND\">Основные параметры</a></li>
\t\t\t\t<li><a href=\"srctbl.phpSTFIND\">База</a></li>
\t\t\t\t<li><a href=\"conformity.phpSTFIND\">Сопоставление полей</a></li>
\t\t\t\t<li><a href=\"termoresistor.phpSTFIND\">Температурная компенсация</a></li>
\t\t\t\t<li><a href=\"CalibrateEC.phpSTFIND\">Калибровка EC</a></li>
\t\t\t\t<li><a href=\"photoresistor.phpSTFIND\">Калибровка фоторезистора</a></li>
\t\t\t\t<li><a href=\"createlev.phpSTFIND\">Калибровка уровня</a></li>
\t\t\t\t<li><a href=\"level.phpSTFIND\">Фильтрация уровня</a></li>
\t\t\t\t<li><a href=\"ph.phpSTFIND\">Калибровка pH</a></li>
\t\t\t\t<li><a href=\"events.phpSTFIND\">Настройка уведомлений</a></li>
\t\t\t\t<li><a href=\"rmfunc.phpSTFIND\">Пересоздание функций</a></li>
\t\t\t</ul>
\t\t</li>
\t\t<li>
\t\t\t<a href=\"owm.phpSTFIND\">Погода</a>
\t\t\t<ul>
\t\t\t\t<li><a href=\"#\">Настройка</a></li>
\t\t\t</ul>
\t\t</li>
\t\t<li>
\t\t\t<a href=\"#\">О проекте</a>
\t\t\t<ul>
\t\t\t\t<li>
\t\t\t\t\t<strong style=\"font-size: 10px\">Версия от: VERSION</strong>
\t\t\t\t</li>
\t\t\t\t<li>
\t\t\t\t\t<a href=\"https://github.com/WEGA-project/wega\">Обновления GIT</a>
\t\t\t\t</li>
\t\t\t\t<li>
\t\t\t\t\t<a href=\"https://t.me/WEGA_SERVER\">Группа поддержки</a>
\t\t\t\t</li>
\t\t\t\t<li>
\t\t\t\t\t<a href=\"https://github.com/WEGA-project/wega/wiki\">WiKI проекта</a>
\t\t\t\t</li>
\t\t\t</ul>
\t\t</li>
\t</ul>
</nav>
", "nav.html.twig", "/var/WEGA/wega-slim/app/templates/nav.html.twig");
    }
}
