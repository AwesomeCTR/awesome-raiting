#!/bin/bash

# Пробегаем по всем файлам README
for file in README.*.md; do
    # Извлекаем тему из имени файла
    topic=$(echo $file | sed -e 's/README\.topic_//' -e 's/README\.language_//' -e 's/\.md//')

    # Создаем папку для темы, если она не существует
    mkdir -p "topics/$topic"

    # Перемещаем файл в соответствующую папку с переименованием в README.md
    mv "$file" "topics/$topic/README.md"
done

echo "Файлы перемещены."