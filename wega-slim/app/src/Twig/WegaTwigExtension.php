<?php

namespace App\Twig;

use Twig\Extension\AbstractExtension;
use Twig\TwigFunction;
use Illuminate\Support\Str;

class WegaTwigExtension extends AbstractExtension
{
    public function getFunctions()
    {
        return [
            new TwigFunction('status', [$this, 'renderStatus'], array('is_safe' => array('html'))),
            new TwigFunction('float_value', [$this, 'getRoundedValue']),
            new TwigFunction('string_value', [$this, 'getStringValue']),
            new TwigFunction('one_of', [$this, 'getOneOfTwo']),
            new TwigFunction('cls_uncamel', [$this, 'getClassNameUncamel']),
        ];
    }

    public function renderStatus($state): string
    {
        if (is_bool($state)) {
            $content = $state ? 'норма' : 'проблема';
            $class = $state ? 'text-success' : 'text-danger';
        }

        if (is_array($state)) {
            $content = $state['valid'] ? 'норма' :  $this->getOneOfTwo($state['info'], 'проблема');
            $class = $state['valid'] ? 'text-success' : 'text-danger';
        }

        return "<span class=\"$class\">$content</span>";
    }

    public function getRoundedValue($value, int $level = 0, string $suffix = '', string $empty_val = "нет данных"): string
    {
        return $value ? round($value, $level) . $suffix : $empty_val;
    }

    public function getStringValue($str, string $suffix = '', string $empty_val = "-"): string
    {
        return $str ? $str . $suffix : $empty_val;
    }

    public function getOneOfTwo($one, string $two): string
    {
        return $one ? $one : $two;
    }

    public function getClassNameUncamel($class): string
    {
        $path = explode('\\', get_class($class));
        $name = array_pop($path);

        // . '---' . Str::ucfirst(Str::camel(Str::snake($name, '-')));
        return   Str::snake($name, '-');
    }
}
