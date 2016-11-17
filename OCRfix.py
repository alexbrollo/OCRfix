#!/usr/bin/python
# -*- coding: utf-8  -*-


import os,shutil,sys,urllib,re,argparse



def dsedExtr(djvuBase):
        dsed=unicode(open(dsedBase+".dsed").read(),"utf-8")
        print len(dsed)
        return
def cleanup(djvuBase):
        dsed=unicode(open(djvuBase+".dsed").read(),"utf-8").split("\n")


        return
def search(djvuBase):
        command='djvused -u "%s" -e output-txt > "%s"' % (djvuBase+".djvu",djvuBase+".dsed")
        print "Comando: ",command
        result=os.system(command)
        print "Risultato: ",result
        regex = ur"\d+ \d+ \d+ \d+ \"(.+)\"\)"
        lista=[]
        dsed=unicode(open(djvuBase+".dsed").read(),"utf-8")

        matches = re.finditer(regex, dsed, re.MULTILINE)

        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1
            
            # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
            
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                
                t=match.group(groupNum)
                
                if not t in lista:
                        
                        lista.append(t)
                        if len(lista)%5000==0:
                                print "Memorizzate ",len(lista), " parole"

        # Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
        lista.sort()
        testo="\n".join(lista)
        open(djvuBase+".txt","w").write(testo.encode("utf-8"))
        open(djvuBase+"_fix.txt","w").write(testo.encode("utf-8"))
        return "fatto"

def diff(djvuBase):
        fwrong=unicode(open(djvuBase+".txt").read(),"utf-8").split("\n")
        fright=unicode(open(djvuBase+"_fix.txt").read(),"utf-8").split("\n")
        
        if len(fwrong)!=len(fright):
                print "I file di correzione non corrispondono per numero di parole"
                return
        l=[]
        for i in range(len(fwrong)):
                if fwrong[i]!=fright[i]:
                        l.append(fwrong[i]+"\t"+fright[i])
        open(djvuBase+"_diff.txt","w").write(("\n".join(l)).encode("utf-8"))
        return 

def fixDjvu(djvuBase):
        lista=unicode(open(djvuBase+"_diff.txt").read(),"utf-8").split("\n")
        dsed=unicode(open(djvuBase+".dsed").read(),"utf-8")
        for i in range(len(lista)):
                parola=lista[i].split("\t")
                if len(parola)==2 and len(parola[0])>0:
                        dsed=dsed.replace('"'+parola[0]+'"','"'+parola[1]+'"')
                        # print "sostituzione ",parola[0]," -> ",parola[1]
        open(djvuBase+".dsed","w").write(dsed.encode("utf-8"))
        comando="djvused %s.djvu -f  %s.dsed -s" %(djvuBase,djvuBase)
        os.system(comando)
        print "Edited words has been uploaded into %s" % (djvuBase+".djvu")
        return

def step1(djvuBase):
        search(djvuBase)
        print '''Please open the file %s and edit it with a utf-8 text editor.
Don't change the number of rows!
Finally save the file and run step 2''' % (djvuBase+"_fix.txt")
        return

def step2(djvuBase):
        diff(djvuBase)
        fixDjvu(djvuBase)
        return "Done"

def path2url(path):
        return urlparse.urljoin('file:', urllib.pathname2url(path))
        
def cleanfolder(dirpath):
        for filename in os.listdir(dirpath):
                filepath = os.path.join(dirpath, filename)
                try:
                        shutil.rmtree(filepath)
                except OSError:
                        os.remove(filepath)
        return



# utilities 
# Nuova versione, gestisce i tag annidati; x e' la parte "aspecifica" del
# tag di apertura (es: {{ cercando {{Intestazione| )
def find_stringa(stringa,idi,idf,dc=0,x=None,side="left"):
    if side=="right":
        idip=stringa.rfind(idi)
    else:
        idip=stringa.find(idi)
    idfp=stringa.find(idf,idip+len(idi))+len(idf)
    if idip>-1 and idfp>0:
        if x!=None:
            while stringa[idip:idfp].count(x)>stringa[idip:idfp].count(idf):
                if stringa[idip:idfp].count(x)>stringa[idip:idfp].count(idf):
                    idfp=stringa.find(idf,idfp)+len(idf)
                
        if dc==0:
            vvalore=stringa[idip+len(idi):idfp-len(idf)]
        else:
            vvalore=stringa[idip:idfp]
    else:
        vvalore=""
    return vvalore

def produci_lista(testo,idi,idf,dc=1,inizio=None):
    t=testo[:]
    lista=[]
    while not find_stringa(t,idi,idf,1,inizio)=="":
        el=find_stringa(t,idi,idf,1,inizio)
        t=t.replace(el,"",1)
        if dc==0:
            el=find_stringa(el,idi,idf,0,inizio)
        lista.append(el)
    return lista

def carica_pcl(nome_file, folder="dati/"):
    nome_file=folder+nome_file+".pcl"
    f=open(nome_file)
    contenuto=pickle.load(f)
    f.close()
    return contenuto

def salva_pcl(variabile,nome_file="dato",folder="dati/"):
    nome_file=folder+nome_file+".pcl"
    f=open(nome_file,"w")
    pickle.dump(variabile, f)
    f.close()
    print "Variabile salvata nel file "+nome_file
    return 

def main(djvuBase, step):
        print "Parametri: ",djvuBase, step
        if step=="step1":
                step1(djvuBase)
        if step=="step2":
                step2(djvuBase)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scarica, modifica e ricarica l'elenco delle parole di un file djvu")

    parser.add_argument('djvuBase', help="nome base del file djvu")

    parser.add_argument('step', help='azione (step1|step2)')
    

    args = parser.parse_args()

    main(args.djvuBase,args.step)
