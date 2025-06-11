# Управление DJI Ronin RS3 Pro через CAN

Этот репозиторий содержит пример скрипта и инструкций для Raspberry Pi 5 c 
шляпой Spotpear 2-channel CAN HAT Plus. Скрипт получает команды с приёмника ELRS 
и передаёт их в стабилизатор DJI через шину CAN.

## Подготовка Raspberry Pi
1. Скопируйте `setup_pi.sh` на Raspberry Pi и запустите:
   ```bash
   chmod +x setup_pi.sh
   ./setup_pi.sh
   ```
   Скрипт установит необходимые пакеты, включит интерфейсы SPI и CAN, 
   добавит оверлеи MCP2515. После завершения перезагрузите систему.

2. Проверьте, что интерфейсы `can0` и `can1` появились командой:
   ```bash
   ip -details link show can0
   ```

## Запуск скрипта
1. Скопируйте `dji_can_control.py` в домашнюю директорию пользователя `pi` и
   сделайте его исполняемым:
   ```bash
   chmod +x dji_can_control.py
   ```

2. При необходимости измените в скрипте параметры `SERIAL_PORT`, `BAUD_RATE` и
   `CAN_CHANNEL` под вашу конфигурацию приёмника и шины.

3. Для автоматического старта создайте службу systemd:
   ```bash
   sudo cp dji_can_control.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable dji_can_control.service
   sudo systemctl start dji_can_control.service
   ```

После перезагрузки Raspberry Pi будет автоматически принимать команды с пульта
и отправлять их на стабилизатор.

> **Важно**: пример кода минимальный и может потребовать доработки под вашу
> аппаратную конфигурацию и протокол DJI Focus Wheel.
