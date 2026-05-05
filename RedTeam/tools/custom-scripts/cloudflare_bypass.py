#!/usr/bin/env python3
"""
Cloudflare Bypass Toolkit
Múltiples métodos para evadir protección de Cloudflare
"""

import argparse
import json
import sys
import time
import random

# User agents reales de navegadores
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

def method_cloudscraper(url, method="GET", data=None, headers=None):
    """Método 1: CloudScraper - Resuelve JS challenges automáticamente"""
    try:
        import cloudscraper
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        if method.upper() == "GET":
            response = scraper.get(url, headers=headers)
        else:
            response = scraper.post(url, data=data, headers=headers)
        
        return {
            "success": True,
            "method": "cloudscraper",
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "cookies": dict(response.cookies),
            "content_length": len(response.content),
            "content": response.text[:2000] if len(response.text) > 2000 else response.text
        }
    except Exception as e:
        return {"success": False, "method": "cloudscraper", "error": str(e)}

def method_curl_cffi(url, method="GET", data=None, headers=None):
    """Método 2: curl_cffi - Impersona navegadores reales a nivel TLS"""
    try:
        from curl_cffi import requests as curl_requests
        
        # Impersona Chrome
        if method.upper() == "GET":
            response = curl_requests.get(url, impersonate="chrome124", headers=headers)
        else:
            response = curl_requests.post(url, data=data, impersonate="chrome124", headers=headers)
        
        return {
            "success": True,
            "method": "curl_cffi",
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "cookies": dict(response.cookies),
            "content_length": len(response.content),
            "content": response.text[:2000] if len(response.text) > 2000 else response.text
        }
    except Exception as e:
        return {"success": False, "method": "curl_cffi", "error": str(e)}

def method_httpx_http2(url, method="GET", data=None, headers=None):
    """Método 3: HTTPX con HTTP/2 - Mejor fingerprint"""
    try:
        import httpx
        
        default_headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }
        if headers:
            default_headers.update(headers)
        
        with httpx.Client(http2=True, follow_redirects=True) as client:
            if method.upper() == "GET":
                response = client.get(url, headers=default_headers)
            else:
                response = client.post(url, data=data, headers=default_headers)
        
        return {
            "success": True,
            "method": "httpx_http2",
            "status_code": response.status_code,
            "http_version": str(response.http_version),
            "headers": dict(response.headers),
            "content_length": len(response.content),
            "content": response.text[:2000] if len(response.text) > 2000 else response.text
        }
    except Exception as e:
        return {"success": False, "method": "httpx_http2", "error": str(e)}

def find_origin_ip(domain):
    """Buscar IP origen detrás de Cloudflare"""
    import subprocess
    
    results = {
        "domain": domain,
        "methods": []
    }
    
    # Método 1: Buscar en registros históricos DNS
    try:
        # SecurityTrails, ViewDNS, etc. (requiere API keys)
        pass
    except:
        pass
    
    # Método 2: Buscar subdominios que no estén en CF
    subdomains_to_check = [
        f"direct.{domain}",
        f"origin.{domain}",
        f"server.{domain}",
        f"backend.{domain}",
        f"api.{domain}",
        f"mail.{domain}",
        f"ftp.{domain}",
        f"cpanel.{domain}",
        f"webmail.{domain}",
        f"admin.{domain}",
        f"dev.{domain}",
        f"staging.{domain}",
        f"test.{domain}",
    ]
    
    print(f"[*] Buscando subdominios sin Cloudflare para {domain}...")
    
    for sub in subdomains_to_check:
        try:
            result = subprocess.run(
                ["dig", "+short", sub],
                capture_output=True, text=True, timeout=5
            )
            ip = result.stdout.strip()
            if ip and not ip.startswith("104.") and not ip.startswith("172.") and not ip.startswith("103."):
                # No es IP de Cloudflare
                results["methods"].append({
                    "subdomain": sub,
                    "ip": ip,
                    "cloudflare": False
                })
                print(f"[+] {sub} -> {ip} (NO CLOUDFLARE)")
        except:
            pass
    
    return results

def check_cloudflare(url):
    """Verificar si un sitio está detrás de Cloudflare"""
    try:
        import requests
        response = requests.head(url, timeout=10, allow_redirects=True)
        
        cf_indicators = {
            "cf-ray": response.headers.get("cf-ray"),
            "cf-cache-status": response.headers.get("cf-cache-status"),
            "server": response.headers.get("server"),
            "cf-request-id": response.headers.get("cf-request-id"),
        }
        
        is_cloudflare = any([
            cf_indicators["cf-ray"],
            cf_indicators["server"] and "cloudflare" in cf_indicators["server"].lower(),
        ])
        
        return {
            "url": url,
            "is_cloudflare": is_cloudflare,
            "indicators": cf_indicators,
            "status_code": response.status_code
        }
    except Exception as e:
        return {"url": url, "error": str(e)}

def bypass_all_methods(url):
    """Probar todos los métodos de bypass"""
    print(f"\n{'='*60}")
    print(f"[*] Target: {url}")
    print(f"{'='*60}\n")
    
    # Verificar si tiene Cloudflare
    cf_check = check_cloudflare(url)
    print(f"[*] Cloudflare detectado: {cf_check.get('is_cloudflare', 'Unknown')}")
    if cf_check.get('indicators', {}).get('cf-ray'):
        print(f"    CF-Ray: {cf_check['indicators']['cf-ray']}")
    print()
    
    results = []
    
    # Método 1: CloudScraper
    print("[*] Probando CloudScraper...")
    result = method_cloudscraper(url)
    results.append(result)
    print(f"    Status: {result.get('status_code', 'Error')} - {'✓' if result['success'] else '✗'}")
    
    time.sleep(1)
    
    # Método 2: curl_cffi
    print("[*] Probando curl_cffi (Chrome impersonation)...")
    result = method_curl_cffi(url)
    results.append(result)
    print(f"    Status: {result.get('status_code', 'Error')} - {'✓' if result['success'] else '✗'}")
    
    time.sleep(1)
    
    # Método 3: HTTPX HTTP/2
    print("[*] Probando HTTPX con HTTP/2...")
    result = method_httpx_http2(url)
    results.append(result)
    print(f"    Status: {result.get('status_code', 'Error')} - {'✓' if result['success'] else '✗'}")
    
    # Resumen
    print(f"\n{'='*60}")
    print("[*] RESUMEN:")
    for r in results:
        status = "✓ SUCCESS" if r['success'] and r.get('status_code', 0) == 200 else "✗ FAILED"
        print(f"    {r['method']}: {status}")
    
    # Retornar el mejor resultado
    for r in results:
        if r['success'] and r.get('status_code') == 200:
            return r
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Cloudflare Bypass Toolkit")
    parser.add_argument("url", help="URL objetivo")
    parser.add_argument("-m", "--method", choices=["cloudscraper", "curl_cffi", "httpx", "all", "origin"],
                       default="all", help="Método de bypass")
    parser.add_argument("-o", "--output", help="Guardar resultado en archivo JSON")
    parser.add_argument("--check", action="store_true", help="Solo verificar si tiene Cloudflare")
    
    args = parser.parse_args()
    
    if args.check:
        result = check_cloudflare(args.url)
        print(json.dumps(result, indent=2))
        return
    
    if args.method == "origin":
        from urllib.parse import urlparse
        domain = urlparse(args.url).netloc
        result = find_origin_ip(domain)
        print(json.dumps(result, indent=2))
        return
    
    if args.method == "all":
        result = bypass_all_methods(args.url)
    elif args.method == "cloudscraper":
        result = method_cloudscraper(args.url)
    elif args.method == "curl_cffi":
        result = method_curl_cffi(args.url)
    elif args.method == "httpx":
        result = method_httpx_http2(args.url)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n[+] Resultado guardado en {args.output}")
    
    return result

if __name__ == "__main__":
    main()
