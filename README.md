# crtsh_dump
Small script that is used to extract subdomains of a specified domain by scraping https://crt.sh. The result are going to be written in an *.CSV* file for easier analysis.

Download repo & install requirements :

```
git clone https://github.com/Darktortue/crtsh_dump.git

pip install -r requirements.txt
```

Script usage :
```
python crtsh.py --help
usage: crtsh.py [-h] [-c] domain

Fetch SSL certificates from crt.sh and write the result to a CSV file.

positional arguments:
  domain       The domain to fetch SSL certificates for.

options:
  -h, --help   show this help message and exit
  -c, --check  Check if the domain/subdomains are available.
```