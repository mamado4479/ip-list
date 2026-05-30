import urllib.parse
import socket
import os

# لیست دامنه‌های هدف
DOMAINS = ["nima.nscl.ir", "bpb.yousef.isegaro.com"]

# پورت‌های مورد نظر
PORTS = [443]

# کانفیگ پایه (الگو)
BASE_CONFIG = "vless://83d88a91-1cf2-4cb1-b9fd-e2d8ed4f15a1@104.17.122.54:443?encryption=none&security=tls&sni=proj1.mamado4479.workers.dev&fp=qq&insecure=0&allowInsecure=0&type=ws&host=proj1.mamado4479.workers.dev&path=%2F%3Fed%3D2048#CFNEW
"

def get_ips(domain):
    """تبدیل دامنه به لیست آی‌پی‌های فعال"""
    try:
        data = socket.getaddrinfo(domain, 80, socket.AF_INET)
        return list(set([item[4][0] for item in data]))
    except Exception as e:
        print(f"خطا در یافتن آی‌پی برای {domain}: {e}")
        return []

def main():
    parsed_url = urllib.parse.urlparse(BASE_CONFIG)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    # پردازش دامنه‌ها
    for domain in DOMAINS:
        domain_configs = []
        ips = get_ips(domain)
        
        print(f"تعداد {len(ips)} آی‌پی برای {domain} یافت شد.")
        
        for ip in ips:
            for port in PORTS:
                netloc = f"{parsed_url.username}@{ip}:{port}"
                # برچسب زدن برای نام نود
                node_label = "nima" if "nima" in domain else "bpb"
                node_name = f"{node_label}-{ip}"
                
                new_config = urllib.parse.urlunparse((
                    parsed_url.scheme,
                    netloc,
                    parsed_url.path,
                    parsed_url.params,
                    urllib.parse.urlencode(query_params, doseq=True),
                    node_name
                ))
                domain_configs.append(new_config)
        
        if domain_configs:
            # ایجاد نام فایل بر اساس درخواست شما
            if "nima" in domain:
                file_name = "nima_nodes.txt"
            elif "bpb" in domain:
                file_name = "bpb_nodes.txt"
            else:
                file_name = f"{domain.split('.')[0]}_nodes.txt"
                
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("\n".join(domain_configs))
            print(f"فایل {file_name} با موفقیت در مسیر {os.getcwd()} ذخیره شد.")

if __name__ == "__main__":
    main()
