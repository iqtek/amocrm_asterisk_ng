# AMOCRM-ASTERISK-NG

Данная интеграция создана для работы со стандартным для amoCRM виджетом "*Asterisk*".

## Требования

  + Роутер с поддержкой Hairpin NAT (перенаправление пакетов LAN->WAN->LAN)
  + Либо: локальный DNS сервис
  + Желательно - статический IP;
  + SSL сертификат (платный, letsencrypt)
  + Домен с настроенной DNS записью вашего статического IP
  + Интернет >1Mbps

#### Технические требования к платформе Asterisk: 
  * Поддержка AMI
  * Работа вебсервера с поддержкой протокола https
  * Сервер с Asterisk в одной сети с интеграцией
#### Пакеты
+ FFmpeg


## Общий принцип работы
Интеграция представляет собой веб-сервер [uvicorn]("https://www.uvicorn.org/"), который обрабатывает запросы, отправляемые виджетом "Asterisk" со стороны amoCRM. Также интеграция взаимодействует с телефонией через *AMI*.

## Логирование звонков
После завершения звонка интеграция получает событие *CDR* со стороны AMI на основе уникального идентификатора (unique_id) этого *CDR* генерируется ссылка, по которому файл данной записи будет доступен. Для этого Вам потребуется указать **base_url** в config.yml. Если в amoCRM есть контакт с номером телефона, указанном в *CDR*, то звонок будет залогирован в [аналитике]("https://www.amocrm.ru/support/analytics/sales_analysis"), в противном случае он будет добавлен в *неразобранное* в указанной воронке [подробнее](#настройка-рабочего-процесса). 


## Установка
Установите FFmpeg.
```bash
sudo apt install ffmpeg
```
Установите и запустите *Redis*.
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis.service
```
Установите и запустите *RabbitMQ*.
	Руководствуйтесь документацией по установке вашего дистрибутива.

Склонируйте репозиторий на свой сервер.
```bash
git clone https://github.com/iqtek/amocrm_asterisk_ng.git
cd amocrm_asterisk_ng
```

Создайте и заполните config.yml.
```bash
cp config_example.yml config.yml 
```

Создайте виртуальную среду внутри каталога с интеграцией и активируйте ее.
```bash
python3 -m venv venv 
source ./venv/bin/activate
```

Установите необходимые зависимости.
```bash
pip install -r requirements.txt
```

## Запуск
```bash
screen python startup.py 
```

# Настройка интеграции

## Настройки amoCRM

### Настройка рабочего процесса

1. Укажите **pipeline_id**. Если звонок невозможно залогировать в [аналитике]("https://www.amocrm.ru/support/analytics/sales_analysis"), по причине отсутствия в системе контакта с таким номером телефона, то звонок будет помещен в *неразобранное* в указанной воронке. Идентификатор воронки вы можете получить из ссылки вида "account.amocrm.ru/leads/pipeline/\*\*\*\*\*\*", где на месте звездочек будет указан требуемый идентификатор. Убедитесь, что *неразобранное* включено в этой воронке.

2. Укажите **base_url**, для генерации ссылок на записи разговоров.

3. Поле **postprocessing_delay** указывает через сколько секунд после фактического завершения звонка он будет залогирован. Это требуется для того, чтобы у оператора было время заполнить карточку клиента или создать соответствующий контакт.

4. Укажите **tmp_directory**  в  этой диретории будет происходить конвертирование файлов записей в другой формат. Дело в том, что amoCRM требует файлы формата *mp3*, в то время как *Asterisk* в основном хранит записи в формате *wav*.

5. Укажите **storage_prefix** для телефонии и amoCRM. **Storage_prefix** требуется для разрешения коллизии имен ключей в *Redis*. Данные поля не обязательны для заполнения.

6. Укажите **internal_number_regex** . Интеграция не логирует звонки между внетренними номерами. Номер считается внутренним, если он указан в настройках виджета или соотвествует регулярному выражению.

### Настройка интеграции
Создайте **внешнюю** интеграцию в аккаунте amoCRM. Подробнее ["создание внешней интеграции"]("https://www.amocrm.ru/developers/content/oauth/step-by-step"). Вам требуется только ее зарегистрировать, *access* и *refresh* токены будут созданы автоматически и сохранены в *Redis*.

### Настройка виджета
Так как интеграция не может обращаться к виджету , Вам придется продублировать его настройки в своем config.yml. Также Вам потребуется указать '"Путь к скрипту" в настройках виджета в интерфейсе amoCRM "https://webhook_url:port/amocrm/calls". 

```yaml
crm:
  type: amocrm
  settings:
    storage_prefix: crm
    kernel:
      call_logging:
       internal_number_regex: "regex"
        tmp_directory: "./convert_dir"
        base_url: https://webhook.mycompany.ru/
        source: asterisk_telephony
        source_uid: asterisk_telephony
        service_code: amo_asterisk
        pipeline_id: 4672053
        postprocessing_delay: 10

      integration:
        integration_id: xxxxxxxx-xxxx-xxxx-xxx-xxxxxxxxxxxx
        secret_key: secret_key
        auth_code: auth_code
        redirect_uri: https://mycompany.ru/
        base_url: https://mycompany.amocrm.ru/

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

3. Поле **media_root** записываются в виде формат-строки, так как файлы *CDR* находятся в файловой системе по пути, зависящем от даты и времени создания данного *CDR*. 

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
## Настройка инфраструктуры

### Настройка сервера
1. Укажите *host* для интеграции.
2. Укажите *port* на котором будет работать интеграция. Обратите внимание, что порт должен совпадать с тем, который указан в "Путь к скрипту" в настройках виджета.
```yaml
integration:
  host: 0.0.0.0
  port: 8000
```

### Настройка шины сообщений
Шина сообщений требуется для отказоустойчивой работы интеграции. Например, если amoCRM будет недоступна в течении некоторого времени, то звонки все равно будут залогированы, когда amoCRM восстановится.

```yaml
message_bus:
    type: rabbitmq
    settings:
      rabbitmq:
        host: "127.0.0.1"
        port: 5672
        login: guest
        password: guest
        virtualhost: '/'
        ssl: false
        login_method: PLAIN
      exchange_name: asterisk_amocrm_ng_exchange
      exchange_type: direct
      queue_name: asterisk_amocrm_ng
      routing_key: asterisk_amocrm_ng
```
### Настройка шины событий
Шины событий работет на основе шины сообщений. Требуется указать количество потребителей сообщений (workers). Чем больше потребителей, тем быстрее будет работать интеграция.
```yaml
event_bus:
  type: extended
  settings:
    workers: 1
```

### Настройка хранилища
Хранилище на базе Redis требуется для работы части интеграции, работающей с телефонией. В хранилище будет хратится служебная информация, а также  *access* и *refresh* токены.

```yaml
storage:
  type: redis
    settings:
    host: 127.0.0.1
    port: 6379
    database: 1
```
