from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta, timezone

# Generate functions for clarity
def generate_key():
  return rsa.generate_private_key(
      public_exponent=65537,
      key_size=2048,
  )

def create_cert(key):
  subject = issuer = x509.Name([
      x509.NameAttribute(NameOID.COUNTRY_NAME, u"CO"),
      x509.NameAttribute(NameOID.STATE_OR_ PROVINCE_NAME, u"Colombia"),
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
      datetime.now(timezone.utc) + timedelta(days=365)
  ).add_extension(
      x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
      critical=False,
  ).sign(key, hashes.SHA256())
  return cert

def save_key_cert(key, cert, key_path="key.pem", cert_path="cert.pem"):
  with open(key_path, "wb") as f:
      f.write(key.private_bytes(
          encoding=serialization.Encoding.PEM,
          format=serialization.PrivateFormat.TraditionalOpenSSL,
          encryption_algorithm=serialization.NoEncryption()
      ))
  with open(cert_path, "wb") as f:
      f.write(cert.public_bytes(serialization.Encoding.PEM))

# Generate key and certificate
key = generate_key()
cert = create_cert(key)

# Save key and certificate
save_key_cert(key, cert)

print("Certificate and key generated successfully!")
