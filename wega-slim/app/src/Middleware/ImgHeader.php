<?php

namespace App\Middleware;


final class ImgHeader
{

    public function __invoke($req, $res, $next)
    {
        $response = $next($req, $res);
        ob_clean();
        return $response
            ->withHeader('Content-Type', FILEINFO_MIME_TYPE);
    }
}
