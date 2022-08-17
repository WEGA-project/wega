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

/* pages/home.twig */
class __TwigTemplate_8e1969055846077ed0519071a9381b0f1b8f0d9a401ddd510f9aa678da5cbe8a extends \Twig\Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->blocks = [
            'title' => [$this, 'block_title'],
            'body' => [$this, 'block_body'],
        ];
    }

    protected function doGetParent(array $context)
    {
        // line 1
        return "layout.html.twig";
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        $this->parent = $this->loadTemplate("layout.html.twig", "pages/home.twig", 1);
        $this->parent->display($context, array_merge($this->blocks, $blocks));
    }

    // line 2
    public function block_title($context, array $blocks = [])
    {
        $macros = $this->macros;
        echo "Панель управления
";
    }

    // line 4
    public function block_body($context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 5
        echo "
\t";
        // line 6
        if (twig_test_empty(($context["devices"] ?? null))) {
            // line 7
            echo "\t\t<h2 class=\"content-head is-center\">Нет доступных систем</h2>
\t";
        } else {
            // line 9
            echo "
\t\t<h2 class=\"content-head is-center\">Список доступных систем</h2>
\t\t<table class=\"pure-table with-full\" style=\"margin-top: 3rem\">
\t\t\t<thead>
\t\t\t\t<tr>
\t\t\t\t\t<th scope=\"col\">Краткое имя</th>
\t\t\t\t\t<th scope=\"col\">Подробное описание</th>
\t\t\t\t\t<th scope=\"col\">t°C</th>
\t\t\t\t\t<th scope=\"col\">RH</th>
\t\t\t\t\t<th scope=\"col\">EC</th>
\t\t\t\t\t<th scope=\"col\">pH</th>
\t\t\t\t\t<th scope=\"col\">V</th>
\t\t\t\t\t<th scope=\"col\">Обновлено</th>
\t\t\t\t</tr>
\t\t\t</thead>
\t\t\t<tbody>
\t\t\t\t";
            // line 25
            $context['_parent'] = $context;
            $context['_seq'] = twig_ensure_traversable(($context["devices"] ?? null));
            foreach ($context['_seq'] as $context["key"] => $context["device"]) {
                // line 26
                echo "\t\t\t\t\t<tr>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t<a href=\"";
                // line 28
                echo twig_escape_filter($this->env, $this->extensions['Slim\Views\TwigExtension']->pathFor("status", ["device" => twig_get_attribute($this->env, $this->source, $context["device"], "db", [], "any", false, false, false, 28)]), "html", null, true);
                echo "\">
\t\t\t\t\t\t\t\t";
                // line 29
                echo twig_escape_filter($this->env, $this->extensions['App\Twig\WegaTwigExtension']->getOneOfTwo(twig_get_attribute($this->env, $this->source, $context["device"], "namesys", [], "any", false, false, false, 29), twig_get_attribute($this->env, $this->source, $context["device"], "name", [], "any", false, false, false, 29)), "html", null, true);
                echo "
\t\t\t\t\t\t\t</a>
\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t";
                // line 33
                echo twig_escape_filter($this->env, $this->extensions['App\Twig\WegaTwigExtension']->getStringValue(twig_get_attribute($this->env, $this->source, $context["device"], "comment", [], "any", false, false, false, 33)), "html", null, true);
                echo "

\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t";
                // line 37
                echo twig_escape_filter($this->env, $this->extensions['App\Twig\WegaTwigExtension']->getRoundedValue(twig_get_attribute($this->env, $this->source, $context["device"], "air_temp", [], "any", false, false, false, 37), 1, "", "-"), "html", null, true);
                echo "
\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>

\t\t\t\t\t\t\t";
                // line 41
                echo twig_escape_filter($this->env, $this->extensions['App\Twig\WegaTwigExtension']->getRoundedValue(twig_get_attribute($this->env, $this->source, $context["device"], "air_hum", [], "any", false, false, false, 41), 1, "%", "-"), "html", null, true);
                echo "

\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>

\t\t\t\t\t\t\t";
                // line 46
                echo twig_escape_filter($this->env, $this->extensions['App\Twig\WegaTwigExtension']->getRoundedValue(twig_get_attribute($this->env, $this->source, $context["device"], "ec", [], "any", false, false, false, 46), 1, "", "-"), "html", null, true);
                echo "

\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t";
                // line 50
                echo twig_escape_filter($this->env, $this->extensions['App\Twig\WegaTwigExtension']->getRoundedValue(twig_get_attribute($this->env, $this->source, $context["device"], "ph", [], "any", false, false, false, 50), 1, "", "-"), "html", null, true);
                echo "

\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t";
                // line 54
                echo twig_escape_filter($this->env, $this->extensions['App\Twig\WegaTwigExtension']->getRoundedValue(twig_get_attribute($this->env, $this->source, $context["device"], "lev", [], "any", false, false, false, 54), 1, "", "-"), "html", null, true);
                echo "

\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t";
                // line 58
                echo twig_escape_filter($this->env, $this->extensions['App\Twig\WegaTwigExtension']->getStringValue(twig_get_attribute($this->env, $this->source, $context["device"], "date", [], "any", false, false, false, 58)), "html", null, true);
                echo "

\t\t\t\t\t\t</td>
\t\t\t\t\t</tr>
\t\t\t\t";
            }
            $_parent = $context['_parent'];
            unset($context['_seq'], $context['_iterated'], $context['key'], $context['device'], $context['_parent'], $context['loop']);
            $context = array_intersect_key($context, $_parent) + $_parent;
            // line 63
            echo "\t\t\t</tbody>
\t\t</table>
\t";
        }
        // line 66
        echo "
";
    }

    public function getTemplateName()
    {
        return "pages/home.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  164 => 66,  159 => 63,  148 => 58,  141 => 54,  134 => 50,  127 => 46,  119 => 41,  112 => 37,  105 => 33,  98 => 29,  94 => 28,  90 => 26,  86 => 25,  68 => 9,  64 => 7,  62 => 6,  59 => 5,  55 => 4,  47 => 2,  36 => 1,);
    }

    public function getSourceContext()
    {
        return new Source("{% extends 'layout.html.twig' %}
{% block title %}Панель управления
{% endblock %}
{% block body %}

\t{% if devices is empty %}
\t\t<h2 class=\"content-head is-center\">Нет доступных систем</h2>
\t{% else %}

\t\t<h2 class=\"content-head is-center\">Список доступных систем</h2>
\t\t<table class=\"pure-table with-full\" style=\"margin-top: 3rem\">
\t\t\t<thead>
\t\t\t\t<tr>
\t\t\t\t\t<th scope=\"col\">Краткое имя</th>
\t\t\t\t\t<th scope=\"col\">Подробное описание</th>
\t\t\t\t\t<th scope=\"col\">t°C</th>
\t\t\t\t\t<th scope=\"col\">RH</th>
\t\t\t\t\t<th scope=\"col\">EC</th>
\t\t\t\t\t<th scope=\"col\">pH</th>
\t\t\t\t\t<th scope=\"col\">V</th>
\t\t\t\t\t<th scope=\"col\">Обновлено</th>
\t\t\t\t</tr>
\t\t\t</thead>
\t\t\t<tbody>
\t\t\t\t{% for key, device in devices %}
\t\t\t\t\t<tr>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t<a href=\"{{ path_for('status', { 'device': device.db }) }}\">
\t\t\t\t\t\t\t\t{{ one_of(device.namesys, device.name)}}
\t\t\t\t\t\t\t</a>
\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t{{ string_value(device.comment) }}

\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t{{ float_value(device.air_temp, 1, '', '-') }}
\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>

\t\t\t\t\t\t\t{{ float_value(device.air_hum, 1, '%', '-') }}

\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>

\t\t\t\t\t\t\t{{ float_value(device.ec, 1, '', '-') }}

\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t{{ float_value(device.ph, 1, '', '-') }}

\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t{{ float_value(device.lev, 1, '', '-') }}

\t\t\t\t\t\t</td>
\t\t\t\t\t\t<td>
\t\t\t\t\t\t\t{{ string_value(device.date) }}

\t\t\t\t\t\t</td>
\t\t\t\t\t</tr>
\t\t\t\t{% endfor %}
\t\t\t</tbody>
\t\t</table>
\t{% endif %}

{% endblock %}
", "pages/home.twig", "/var/WEGA/wega-slim/app/templates/pages/home.twig");
    }
}
