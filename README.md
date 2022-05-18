# AMOCRM-ASTERISK-NG

Данная интеграция создана для работы со стандартным для amoCRM виджетом "*Asterisk*".

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
#### Пакеты
+ FFmpeg
+ Redis

## Общий принцип работы
Интеграция представляет собой веб-сервер [uvicorn]("https://www.uvicorn.org/"), который обрабатывает запросы, отправляемые виджетом "Asterisk" со стороны amoCRM. Также интеграция взаимодействует с телефонией через *AMI*.

## Установка
**Руководствуясь документацией вашего дистрибутива.**
Установите *FFmpeg*.
Установите и запустите *Redis*.

Склонируйте репозиторий на свой сервер.
```bash
git clone https://github.com/iqtek/amocrm_asterisk_ng.git /opt/amocrm_asterisk_ng
cd /opt/amocrm_asterisk_ng
```

Создайте и заполните config.yml.
```bash
cp ./configs/config_example.yml ./configs/config.yml
```

Создайте виртуальную среду внутри каталога с интеграцией.
```bash
python3.8 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Запуск

### Первый способ.
Используйте утилиту screen.
```bash
source ./venv/bin/activate
screen python startup.py 
```

### Второй способ.
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
WorkingDirectory=/opt/amocrm_asterisk_ng
ExecStart=/bin/bash /opt/amocrm_asterisk_ng/startup.sh

[Install]
WantedBy=multi-user.target
```
```bash
systemctl start amocrm_asterisk_ng
```

## Принцип  логирования звонков.
После завершения звонка интеграция получает событие *CDR* со стороны AMI на основе уникального идентификатора (unique_id) этого *CDR* генерируется ссылка, по которому файл данной записи будет доступен. Для этого Вам потребуется указать **base_url** в config.yml. Если в amoCRM есть контакт с номером телефона, указанном в *CDR*, то звонок будет залогирован в [аналитике]("https://www.amocrm.ru/support/analytics/sales_analysis"), в противном случае он будет добавлен в *неразобранное* в указанной воронке [подробнее](## Настройка базнес-логики.). 

# Настройка интеграции
Настройки интеграции хранятся в двух файлах .configs/classic_scenario.yml и .configs/config.yml.

1. В .configs/config.yml хранятся основные настройки и доступы к дополнительным системам.
2. В ./configs/classic_scenario.yml содержится конфигрурация бизнес-логики.

## Настройка бизнес-логики.
По умолчанию *./configs/classic_scenario.yml*.

1. Укажите **pipeline_name**. Если звонок невозможно залогировать в [аналитике]("https://www.amocrm.ru/support/analytics/sales_analysis"), по причине отсутствия в системе контакта с таким номером телефона, то звонок будет помещен в *неразобранное* в указанной воронке. Убедитесь, что *неразобранное* включено в этой воронке.
2. Поле **postprocessing_delay** указывает через сколько секунд после фактического завершения звонка он будет залогирован. Это требуется для того, чтобы у оператора было время заполнить карточку клиента или создать соответствующий контакт.
3. Укажите **internal_number_regex** . Интеграция не логирует звонки между внетренними номерами. Номер считается внутренним, если он указан в настройках виджета или соотвествует регулярному выражению.
4. Укажите **source_name**, **source** и т.д. Эти поля используются во время логирования звонка. См [документация amoCRM](https://www.amocrm.ru/developers/content/crm_platform/calls-api)
5. Укажите **internal_number_pattern** - регулярное выражение, которому соотвествуют внутренние номера. (Например, "6\\d\\d" - указывает, что внутренние номера состоят из 3 цифр и первая из них 6). Если данный параметр не указан, то внутренними номерами будут считаться только те, что указаны в конфигурации виджета.

```yaml
call_logging:
  source_name: asterisk_telephony
  source: asterisk_telephony
  source_uid: asterisk_telephony
  service_code: amo_asterisk
  pipeline_name: Воронка
  postprocessing_delay: 1

internal_number_pattern: "6\\d\\d"
```

## Оснвные настройки.

### Настройка интеграции
Создайте **внешнюю** интеграцию в аккаунте amoCRM. Подробнее ["создание внешней интеграции"]("https://www.amocrm.ru/developers/content/oauth/step-by-step"). 

## Настройки amoCRM
1. Укажите **base_url**, для генерации ссылок на записи разговоров.
2. Укажите флаг **enable_conversion**. Если данная настрйка включена, то файлы будут *CDR* будет конфертироваться в mp3 "на лету".
3. Если флаг **enable_conversion** включен, то укажите путь до директории **tmp_directory** в которой будет происходить конвертация. 
4. Заполните настройки интеграции, которую вы создали в amoCRM.

```yaml
crm:
  type: amocrm
  settings:
    storage_prefix: crm
    kernel:
      call_logging:
        enable_conversion: true
        tmp_directory: "./files"
        base_url: https://webhook.iqtek.ru/

      integration:
        integration_id: xxxxxxxx-xxxx-xxxx-xxx-xxxxxxxxxxxx
        secret_key: secret_key
        auth_code: auth_code
        redirect_uri: https://mycompany.ru/
        base_url: https://mycompany.amocrm.ru/
```
### Настройка виджета
Так как интеграция не может обращаться к виджету , Вам придется продублировать его настройки в своем config.yml. Также Вам потребуется указать '"Путь к скрипту" в настройках виджета в интерфейсе amoCRM "https://webhook_url:port/amocrm/calls". 

```yaml
widget:
	type: asterisk_widget
    settings:
        login: login
        password: password
    	users:
            111: my_email@email.ru
            222: someone_mail@email.ru
            333: other_mail@email.ru
```

## Настройка телефонии
В данный момент поддерживается только телефония на базе Asterisk16.
1. Укажите данные для авторизации через *AMI*.
2. Укажите данные для доступа к базе данных, в которой *Asterisk* хранит информацию о *CDR*.
3. Поле **media_root** - путь до файлов с записями разговоров. Данное поле указывается в виде формат-строки, так как файлы *CDR* находятся в файловой системе по пути, зависящем от даты и времени создания данного *CDR*. 
4. Укажите **context** и **timeout** параметры. Данные параметры будут использованы для команды *AMI* [Originate](https://wiki.asterisk.org/wiki/display/AST/Asterisk+16+ManagerAction_Originate).

```yaml
telephony:
  type: asterisk_16
  settings:
    storage_prefix: telephony
    ami:
      host: 127.0.0.1
      port: 5038
      user: user
      secret: secret
    cdr:
      mysql:
        host: 172.27.12.30
        port: 3306
        user: user
        password: password
        database: asteriskcdrdb
      media_root: "/var/spool/asterisk/monitor/%Y/%m/%d/"
    dial:
      context: from-internal
      timeout: 30000
```
#### Настройка БД

Добавить поле для имени файла записи разговора:
```sql
ALTER TABLE `cdr` ADD `recordingfile` VARCHAR(120) NOT NULL;
```
Добавить поле для хранения времени добавления cdr записи:
```sql
ALTER TABLE `cdr` ADD `addtime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```
Установить значение поля для старой записи:
```sql
UPDATE cdr SET addtime=calldate;
```
## Настройка инфраструктуры

### Настройка сервера.
1. Укажите *host* для интеграции.
2. Укажите *port* на котором будет работать интеграция. Обратите внимание, что порт должен совпадать с тем, который указан в **"Путь к скрипту"** в настройках виджета.
```yaml
integration:
  host: 0.0.0.0
  port: 8000
```

### Настройка хранилища.
Хранилище на базе Redis требуется для работы части интеграции, работающей с телефонией. Это требуется для хранения служебной информации.
```yaml
storage:
  type: redis
    settings:
    host: 127.0.0.1
    port: 6379
    database: 1
```

### Настройка логгера.
В данном пункте хранятся настройки стандартной для python библиотеки [logging](https://docs.python.org/3/library/logging.html). Без особой необходимости данные настройки лучше всего не трогать.
