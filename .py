# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:13:17 2016

@author: U115-H016
"""

import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QWidget, QPushButton, QApplication, QFileDialog, QMessageBox
from PyQt4.QtCore import Qt, SIGNAL, SLOT, QTranslator, QLocale, QLibraryInfo
import os
from interpo_lineaire_DOY16jours import interpo_lineaire_DOY16jours
from decoupage_et_serie_temporelle import decoupage_et_serie_temporelle
from function_data_raster import*
from metriquePheno import*


qtCreatorFile = "pheno1.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        
        self.setupUi(self)
        self.pushButton_cheminNDVI.clicked.connect(self.accesRepertoireNdvi)
        self.pushButton_cheminDOY.clicked.connect(self.accesRepertoireDoy)
        self.pushButton_cheminOut.clicked.connect(self.accesCheminSave)
        self.pushButton_cheminNDVI_metrique.clicked.connect(self.accesRepertoireNdviMetrique)
        self.pushButton_cheminNDVI_metrique_fichier.clicked.connect(self.accesFichierNdviMetriqueMultiannuelle)
        self.pushButton_cheminOut_metrique.clicked.connect(self.accesCheminSaveMetrique)

        self.pushButton_cheminZoneEtudes.clicked.connect(self.accesZoneEtudes)
        self.pushButton_execution.clicked.connect(self.validation)
        self. pushButton_execution_metrique.clicked.connect(self.validationMetrique)
       
        
        self.closePretraitement.clicked.connect(self.quit)
        self.closeMetrique.clicked.connect(self.quit)
        
        self.radioButton_DOY.clicked.connect(self.selectionDOY)
        self.radioButton_NDVI.clicked.connect(self.selectionNDVI)


            
    

    def accesRepertoireNdvi(self):

        """
        @brief cette fonction permet de selectionner le lien du repertoire
        dans lequel se trouve le NDVI
       
        
        """
        ndviPath = QFileDialog.getExistingDirectory(self,u'Repertoire du NDVI','.')
          
        if ndviPath:
          
          self.cheminNDVI.setText(ndviPath)
          
    def accesRepertoireNdviMetrique(self):
        
        """
        @brief cette fonction permet de selectionner le lien du repertoire
        dans lequel se trouve le NDVI
       
        
        """
        ndviPath = QFileDialog.getExistingDirectory(self,u'Repertoire du NDVI','.')
          
        if ndviPath:
          
          self.cheminNDVI_metrique.setText(ndviPath)

    def accesFichierNdviMetriqueMultiannuelle(self):
        
        """
        @brief cette fonction permet de selectionner le lien du repertoire
        dans lequel se trouve le NDVI       
        
        """
        ndviPath = QFileDialog.getOpenFileName(self, 
                                            u"Ouvrir le fichier NDVI multiannuelle", 
                                            u"/home/puiseux/images", 
                                            u"Images (*.tif )")
          
        if ndviPath:
          
          self.cheminNDVI_metriqueFichier.setText(ndviPath)
              
              
    def accesRepertoireDoy(self):
        
        """
        !@brief  cette fonction permet de selectionner le lien du repertoire
        dans lequel se trouve le DOY

        """
        
        
        doyPath = QFileDialog.getExistingDirectory(self,u'Repertoire du DOY','.')
          
        if doyPath:
          
          self.cheminDOY.setText(doyPath)

    def accesCheminSave(self,var):
        """
        /*********************************************************
        !@brief
        cette fonction permet de selectionner le repertoire d'enregistrement des fichiers
        *********************************************************/
        
        """
        savePath = QFileDialog.getExistingDirectory(self,u'Repertoire d''enregistrement','.')
              
        if savePath:
                      
                      self.cheminOut.setText(savePath)
    def accesCheminSaveMetrique(self,var):
        """
        /*********************************************************
        !@brief
        cette fonction permet de selectionner le repertoire d'enregistrement des fichiers
        *********************************************************/
        
        """
        savePath = QFileDialog.getExistingDirectory(self,u'Repertoire d''enregistrement des parametres','.')
                  
        if savePath:
                      
                      self.cheminOut_metrique.setText(savePath)



    def accesZoneEtudes(self):
        """
        /*********************************************************
        !@brief
        cette fonction permet de selectionner le lien du repertoire
        dans lequel se trouve le NDVI
        *********************************************************/
        
        """
        
        
        zonePath = QFileDialog.getOpenFileName(self, u"Enregistrer", 
                                               u"/home/puiseux/", 
                                               u"Images (*.shp )")
          
        if zonePath:
          
          self.zoneEmprise.setText(zonePath)

    def quit(self):
        """
        /** *******************************************************
        !@brief
        cette fonction permet de selectionner de fermer l'application
        ******************************************************** */
        
        """
        
        exit(0) 
        
        
    def selectionNDVI(self):
        """
        /** permet de charger le lien du repertoire du NDVI et verrouiller celui du DOY        */
        """
        while self.outilPretraitement.currentIndex()==0:
            self.cheminDOY.clear()
            self.cheminDOY.setEnabled(0)
            self.cheminNDVI.setEnabled(1)

        
    def selectionDOY(self):
        """
        /** permet de charger le lien du repertoire du DOY et verrouiller celui du NDVI        */
        """
        while self.outilPretraitement.currentIndex()==0:
            self.cheminNDVI.clear()
            self.cheminNDVI.setEnabled(0)
            self.cheminDOY.setEnabled(1)

    
    def validation(self):
        
        """
        /** 
        !@brief
        cette fonction permet de determiner l'action à réaliser quand on clique sur 
        Valider
        ******************************************************* */
        
        """
        #________si le decoupage est selectionné______________
#==============================================================================
        if self.outilPretraitement.currentIndex()==0:
             
              
              zoneEtudes=self.zoneEmprise.text() #zone d'etude
              
              debutYear=int(self.spinBox_debut.value()) #annee de debut
              
              lienSave=self.cheminOut.text()     #lien d'enregistrement
              
              if self.radioButton_NDVI.isChecked():
                  nomDonnee='NDVI' # type de données
                  lienDonnee=self.cheminNDVI.text()  # repertoire des données
                  
              if self.radioButton_DOY.isChecked():
                  nomDonnee='DOY' # type de données
                  lienDonnee=self.cheminDOY.text()   # repertoire des données
              if self.radioButton_imageParAn.isChecked():
                  pluriAnnuelle=0
              
              if self.radioButton_pluriAnnuelle.isChecked():
                  pluriAnnuelle=1
                      
              decoupage_et_serie_temporelle(str(lienDonnee),str(zoneEtudes),str(lienSave),debutYear,nomDonnee,pluriAnnuelle)    

        if self.outilPretraitement.currentIndex()==1:
            
            lienNdvi=self.cheminNDVI.text()
            lienDoy=self.cheminDOY.text()
            lienSave=self.cheminOut.text() 
            debutYear=int(self.spinBox_debut.value())
            finYear=int(self.spinBox_fin.value())
            save=1
            
            lissage=self.filtreInterpol.currentIndex()           
                
            if self.radioButton_imageParAn_interpol.isChecked():
                pluriAnnuelle=0
              
            if self.radioButton_pluriAnnuelle_interpol.isChecked():
                pluriAnnuelle=1
            
            interpo_lineaire_DOY16jours(lienNdvi,lienDoy,lienSave,debutYear,finYear,save,pluriAnnuelle,lissage)
            
    def validationMetrique(self):
        """
        /** 
        !@brief
        cette fonction permet de determiner l'action à réaliser quand on clique sur 
        Valider
        ******************************************************* */
        
        """
            
        chemin=str(self.cheminNDVI_metriqueFichier.text() )     
        p=0        
        if  p==1: #verifie que lien du NDVI existe
            
            print "lien du NDVI n'existe pas"
            
        else:
            
            [NDVI,GeoTransform,Projection]=open_data(chemin)
            
            duree=int(self.spinBox_fin__metrique.value())-int(self.spinBox_debut__metrique.value())+1
            
            
            [L,C,r]=NDVI.shape
            
            seuil1=self.seuilSOS.value()
            seuil2=self.seuilEOS.value()
            #variable qui stocke les 10 metriques pour chaque années 
            metrique=sp.empty((L,C,10),dtype='float16') 
            #tableaux dans les quelles les differentes metriques seront stockées séparemment
            sos=sp.empty((L,C,duree),dtype='float16')
            eos=sp.empty((L,C,duree),dtype='float16')
            los=sp.empty((L,C,duree),dtype='float16')
            
            area=sp.empty((L,C,duree),dtype='float16')
            areaBef=sp.empty((L,C,duree),dtype='float16')
            areaAft=sp.empty((L,C,duree),dtype='float16')
            
            anomalieSos=sp.empty((L,C,duree),dtype='float16')
            anomalieEos=sp.empty((L,C,duree),dtype='float16')
            anomalieLos=sp.empty((L,C,duree),dtype='float16')
            
            anomalieArea=sp.empty((L,C,duree),dtype='float16')
            anomalieAreaBef=sp.empty((L,C,duree),dtype='float16')
            anomalieAreaAft=sp.empty((L,C,duree),dtype='float16')


            self.progressBar_metrique.setValue(0)
            for k in range (duree):
                
                 deb=k*23
                 fin=deb+23
                 annee=int(self.spinBox_debut__metrique.value())+k
                 print annee
                 progress=k/(duree-1)*100
                 
                 for x in range(L):
                     for y in range(C):
                         
                         ndvi=NDVI[x,y,deb:fin]*0.0001

                         if self.methode.currentIndex()==0:
                             out1= metrique_pheno_greenbrown(ndvi,"white",seuil1,seuil2)
                             
                         if self.methode.currentIndex()==1:
                             out1= metrique_pheno_greenbrown(ndvi,"trs",seuil1,seuil2)
                         
                         if self.methode.currentIndex()==2:
                             out1= metrique_pheno_vito(ndvi,seuil1,seuil2)
                             
                             
                         outListe=metrique_pheno_param(ndvi,out1[0],out1[1],out1[4])
                         parametre=out1[0:3]+outListe
                         progress=progress+0.00001
                         self.progressBar_metrique.setValue(progress)
                         metrique[x,y,:]=sp.array(parametre)
                 sos[:,:,k]=metrique[:,:,1]
                 eos[:,:,k]=metrique[:,:,2]
                 los[:,:,k]=metrique[:,:,3]
                 area[:,:,k]=metrique[:,:,4]
                 areaBef[:,:,k]=metrique[:,:,5]
                 areaAft[:,:,k]=metrique[:,:,6]
                 
                 if self.prefixe.text()=='':
                     prefixe="parametre"
                     self.prefixe.setText(prefixe)
                 else:
                     prefixe=self.prefixe.text()
                
                 #Enregistrement des metriques année/année
                 output_name=self.cheminOut_metrique.text()+"\\"+prefixe+str(annee)+'.tif'
                 write_data(output_name,metrique,GeoTransform,Projection)
            name=str(self.spinBox_debut__metrique.value())+'-'+str(self.spinBox_fin__metrique.value())+".tif"
            
#==============================================================================
            moySos=sos.mean(2)
            moyEos=eos.mean(2)
            moyLos=los.mean(2)
            moyArea=area.mean(2)
            moyAreaBef=areaBef.mean(2)
            moyAreaAft=areaAft.mean(2)
             
            stdSos=sos.std(2)
            stdEos=eos.std(2)
            stdLos=los.std(2)
            stdArea=area.std(2)
            stdAreaBef=areaBef.std(2)
            stdAreaAft=areaAft.std(2)
            print stdSos
#==============================================================================
            
            for k in range(duree):
                anomalieSos[:,:,k]=(sos[:,:,k]-moySos)/stdSos
                anomalieEos[:,:,k]=(eos[:,:,k]-moyEos)/stdEos
                anomalieLos[:,:,k]=(los[:,:,k]-moyLos)/stdLos
                
                anomalieArea[:,:,k]=(area[:,:,k]-moyArea)/stdArea
                anomalieAreaBef[:,:,k]=(areaBef[:,:,k]-moyAreaBef)/stdAreaBef
                anomalieAreaAft[:,:,k]=(areaAft[:,:,k]-moyAreaAft)/stdAreaAft


            #enregistrement de sos
            write_data(self.cheminOut_metrique.text()+"\\"+"SOS_"+name,sos,GeoTransform,Projection)
            #enregistrement eos
            write_data(self.cheminOut_metrique.text()+"\\"+"EOS_"+name, eos,GeoTransform,Projection)
            #enregistrement los
            write_data(self.cheminOut_metrique.text()+"\\"+"LOS_"+name,los,GeoTransform,Projection)
            #enregistrement area
            write_data(self.cheminOut_metrique.text()+"\\"+"area_"+name,area,GeoTransform,Projection)
            #enregistrement areaAft
            write_data(self.cheminOut_metrique.text()+"\\"+"areaAfter_max_"+name,areaAft,GeoTransform,Projection)
            #enregistrement areaBef
            write_data(self.cheminOut_metrique.text()+"\\"+"areaBefore_max_"+name,areaBef,GeoTransform,Projection)

            #enregistrement de anomalie sos
            write_data(self.cheminOut_metrique.text()+"\\"+"anomalie_SOS_"+name,anomalieSos,GeoTransform,Projection)
            #enregistrement anomalie eos
            write_data(self.cheminOut_metrique.text()+"\\"+"anomalie_EOS_"+name, anomalieEos,GeoTransform,Projection)
            #enregistrement anomalielos
            write_data(self.cheminOut_metrique.text()+"\\"+"anomalie_LOS_"+name,anomalieLos,GeoTransform,Projection)
            #enregistrement anomalie area
            write_data(self.cheminOut_metrique.text()+"\\"+"anomalie_area_"+name,anomalieArea,GeoTransform,Projection)
            #enregistrement anomalie areaAft
            write_data(self.cheminOut_metrique.text()+"\\"+"anomalie_areaAfter_max_"+name,anomalieAreaBef,GeoTransform,Projection)
            #enregistrement anomalie AreaAFT
            write_data(self.cheminOut_metrique.text()+"\\"+"anomalie_areaBefore_max_"+name,anomalieAreaAft,GeoTransform,Projection)


            self.progressBar_metrique.setValue(0)

                    
            
            

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
 
