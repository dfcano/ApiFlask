from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta, timezone

# Generar clave privada
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Crear certificado
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"CO"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Colombia"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Bogotá D.C"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Diego Inc"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"diego.cano.com"),
])
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.now(timezone.utc)
).not_valid_after(
    # Certificado válido por 1 año
    datetime.now(timezone.utc) + timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
    critical=False,
).sign(key, hashes.SHA256())

# Guardar clave privada en una ruta específica
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Guardar certificado en una ruta específica
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))
