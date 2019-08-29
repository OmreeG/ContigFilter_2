#!/bin/bash

name_of_repository=ContigFilter_2
echo "# $name_of_repository" >> README.md
git init
git add .
git commit -m 'Initial commit'
git remote add origin https://github.com/OmreeG/{$name_of_repository}.git
git push -u origin master


