<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice</title>
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="css/default.css">
</head>
<?php
$env = parse_ini_file(__DIR__ . "/.env");
if ($env === false) {
    die("No se pudo leer el fichero .env");
}
$db   = $env["DB"];
$type = $env["TIPO_DB"]
?>
<body class="bg-light">
    <div class="min-vh-100 d-flex align-items-center">
        <div class="container-md py-4">
            <?php if (is_writable($db) || $type != 'sqlite') { ?>
            <h1 class="mb4">DB: %%TIPO_DB%% ➡️ UI: %%UI_TYPE%%</h1>
            <h2 class="mb4">Tablas disponibles en la base de datos</h2>
            <div class="list-group">
%%BOTONES%%
            </div>
            <?php } else { echo 'La base de datos "' . $db . '" es readonly.'; } ?>
        </div>
    </div>
</body>