# HTTPS and Security Configuration

## Django settings
- `SECURE_SSL_REDIRECT = True` forces HTTP->HTTPS redirects.
- `SECURE_HSTS_SECONDS = 31536000`, `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`, `SECURE_HSTS_PRELOAD = True` enable HSTS for one year across subdomains and allow preload submission.
- `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` ensure cookies are only sent over HTTPS.
- `X_FRAME_OPTIONS = 'DENY'` blocks clickjacking frames.
- `SECURE_CONTENT_TYPE_NOSNIFF = True` prevents MIME sniffing.
- `SECURE_BROWSER_XSS_FILTER = True` enables basic XSS protection.
- Optional when behind a TLS-terminating proxy (e.g., load balancer): set `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` so Django knows the original scheme.

## Deployment (Nginx example)
1) Obtain certificates (Let	's Encrypt):
   - `sudo apt install certbot python3-certbot-nginx`
   - `sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com`
2) Nginx server block (excerpt):
   ```
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       return 301 https://$host$request_uri;
   }

   server {
       listen 443 ssl http2;
       server_name yourdomain.com www.yourdomain.com;

       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_prefer_server_ciphers on;

       location / {
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto https;
           proxy_pass http://127.0.0.1:8000;
       }
   }
   ```
3) Reload Nginx: `sudo systemctl reload nginx`.

## Deployment (Apache example)
1) Enable modules: `a2enmod ssl headers proxy proxy_http rewrite`
2) Obtain certificates (Let	's Encrypt): `sudo certbot --apache -d yourdomain.com -d www.yourdomain.com`
3) VirtualHost (excerpt):
   ```
   <VirtualHost *:80>
       ServerName yourdomain.com
       ServerAlias www.yourdomain.com
       Redirect / https://yourdomain.com/
   </VirtualHost>

   <VirtualHost *:443>
       ServerName yourdomain.com
       ServerAlias www.yourdomain.com

       SSLEngine on
       SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
       SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem

       ProxyPreserveHost On
       ProxyPass / http://127.0.0.1:8000/
       ProxyPassReverse / http://127.0.0.1:8000/
       RequestHeader set X-Forwarded-Proto "https"
       Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
       Header always set X-Frame-Options "DENY"
       Header always set X-Content-Type-Options "nosniff"
       Header always set X-XSS-Protection "1; mode=block"
   </VirtualHost>
   ```
4) Reload Apache: `sudo systemctl reload apache2`.

## Security review
- HTTPS enforcement: `SECURE_SSL_REDIRECT` plus web server 301 ensures all traffic uses TLS.
- Transport hardening: HSTS locks browsers to HTTPS and can be preloaded.
- Cookie security: session and CSRF cookies are HTTPS-only.
- Browser headers: clickjacking, MIME sniffing, and basic XSS protections enabled.
- Remaining actions: set `ALLOWED_HOSTS` for production domains; add CSP middleware if using external assets; configure `SECURE_PROXY_SSL_HEADER` when behind a proxy; ensure cert renewal automation (certbot renew timer) and monitor TLS expiry.
