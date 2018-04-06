"""Busca y cuenta el número de archivos en un directorio."""

# -*- coding: utf-8-sig -*-

import os
import fnmatch
import pandas
import word_count
import textract
from nltk.tokenize import word_tokenize

cwd = os.getcwd()


def crawler(filetype='*'):
    """Prototype crawler function."""
    for file in os.listdir(cwd):
        if fnmatch.fnmatch(file, '*.' + filetype):
            print(file)

def crawler2():
	"""Slightly improved version."""
    flist = [(folders, files) for folders, dirs, files in os.walk(cwd, topdown=False)]
    nlist = []
    for folder, filenames in flist:
        for files in filenames:
            nlist.append((folder, files))
    df = pandas.DataFrame(nlist, columns=['direccion', 'archivo'])
    df.to_csv('test.csv', encoding='utf-8-sig')
    return(df)


def crawler3():
	"""Working version. Crawls through all folders contained from where executed. Use if textract not available."""
    flist = [(folders, file) for folders, dirs, file in os.walk(cwd, topdown=False)]
    nlist = []
    for folder, filenames in flist:
        for file in filenames:
            wcount = 0
            pcount = 0
            # print('testing: ', file)
            if fnmatch.fnmatch(file, '*.pdf'):
                pcount= word_count.getPageCount(folder + '/' + file)
                wcount = word_count.countwords(folder + '/' + file)
            nlist.append((folder, file, wcount, pcount))
            print(file, ' added, with ', wcount, ' words and ', pcount, ' pages.')
    df = pandas.DataFrame(nlist, columns=['direccion', 'archivo', 'palabras', 'hojas'])
    df.to_csv('test.csv', encoding='utf-8-sig')
    return(df)


def crawler4():
    """Easily 10x faster than crawler3 and infinitely more accurate, but requires textract."""
    flist = [(folders, file) for folders, dirs, file in os.walk(cwd, topdown=False)]
    nlist = []
    for folder, filenames in flist:
        for file in filenames:
            wcount = 0
            pcount = 0
            if fnmatch.fnmatch(file, '*.pdf'):
                pcount= word_count.getPageCount(folder + '/' + file)
                wcount = len(word_tokenize(textract.process(folder + '/' + file).decode('latin-1')))
            nlist.append((folder, file, wcount, pcount))
            print(file, ' added, with ', wcount, ' words and ', pcount, ' pages.')
    df = pandas.DataFrame(nlist, columns=['direccion', 'archivo', 'palabras', 'hojas'])
    df.to_csv('test.csv', encoding='utf-8-sig')
    return(df)
