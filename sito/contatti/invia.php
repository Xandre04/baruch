<?php
// Riceve il modulo della pagina Contatti e lo inoltra via email a Caterina.
// Funziona su Keliweb (PHP); l'anteprima su GitHub Pages non esegue PHP.
const DESTINATARIO = 'illustraremondi@gmail.com';

header('Content-Type: application/json; charset=utf-8');

function rispondi(bool $ok, int $codice = 200): void {
    http_response_code($codice);
    echo json_encode(['ok' => $ok]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') rispondi(false, 405);

// campo nascosto: le persone non lo vedono, i programmi di spam lo compilano
if (!empty($_POST['sito'])) rispondi(true);

$nome = trim(str_replace(["\r", "\n"], ' ', strip_tags($_POST['nome'] ?? '')));
$email = trim($_POST['email'] ?? '');
$messaggio = trim(strip_tags($_POST['messaggio'] ?? ''));

if (strlen($nome) < 2 || strlen($nome) > 100
    || !filter_var($email, FILTER_VALIDATE_EMAIL)
    || strlen($messaggio) < 10 || strlen($messaggio) > 5000) {
    rispondi(false, 422);
}

$dominio = preg_replace('/^www\./', '', $_SERVER['SERVER_NAME']);
$oggetto = '=?UTF-8?B?' . base64_encode("Messaggio dal sito da $nome") . '?=';
$intestazioni = implode("\r\n", [
    "From: Sito Baruch <noreply@$dominio>",
    "Reply-To: $email",
    'Content-Type: text/plain; charset=UTF-8',
]);
$testo = "$messaggio\n\n--\n$nome\n$email\n";

rispondi(mail(DESTINATARIO, $oggetto, $testo, $intestazioni), 200);
