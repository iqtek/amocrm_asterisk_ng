# _AMOCRM-ASTERISK-NG_

Интеграция телефонии на базе _Asterisk16_ и _amoCRM_. С поддержкой:
+ стандартного виджета _Asterisk_;
+ нового виджета _AsteriskNG_;
+ переадресации на отвественного;
+ логирования звонков;

## Требования
  + Роутер с поддержкой Hairpin NAT (перенаправление пакетов LAN->WAN->LAN)
  + Либо: локальный DNS сервис
  + Желательно - статический IP
  + SSL сертификат (платный, letsencrypt)
  + Домен с настроенной DNS записью вашего статического IP
  + Интернет >1Mbps

#### Технические требования к платформе Asterisk: 
  * Поддержка AMI
  * Работа вебсервера с поддержкой протокола httpsSmall Refactoring.
  * Сервер с Asterisk в одной сети с интеграцией
#### Зависимости
+ FFmpeg
+ Redis


## Общий принцип работы
Интеграция представляет собой веб-сервер [uvicorn]("https://www.uvicorn.org/"), который обрабатывает запросы, отправляемые виджетами со стороны amoCRM. Также интеграция взаимодействует с телефонией через *AMI*.

## Установка

**Руководствуясь документацией вашего дистрибутива.**
Установите *FFmpeg*.
Установите и запустите *Redis*.

Склонируйте репозиторий на свой сервер.
```bash
git clone https://github.com/iqtek/amocrm_asterisk_ng.git /opt/amocrm_asterisk_ng
cd /opt/amocrm_asterisk_ng
```

Создайте виртуальную среду внутри каталога с интеграцией.
```bash
python3.8 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
mkdir logs
```
Создайте и заполните config.yml.
```bash
cp ./configs/config_example.yml ./configs/config.yml
```

Добавьте поле в таблицу _CDR_  для имени файла записи разговора:
```sql
ALTER TABLE `cdr` ADD `recordingfile` VARCHAR(120) NOT NULL;
```

## Запуск

### Запуск через _screen_ .
```bash
source ./venv/bin/activate
screen python -m asterisk_ng
```

### Запуск через Systemd.
Используйте systemd unit.
Создайте файл */usr/lib/systemd/system/amocrm_asterisk_ng.service* и заполните его так как указано ниже.

```
Description=AmoCRM and Asterisk Integration
After=syslog.target
After=network.target
After=mysql.service
After=redis.service

Requires=mysql.service
Requires=redis.service

[Service]
Type=simple
WorkingDirectory=/srv/amocrm_asterisk_ng
ExecStart=/bin/bash -c  'source ./venv/bin/activate && python -m asterisk_ng --config ./config.yml'
ExecReload=/bin/kill -s HUP $MAINPID

KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target
```
Запустите сервис.
```bash
systemctl start amocrm_asterisk_ng
```

Проверить запущена ли интеграция можно через _Swagger_ по адресу _127.0.0.1:8000/docs_.



# Настройка интеграции

Создайте config.yml.
```bash
cp config.example.yml config.yml
```

Конфигурационный файл разделен на два блока:
+ Статическая конфигурация 
+ Конфигурация плагинов

В блоке статической конфигурации описаны настройки стандартной для python библиотеки [logging](https://docs.python.org/3/library/logging.html). Без особой на то необходимости данные настройки лучше всего не трогать.

В начале блока конфигурации плагинов указывается список (_uploaded_) плагинов, которые будут загружены. На данный момент менять порядок загрузки нельзя. 

```yaml
uploaded:
    - "system.converter"
    - "system.storage"
    - "system.fastapi"
    - "amocrm.amoclient"
    - "amocrm.functions"
    - "amocrm.records.provider"
    - "amocrm.widget.asterisk"
    - "telephony.ami_manager"
    - "telephony.asterisk16.reflector"
    - "telephony.asterisk16.functions"
    - "standard.domain"
    - "telephony.redirecting"
    - "telephony.records_provider"
    - "amocrm.widget.asterisk_ng"
```
##### Плагины

###### standard.domain
Данный плагин реализует бизнес-логику приложения.
```yaml
"standard.domain":
  # Соответствие агентов и их внутренних номеров.
  agents: 
    "username@email.ru": 613
    "username_1@email.ru": 610
  # Ответственный по умолчанию
  responsible_agent: "director@email.ru" 

  # Преобразователь номеров телефонов клиентов.
  client_corrector:
    - ["^\\+?7(\\d{10})$", "8\\g<1>"] # [Pattern, Substitution]
```
Корректоры работают как конвеер, можно указать сразу несколько и они объединятся в цепочку. Указанный в примере корректор заменяет префикс номера на 8. Данная функция полезна, чтобы номера добавляемые в AmoCRM были однотипны.

###### amocrm.amoclient
Создайте **внешнюю** интеграцию в аккаунте amoCRM. Подробнее ["создание внешней интеграции"]("https://www.amocrm.ru/developers/content/oauth/step-by-step").
```yaml
"amocrm.amoclient":
  backup_file_path: "./credentials.txt"
  encryption_key: "asterisk_ng"
  integration_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  secret_key: "secret_key"
  auth_code: "auth_code"
  base_url: "https://mycompany.amocrm.ru/"
  redirect_uri: "https://mycompany.ru/"
```

###### amocrm.functions
Плагин отвечающий за логирование звонка в amoCRM. Подробнее параметры описаны в [документации]("https://www.amocrm.ru/developers/content/telephony/calls_add").
Если в amoCRM есть контакт с номером телефона, указанном в *CDR*, то звонок будет залогирован в [аналитике]("https://www.amocrm.ru/support/analytics/sales_analysis"), в противном случае он будет добавлен в *неразобранное* в указанной воронке. 
```yaml
"amocrm.functions":
    pipeline: "Воронка" # Имя воронки, для неразобранных звонков.
    source: "AsteriskNG"
    source_uid: "AsteriskNG"
    source_name: "AsteriskNG"
    service_code: "AsteriskNG"
```

###### amocrm.records.provider
Плагин отвечающий за предоставление записей разговоров по _REST_. 
Флаг *enable_conversion* отвечает за то, будут ли записи конвертироваться в _mp3_на лету.
Поле *base_url*, состоит из доменного имени сервера, на котором запущена интеграция + _/records_. 
В amoCRM, будет добавлена ссылка на звонок вида _https://domain.com/records/{unique_id}_.

```yaml
"amocrm.records.provider":
  base_url: https://webhook.api.ru/records
  enable_conversion: true
```
###### amocrm.widget.asterisk 
Плагин стандартного виджета _Asterisk_.
```yaml
"amocrm.widget.asterisk":
    login: "login"
    password: "password"
```
###### amocrm.widget.asterisk_ng
Плагин нового  виджета [AsteriskNG]("https://github.com/iqtek/asterisk_ng").
```yaml
"amocrm.widget.asterisk_ng":
    secret_key: "AsteriskNG"
```

###### telephony.ami_manager
Плагин для работы с _AMI_.
```yaml
"telephony.ami_manager":
  user: admin
  host: 127.0.0.1
  port: 5038
  secret: secret
```

###### telephony.asterisk16.functions
Плагин управления телефонией. Указанные поля будут использованы для команд *AMI* [Originate](https://wiki.asterisk.org/wiki/display/AST/Asterisk+16+ManagerAction_Originate) и  [Redirect](https://wiki.asterisk.org/wiki/display/AST/Asterisk+16+ManagerAction_Redirect).
```yaml
"telephony.asterisk16.functions":
    origination_context: from-internal
    origination_timeout: 30000
    redirect_context: from-internal
```

###### telephony.asterisk16.reflector
Плагин трансляции событий _AMI_ в события о статусах звонков.
Поле _internal_number_pattern_ - паттерн для имени канала c одной группой - содержащей внутренний номер. В данном примере, внутрениий номер состоит из 3 чисел и начинается с SIP или PJSIP.

```yaml
"telephony.asterisk16.reflector":
  internal_number_pattern: "(?:SIP|PJSIP)/(\\d\\d\\d)\\D"
```

###### telephony.records_provider
Плагин отвечающий за пролучение файла записи по его _unique_id_.  Поле **media_root** - путь до файлов с записями разговоров. Данное поле указывается в виде формат-строки, так как файлы *CDR* находятся в файловой системе по пути, зависящем от даты и времени создания данного *CDR*.
```yaml
"telephony.records_provider":
  mysql:
    host: 127.0.0.1
    port: 3306
    user: user
    password: password
    database: asteriskcdrdb
  cdr_table: cdr
  calldate_column: calldate
  recordingfile_column: "recordingfile"
  media_root: "/var/spool/asterisk/monitor/%Y/%m/%d/"
```

###### system.storage
Плагин предоставляющий  _Redis_. Хранилище на базе Redis требуется для хранения служебной информации, во время работы с телефонией.
```yaml
"system.storage":
  host: 127.0.0.1
  port: 6379
  database: 0
```

###### system.fastapi
Плагин запускающий веб-сервер и _Swagger_.
```yaml
"system.fastapi":
  host: 0.0.0.0
  port: 8000
  workers: 1
```

###### system.system.converter
```yaml
Плагин для конвертации аудиофайлов средствами FFmgeg.
"system.converter":
  tmp_dir: ./tmp # Директория для конвертации.
```
