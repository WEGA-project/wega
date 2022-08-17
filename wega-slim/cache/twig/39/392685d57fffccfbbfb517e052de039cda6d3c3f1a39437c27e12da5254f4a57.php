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

/* layout.html.twig */
class __TwigTemplate_e31a7b9f44600c445697bc8dd896e11af2d277dc2282718d1a2565f930c4c447 extends \Twig\Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->parent = false;

        $this->blocks = [
            'title' => [$this, 'block_title'],
            'body' => [$this, 'block_body'],
        ];
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 1
        echo "<!DOCTYPE html>
<html lang=\"en\">
\t<head>
\t\t<meta charset=\"UTF-8\">
\t\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">

\t\t<link href='";
        // line 7
        echo twig_escape_filter($this->env, $this->extensions['Slim\Views\TwigExtension']->baseUrl(), "html", null, true);
        echo "/css/pure-min.css' rel='stylesheet' type='text/css' crossorigin=\"anonymous|use-credentials\">
\t\t<link href='";
        // line 8
        echo twig_escape_filter($this->env, $this->extensions['Slim\Views\TwigExtension']->baseUrl(), "html", null, true);
        echo "/css/style.css' rel='stylesheet' type='text/css' crossorigin=\"anonymous|use-credentials\">
\t\t<title>
\t\t\tWEGA|
\t\t\t";
        // line 11
        $this->displayBlock('title', $context, $blocks);
        // line 12
        echo "\t\t</title>
\t</head>

\t<body>

\t\t<header class=\"header\">
\t\t\t";
        // line 18
        $this->loadTemplate("nav.html.twig", "layout.html.twig", 18)->display($context);
        // line 19
        echo "\t\t</header>

\t\t<section class=\"content-wrapper main-layout-container\">
\t\t\t<div class=\"content\"> ";
        // line 22
        $this->displayBlock('body', $context, $blocks);
        // line 23
        echo "\t\t\t\t</div>
\t\t\t</section>
\t\t</body>
\t</html>
";
    }

    // line 11
    public function block_title($context, array $blocks = [])
    {
        $macros = $this->macros;
    }

    // line 22
    public function block_body($context, array $blocks = [])
    {
        $macros = $this->macros;
    }

    public function getTemplateName()
    {
        return "layout.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  90 => 22,  84 => 11,  76 => 23,  74 => 22,  69 => 19,  67 => 18,  59 => 12,  57 => 11,  51 => 8,  47 => 7,  39 => 1,);
    }

    public function getSourceContext()
    {
        return new Source("<!DOCTYPE html>
<html lang=\"en\">
\t<head>
\t\t<meta charset=\"UTF-8\">
\t\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">

\t\t<link href='{{ base_url() }}/css/pure-min.css' rel='stylesheet' type='text/css' crossorigin=\"anonymous|use-credentials\">
\t\t<link href='{{ base_url() }}/css/style.css' rel='stylesheet' type='text/css' crossorigin=\"anonymous|use-credentials\">
\t\t<title>
\t\t\tWEGA|
\t\t\t{% block title %}{% endblock %}
\t\t</title>
\t</head>

\t<body>

\t\t<header class=\"header\">
\t\t\t{% include 'nav.html.twig' %}
\t\t</header>

\t\t<section class=\"content-wrapper main-layout-container\">
\t\t\t<div class=\"content\"> {% block body %}{% endblock %}
\t\t\t\t</div>
\t\t\t</section>
\t\t</body>
\t</html>
", "layout.html.twig", "/var/WEGA/wega-slim/app/templates/layout.html.twig");
    }
}
