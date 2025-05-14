<a href="https://ru.hexlet.io/">
<p align="center">
    <img src="images/hexlet_logo.png" 
        width="200" 
        height="200">
</p>
</a>


## Hexlet tests and linter status:
[![Actions Status](https://github.com/Alex-Iset/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Alex-Iset/python-project-83/actions)
[![my-check](https://github.com/Alex-Iset/python-project-83/actions/workflows/my-check.yml/badge.svg)](https://github.com/Alex-Iset/python-project-83/actions/workflows/my-check.yml)


## Tech Stack:
![Static Badge](https://img.shields.io/badge/flask-3.1.0-F?logo=flask&color=black)
![Static Badge](https://img.shields.io/badge/gunicorn-23.0.0-F?logo=gunicorn&color=%23329f5a)
![Static Badge](https://img.shields.io/badge/beautifulsoup4-4.13.4-F?logo=beautifulsoup&color=yellow)
![Static Badge](https://img.shields.io/badge/psycopg2-2.9.10-F?logo=psycopg&color=yellow)
![Static Badge](https://img.shields.io/badge/pythondotenv-1.1.0-F?color=yellow)
![Static Badge](https://img.shields.io/badge/requests-2.32.3-F?logo=requests&color=yellow)
![Static Badge](https://img.shields.io/badge/validators-0.35.0-F?logo=validators&color=yellow)


## Table of contents:
### [1. «Page Analyzer»](#page-analyzer)
### [2. Installing and launch](#installing-and-launch)
### [3. P.S.  If PostgreSQL is not installed](#ps-if-PostgreSQL-is-not-installed)


## «Page Analyzer»:
«Page Analyzer» - this is a website that analyzes the specified pages for SEO suitability by analogy with [PageSpeed Insights](https://pagespeed.web.dev/):
#### [Demo result of the application](https://python-project-83-rsfr.onrender.com/)


## Installing and launch
### 1. Installing dependencies
```
make install
```
### 2. Configuring the database using the initializer file
```
psql -d <database_name> -f database.sql
```
### 3. Project launch (locally)
```
make start
```


## P.S. If PostgreSQL is not installed
### 1. Install PostgreSQL (Ubuntu)
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```
### 2. Start the PostgreSQL service and check that it is working correctly
```
sudo service postgresql start
sudo service postgresql status
```
### 3. Create a database
```
sudo -u postgres createdb <database_name>
```