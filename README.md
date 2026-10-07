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
# EasyTier node catalog

`easytier-nodes.txt` supplies candidate bootstrap nodes to the experimental
Windows EasyTier module. Beam validates this bounded HTTPS list, adds built-in
fallback candidates and tests real EasyTier connections before selection.
This list is not a guarantee of uptime, relay permission or streaming speed.
The server saves the chosen common pool in invitations; clients check that pool
without selecting a different network independently. The feed contains only
public node addresses, never Beam accounts, VPN identities or invitation keys.

The current candidates passed isolated no-TUN EasyTier 2.6.4 handshake probes
on 2026-10-08. Operator references:
https://github.com/pmh1314520/MCTier and https://wiki.slarker.me/application/easytier.html.
Update addresses only after protocol verification, then run
`python scripts/check_site.py`. Publishing this data does not publish a Beam
binary release or change the stable downloads.
