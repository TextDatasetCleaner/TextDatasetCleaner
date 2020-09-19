# Text Dataset Cleaner

Очистка текстовых датасетов от мусора (некорректный язык строк, бранная речь, HTML-теги и т.д.). В данный момент это "грязная" версия данного решения, в которой захардкожен мой пайплайн и подход к очистке. Содержимое этого репозитория "вырвано" из своих наработок в виде "сборной солянки", поэтому в текущий момент 100% работоспособность не гарантируется 🤪

## Запуск

Использовалось на Ubuntu 18.04 с Python 3.7.

Для запуска нужно положить в директорию `datasets/` файл с расширением `.txt` (например, `yahoo_news.txt`) и выполнить команду:

```bash
./run.sh yahoo_news
```

Он проведёт установку зависимостей (через `pip`, глобально!) из файла `requirements.txt` и начнёт пошагово запускать питонячие скрипты для препроцессинга.

## TODO

В идеале хочется собрать всё в виде docker-контейнера, чтоб можно было сделать `docker pull ...`, выставить input и output директории через volume и задать какой-то yaml-подобный файл конфигурации для определения необходимых шагов препроцессинга. А при запуске контейнера чтобы стартовала очистка, которая в итоге брала все файлы из input-директории и собирала результаты в output.

К существующим скриптам препроцессинга хочется допилить:

- [ ] Проверку и исправление орфографии через standalone-версию [LanguageTool](https://github.com/languagetool-org/languagetool)
- [ ] Исправление знаков пунктуации в строках
- [ ] Сделать анализ тональности и удалять негативные строки
- [ ] Попробовать прикрутить классификацию тематики текста
- [ ] Удаление знаков препинания
- [ ] Понижение регистра (если вдруг кому-то это нужно)
- [ ] Сделать удаление нечётких дубликатов через шинглы (лучше через какое-то готовое решение)
- [ ] Удаление всех строк, которые содержат стоп-слова из заданного словаря
- [ ] Проверка метрик читаемости текста (через [pattern.metrics](https://www.clips.uantwerpen.be/pages/pattern-metrics) или [ruTS](https://github.com/SergeyShk/ruTS))
- [ ] Оценка натуральности/логичности текста через [BERT (режим №2)](https://colab.research.google.com/github/blade1780/bert/blob/master/BERT.ipynb)
- [ ] Использование готовых API для проверки орфографии через Google/Bing
- [ ] Прикрутить использование RAMDisk для ускорения обработки
- [ ] Загрузка процессоров из других директорий (чтобы не форкать реп, если нужно прикрутить свой)
- [ ] Удаление emoji

## Contribute?

Хочется что-то предложить или поделиться своим опытом? - Welcome in issues! Мы будем рады обсудить ваши идеи и опыт ;-)

Вы тоже понимаете, что сейчас нет "серебряной пули" для решения такого рода задачи и абсолютно каждый городит что-то своё? - Присылайте PR, давайте сделаем вместе что-то прекрасное и полезное для всего DS-сообщества!
