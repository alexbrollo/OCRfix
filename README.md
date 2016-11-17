# OCRfix
A simple python script to fix scannos inside djvu text layer

OCRfix.djvu outputs text layer of a djvu file, builds from it the full list of words, and allows a suer to edit them; finally edited words are wrapped again into djvu text layer. 

It works into two steps, step1 and step2.

Needed:
1. a djvu file with a text layer at word detail
2. djvused (DjvuLibre library)
3. a good utf-8 text editor 
