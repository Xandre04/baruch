<?php
// Accesso all'editor con email e password, al posto dell'account GitHub.
//
// L'editor (Sveltia CMS) apre questa pagina quando si preme "Sign In with GitHub".
// Se email e password sono giuste, la pagina passa all'editor la chiave GitHub custodita sul server.
//
// Email, password e chiave NON stanno nel repository: sono nel file baruch-editor.php,
// da mettere sul server una cartella sopra quella pubblica del sito (vedi README).
// Funziona solo dove c'è PHP (Keliweb); l'anteprima su GitHub Pages non lo esegue.

$segreti = dirname($_SERVER['DOCUMENT_ROOT']) . '/baruch-editor.php';
const MAX_TENTATIVI = 5;        // tentativi sbagliati consentiti…
const FINESTRA = 15 * 60;       // …in 15 minuti, per ogni indirizzo IP

header('Cache-Control: no-store');
header('X-Frame-Options: DENY');
header('Referrer-Policy: no-referrer');

function file_tentativi(): string {
    return sys_get_temp_dir() . '/baruch-accesso-' . md5($_SERVER['REMOTE_ADDR'] ?? '') . '.json';
}

function tentativi_recenti(): array {
    $f = file_tentativi();
    $lista = is_file($f) ? (json_decode((string) file_get_contents($f), true) ?: []) : [];
    return array_values(array_filter($lista, fn($t) => $t > time() - FINESTRA));
}

$errore = '';
$token = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $recenti = tentativi_recenti();
    if (count($recenti) >= MAX_TENTATIVI) {
        $errore = 'Troppi tentativi sbagliati. Riprova tra un quarto d’ora.';
    } elseif (!is_file($segreti)) {
        $errore = 'L’accesso non è ancora configurato sul server.';
    } else {
        $s = require $segreti;
        $email_ok = hash_equals(strtolower(trim($s['email'])), strtolower(trim((string) ($_POST['email'] ?? ''))));
        $password_ok = hash_equals((string) $s['password'], (string) ($_POST['password'] ?? ''));
        if ($email_ok && $password_ok) {
            @unlink(file_tentativi());
            $token = $s['github_token'];
        } else {
            $recenti[] = time();
            file_put_contents(file_tentativi(), json_encode($recenti));
            sleep(1);
            $errore = 'Email o password non corrette.';
        }
    }
}
?>
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>Accesso · Editor di Baruch</title>
  <link rel="icon" href="../assets/img/ui/favicon.png">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@400;500&family=Kalam:wght@400&display=swap">
  <style>
    body { margin: 0; min-height: 100dvh; display: grid; place-items: center; padding: 24px 16px;
           background: #fefdfb; color: #34432f; font: 17px/1.5 "Barlow Semi Condensed", sans-serif; }
    main { width: min(100%, 360px); text-align: center; }
    img { width: 110px; margin: 0 auto 8px; display: block; }
    h1 { font: 400 30px/1.2 Kalam, cursive; margin: 0 0 20px; }
    form { display: grid; gap: 14px; text-align: left; }
    label { display: grid; gap: 4px; font-weight: 500; }
    input { font: inherit; padding: 10px 12px; border: 1.5px solid #9fb092; border-radius: 10px 14px 12px 9px; background: #fff; color: inherit; }
    input:focus { outline: none; border-color: #34432f; box-shadow: 0 0 0 3px #dfe9d6; }
    button { margin-top: 6px; padding: 14px; border: 0; cursor: pointer; font: 22px Kalam, cursive; color: #34432f;
             background: url(../assets/img/ui/pennellata-pesca.webp) center / 100% 100% no-repeat; }
    .errore { color: #a2401f; margin: 0; }
  </style>
</head>
<body>
  <main>
    <img src="../assets/img/ui/baruch-lettera.webp" alt="">
<?php if ($token): ?>
    <h1>Accesso riuscito</h1>
    <p>Puoi tornare all’editor.</p>
    <script>
      // consegna la chiave solo all'editor di questo stesso sito
      const contenuto = <?= json_encode(['token' => $token, 'provider' => 'github'], JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT) ?>;
      window.addEventListener('message', (e) => {
        if (e.origin !== location.origin || e.data !== 'authorizing:github') return;
        window.opener.postMessage('authorization:github:success:' + JSON.stringify(contenuto), e.origin);
      });
      window.opener?.postMessage('authorizing:github', location.origin);
    </script>
<?php else: ?>
    <h1>Editor di Baruch</h1>
    <form method="post">
      <label>Email <input type="email" name="email" autocomplete="username" required></label>
      <label>Password <input type="password" name="password" autocomplete="current-password" required></label>
<?php if ($errore): ?>
      <p class="errore" role="alert"><?= htmlspecialchars($errore) ?></p>
<?php endif; ?>
      <button type="submit">Entra</button>
    </form>
<?php endif; ?>
  </main>
</body>
</html>
