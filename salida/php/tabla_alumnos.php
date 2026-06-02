<?php
/* ==============================
   CONEXIÓN
   ============================== */
// Tabla: alumnos
//  + id : INTEGER
//  + nombre : varchar(20)
//  + apellidos : varchar(50)
//  + edad : INTEGER


$env = parse_ini_file(__DIR__ . "/.env");

if ($env === false) {
    die("No se pudo leer el fichero .env");
}

$host = $env["HOST"];
$db   = $env["DB"];
$user = $env["USER"];
$pass = $env["PASS"];

try {
    $pdo = new PDO("sqlite:$db", null, null, array(PDO::ATTR_PERSISTENT => true, PDO::ATTR_ERRMODE => true, PDO::ERRMODE_EXCEPTION => true));
} catch (PDOException $e) {
    die("Error de conexión: " . $e->getMessage());
}


/* ==============================
   CREATE
   ============================== */

if (isset($_POST["create"])) {

    $stmt = $pdo->prepare(
        "INSERT INTO alumnos (id, nombre, apellidos, edad)
         VALUES (?, ?, ?, ?)"
    );

    $stmt->execute([
	$_POST["id"],
	$_POST["nombre"],
	$_POST["apellidos"],
	$_POST["edad"]
    ]);
}


/* ==============================
   UPDATE
   ============================== */

if (isset($_POST["update"])) {

    $stmt = $pdo->prepare(
        "UPDATE alumnos
         SET nombre = ?, apellidos = ?, edad = ?
		WHERE id = ? ;"
    );

    $stmt->execute([
		$_POST["nombre"],
		$_POST["apellidos"],
		$_POST["edad"],
		$_POST["id"]
    ]);
}


/* ==============================
   DELETE
   ============================== */

if (isset($_POST["delete"])) {

    $stmt = $pdo->prepare(
        "DELETE FROM alumnos WHERE id = ?"
    );

    $stmt->execute([$_POST["id"]]);
}


/* ==============================
   READ
   ============================== */

$filas = $pdo->query(
    "SELECT * FROM alumnos ORDER BY id"
)->fetchAll(PDO::FETCH_ASSOC);

?>

<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>CRUD alumnos</title>
<link href="css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="css/default.css">
<script src="js/bootstrap.bundle.min.js"></script>
</head>
<body>
<div class="container-md py-4">

<h1 class="mb4">DB: sqlite ➡️ UI: php</h1>
<!--<h2 class="mb4">Tablas disponibles en la base de datos</h2>-->
<h2>CRUD tabla alumnos</h2>
<div class="accordion" id="crudAccordion">
    <!-- ===================================================== -->
    <!-- CREATE -->
    <!-- ===================================================== -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="headingCreate">
            <button class="accordion-button collapsed" type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapseCreate">
            CREATE tabla alumnos
            </button>
        </h2>

        <div id="collapseCreate"
            class="accordion-collapse collapse"
            data-bs-parent="#crudAccordion">

            <div class="accordion-body">

             <form method="post">
                <div class="mb-3">	<label class="form-label">ID</label>
<input type="text" name="id" class="form-control" required /></div>
<div class="mb-3">	<label class="form-label">NOMBRE</label>
<input type="text" name="nombre" class="form-control" required /></div>
<div class="mb-3">	<label class="form-label">APELLIDOS</label>
<input type="text" name="apellidos" class="form-control" required /></div>
<div class="mb-3">	<label class="form-label">EDAD</label>
<input type="text" name="edad" class="form-control" required /></div>

                <button type="submit" name="create" class="btn btn-success">Crear</button>
            </form>

            </div>
        </div>
    </div>

    <!-- ===================================================== -->
    <!-- READ -->
    <!-- ===================================================== -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="headingRead">
            <button class="accordion-button" type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapseRead">
            READ – Listado de alumnos
            </button>
        </h2>

        <div id="collapseRead"
            class="accordion-collapse collapse show"
            data-bs-parent="#crudAccordion">

            <div class="accordion-body">

            <table class="table table-striped table-bordered table-hover">
                <tr>
                	<th>Id</th>
	<th>Nombre</th>
	<th>Apellidos</th>
	<th>Edad</th>
</tr>

                <?php foreach ($filas as $fila): ?>
                <tr>
                	<td><?= htmlspecialchars($fila["id"]) ?></td>
	<td><?= htmlspecialchars($fila["nombre"]) ?></td>
	<td><?= htmlspecialchars($fila["apellidos"]) ?></td>
	<td><?= htmlspecialchars($fila["edad"]) ?></td>
</tr>
                <?php endforeach; ?>
            </table>

            </div>
        </div>
    </div>

    <!-- ===================================================== -->
    <!-- UPDATE -->
    <!-- ===================================================== -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="headingUpdate">
            <button class="accordion-button collapsed" type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapseUpdate">
            UPDATE – Modificar alumnos
            </button>
        </h2>

        <div id="collapseUpdate"
            class="accordion-collapse collapse"
            data-bs-parent="#crudAccordion">

            <div class="accordion-body">

             <form method="post">
            <div class="mb-3">	<label class="form-label">ID</label>
<input type="text" name="id" class="form-control" required /></div>
<div class="mb-3">	<label class="form-label">NOMBRE</label>
<input type="text" name="nombre" class="form-control" required /></div>
<div class="mb-3">	<label class="form-label">APELLIDOS</label>
<input type="text" name="apellidos" class="form-control" required /></div>
<div class="mb-3">	<label class="form-label">EDAD</label>
<input type="text" name="edad" class="form-control" required /></div>

                <button type="submit" name="update" class="btn btn-success">Actualizar</button>
            </form>

            </div>
        </div>
    </div>

    <!-- ===================================================== -->
    <!-- DELETE -->
    <!-- ===================================================== -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="headingDelete">
            <button class="accordion-button collapsed" type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapseDelete">
            DELETE – Borrar alumnos
            </button>
        </h2>

        <div id="collapseDelete"
            class="accordion-collapse collapse"
            data-bs-parent="#crudAccordion">

            <div class="accordion-body">

            <form method="post">
                <label class="form-label">ID del alumno:</label>
                <input type="number" name="id" class="form-control" required>

                <button type="submit" name="delete" class="btn btn-danger">Eliminar</button>
            </form>

            </div>
        </div>
    </div>
</div>

<div class="btn btn-success"><a href="index.php">Volver</a></div>
</body>
</html>
