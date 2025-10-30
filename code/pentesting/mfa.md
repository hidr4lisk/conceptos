La autenticación multifactor (MFA) refuerza la seguridad al exigir dos o más verificaciones distintas. La 2FA es un caso particular de MFA que usa exactamente dos factores.

Factores de autenticación:

Algo que sabés: contraseña, PIN.

Algo que tenés: celular con app, token físico, smartcard, certificado cliente.

Algo que sos: biometría (huella, rostro, iris).

Dónde estás: geolocalización, IP de origen.

Algo que hacés: patrones de tecleo, movimiento del mouse.

Métodos comunes de 2FA:

TOTP (Google Authenticator, Authy): códigos que expiran cada 30s.

Push notifications (Duo, Google Prompt): aprobación directa en el dispositivo.

SMS: práctico, pero menos seguro por riesgo de interceptación.

Hardware tokens (ej. YubiKey): seguros, incluso sin conexión.

Acceso condicional: reglas dinámicas según contexto (ubicación, horario, dispositivo, comportamiento).

Adopción global: regulaciones como GDPR, HIPAA y PCI-DSS impulsan MFA en sectores críticos. Varias brechas masivas (Equifax 2017, Target 2013) habrían sido evitables con MFA.

Conclusión: MFA es hoy una medida esencial contra ataques de phishing, ingeniería social y robo de credenciales.

