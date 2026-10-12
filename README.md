# Beam — сайт и скачивания

Публичный сайт: https://jughodorf.github.io/beam-site/

Статический сайт без npm-зависимостей, трекеров и клиентских токенов. Программы
и соответствующие исходники размещаются в Releases этого репозитория.

Основные исходники Beam и история разработки находятся в отдельном репозитории;
его видимость сайт не меняет. GitHub Pages автоматически публикует статические
файлы из ветки `main`. В этом репозитории находятся только публичные файлы.

## Локальная проверка

```bash
python3 scripts/check_site.py
node --check assets/site.js
python3 -m http.server 4347 --bind 127.0.0.1
```

Откройте http://127.0.0.1:4347/. Проверьте главную страницу, выбор Android APK,
мобильную ширину и страницу исходников. Прямые ссылки проверяются после публикации
Releases, сверяются размеры и SHA-256.

## Новая версия

Публикуйте подписанные файлы без изменения их байтов, контрольные суммы и
соответствующие исходники. Затем обновите ссылки, версии и размеры в `index.html`,
`assets/site.js`, `sources.html` и `downloads.json`. Перед push выполните локальную
проверку. Ключи подписи и пароли никогда не загружаются сюда.

Программы и сайт — GPL-3.0. Авторские уведомления программ сохранены в архивах.

## Предварительный выпуск EasyTier

Раздел `#easytier` содержит Server 2.2.1, Windows Client 2.2.1, общий
установщик 2.2.1, модуль 0.1.4 и Android 2.2.1.
Release `v2.2.1-preview` остаётся prerelease.
Архив Windows соответствует коммиту 8000505803f4db1f37ddfba0920f3dca063177f8.
Закреплённые подмодули, патчи и инструкции сборки включены; соответствующие
исходники native-модуля и helper доступны отдельным архивом 0.1.4.
В `downloads.json` зафиксированы размеры и SHA-256. Старые файлы сохранены.
Основной репозиторий остаётся закрытым.

ID-вход использует прежних пользователей и права. Ключ сети выводится из
публичного ID: пароль защищает вход Beam, но не исключает сетевой DoS/DHCP.
Для закрытой группы остаётся секретное приглашение. Android 2.2.1 принимает ID на Android 7.0+; приглашения сохраняются.
Кодеки, очереди, FEC и исходный звуковой тракт в этом выпуске не менялись.
Периодические лаги в Wi-Fi/играх не воспроизведены и не объявлены устранёнными.
Реальная установка нового пакета требует проверки на отдельном ПК/VM.

Клиент 2.0.11 использует `downloads.json` для проверки и скачивания обновлений:
`files` — стабильный канал, `preview.files` — тестовый канал по выбору пользователя.
Сохраняйте точные имя, tag, URL, размер и SHA-256 каждого EXE. Установка остаётся
ручной; скачивание и проверка приостанавливаются на время сеанса.

Проверки эмуляторов и UDP-буфера не подтверждают плавность настоящего
WAN-видеосеанса; до проверки на физических устройствах не объявляйте этот
комплект стабильной 2.1. Обмен двух разных физических мониторов, HDR/SDR и игры
также требуют аппаратной проверки. При замене файлов сверяйте и удалённые SHA-256,
и размеры, затем проверяйте выбор APK и отсутствие переполнения страницы
на телефоне. Веб-интерфейс не должен получать приглашения или ключи сети.

# EasyTier node catalog

`easytier-nodes.txt` supplies candidate bootstrap nodes to the experimental
Windows EasyTier module. Beam validates this bounded HTTPS list, adds built-in
fallback candidates and tests real EasyTier connections before selection.
This list is not a guarantee of uptime, relay permission or streaming speed.
The server saves the chosen common pool in invitations; clients check that pool
without selecting a different network independently. The feed contains only
public node addresses, never Beam accounts, VPN identities or invitation keys.

The six current candidates passed isolated no-TUN EasyTier 2.6.4 handshake
probes on 2026-10-11; availability varied between repeated checks. Beam uses
six common anchors and at most two additional distinct hostnames; a 256-entry
catalog is capacity, not a guarantee or automatic scan of 256 nodes. Operator references:
https://github.com/pmh1314520/MCTier, https://wiki.slarker.me/application/easytier.html
and https://easytier.dreamlife.indevs.in/.
Update addresses only after protocol verification, then run
`python scripts/check_site.py`. Publishing this data does not publish a Beam
binary release or change the stable downloads.

## Главный вариант скачивания

Основной установщик Windows — BeamSetup-2.2.1.exe в карточке #beam-installer.
Кнопки «Скачать Beam» ведут к нему; отдельные сервер, клиент и модуль
доступны в раскрываемом разделе #separate-installers. Android 2.2.1
доступен рядом, в пяти ABI; клиент и сервер обновлены; исходный медиатракт сохранён.
Архив Android соответствует коммиту 8000505803f4db1f37ddfba0920f3dca063177f8.

## Выпуск 2.2.1

Windows Client 2.2.1 / Server 2.2.1, Android 2.2.1, EasyTier 0.1.4.
Общий установщик остаётся основным, отдельные компоненты — дополнительными.
Коммит Windows 8000505803f4db1f37ddfba0920f3dca063177f8; Android 8000505803f4db1f37ddfba0920f3dca063177f8.
Предварительный канал сохранён. Установка на реальные компьютеры при подготовке не выполнялась.
