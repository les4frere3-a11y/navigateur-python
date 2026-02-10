import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLineEdit, QProgressBar, QLabel,
                             QFileDialog, QMessageBox, QTabWidget, QListWidget, 
                             QDialog, QListWidgetItem, QInputDialog, QMenu, QAction)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QUrl, Qt, QSize


class Navigateur(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LulyOS Navigator")
        self.setGeometry(100, 100, 1400, 900)
        
        # Liste des téléchargements
        self.telechargements = []
        
        # Historique et favoris
        self.historique = []
        self.favoris = []
        self.charger_donnees()
        
        # Appliquer le thème sombre
        self.appliquer_theme_sombre()
        
        # Widget principal
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)
        
        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(0)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        widget_principal.setLayout(layout_principal)
        
        # Barre de navigation supérieure
        barre_superieure = QWidget()
        barre_superieure.setObjectName("barreSuperieure")
        layout_barre = QVBoxLayout()
        layout_barre.setSpacing(10)
        layout_barre.setContentsMargins(15, 10, 15, 10)
        barre_superieure.setLayout(layout_barre)
        
        # Titre et contrôles
        layout_titre = QHBoxLayout()
        titre_app = QLabel("🌐 LulyOS Navigator")
        titre_app.setObjectName("titreApp")
        titre_app.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout_titre.addWidget(titre_app)
        layout_titre.addStretch()
        
        # Bouton thème
        self.btn_theme = QPushButton("☀️ Mode Clair")
        self.btn_theme.setObjectName("btnTheme")
        self.btn_theme.clicked.connect(self.basculer_theme)
        self.btn_theme.setFixedSize(120, 35)
        layout_titre.addWidget(self.btn_theme)
        
        layout_barre.addLayout(layout_titre)
        
        # Barre de navigation
        self.barre_nav = QHBoxLayout()
        self.barre_nav.setSpacing(8)
        
        # Bouton Retour
        self.btn_retour = QPushButton("◄")
        self.btn_retour.setObjectName("btnNav")
        self.btn_retour.setToolTip("Retour (Alt+←)")
        self.btn_retour.clicked.connect(self.retour)
        self.btn_retour.setFixedSize(45, 40)
        self.barre_nav.addWidget(self.btn_retour)
        
        # Bouton Avancer
        self.btn_avancer = QPushButton("►")
        self.btn_avancer.setObjectName("btnNav")
        self.btn_avancer.setToolTip("Avancer (Alt+→)")
        self.btn_avancer.clicked.connect(self.avancer)
        self.btn_avancer.setFixedSize(45, 40)
        self.barre_nav.addWidget(self.btn_avancer)
        
        # Bouton Actualiser
        self.btn_actualiser = QPushButton("⟳")
        self.btn_actualiser.setObjectName("btnNav")
        self.btn_actualiser.setToolTip("Actualiser (F5)")
        self.btn_actualiser.clicked.connect(self.actualiser)
        self.btn_actualiser.setFixedSize(45, 40)
        self.barre_nav.addWidget(self.btn_actualiser)
        
        # Bouton Accueil
        self.btn_accueil = QPushButton("🏠")
        self.btn_accueil.setObjectName("btnNav")
        self.btn_accueil.setToolTip("Page d'accueil")
        self.btn_accueil.clicked.connect(self.aller_accueil)
        self.btn_accueil.setFixedSize(45, 40)
        self.barre_nav.addWidget(self.btn_accueil)
        
        # Barre d'adresse
        self.barre_adresse = QLineEdit()
        self.barre_adresse.setObjectName("barreAdresse")
        self.barre_adresse.setPlaceholderText("🔍 Rechercher ou entrer une URL...")
        self.barre_adresse.setText("https://www.google.com")
        self.barre_adresse.returnPressed.connect(self.charger_url)
        self.barre_adresse.setFixedHeight(40)
        self.barre_nav.addWidget(self.barre_adresse)
        
        # Bouton Favoris
        self.btn_favoris = QPushButton("⭐")
        self.btn_favoris.setObjectName("btnNav")
        self.btn_favoris.setToolTip("Ajouter aux favoris")
        self.btn_favoris.clicked.connect(self.ajouter_favori)
        self.btn_favoris.setFixedSize(45, 40)
        self.barre_nav.addWidget(self.btn_favoris)
        
        # Bouton Afficher Favoris
        self.btn_voir_favoris = QPushButton("📚")
        self.btn_voir_favoris.setObjectName("btnNav")
        self.btn_voir_favoris.setToolTip("Voir les favoris")
        self.btn_voir_favoris.clicked.connect(self.afficher_favoris)
        self.btn_voir_favoris.setFixedSize(45, 40)
        self.barre_nav.addWidget(self.btn_voir_favoris)
        
        # Bouton Historique
        self.btn_historique = QPushButton("🕒")
        self.btn_historique.setObjectName("btnNav")
        self.btn_historique.setToolTip("Voir l'historique")
        self.btn_historique.clicked.connect(self.afficher_historique)
        self.btn_historique.setFixedSize(45, 40)
        self.barre_nav.addWidget(self.btn_historique)
        
        # Bouton Téléchargements
        self.btn_telechargements = QPushButton("📥")
        self.btn_telechargements.setObjectName("btnNav")
        self.btn_telechargements.setToolTip("Voir les téléchargements")
        self.btn_telechargements.clicked.connect(self.afficher_telechargements)
        self.btn_telechargements.setFixedSize(45, 40)
        self.barre_nav.addWidget(self.btn_telechargements)
        
        # Bouton Nouvel onglet
        self.btn_nouvel_onglet = QPushButton("➕")
        self.btn_nouvel_onglet.setObjectName("btnNouveau")
        self.btn_nouvel_onglet.setToolTip("Nouvel onglet (Ctrl+T)")
        self.btn_nouvel_onglet.clicked.connect(self.nouvel_onglet)
        self.btn_nouvel_onglet.setFixedSize(45, 40)
        self.barre_nav.addWidget(self.btn_nouvel_onglet)
        
        layout_barre.addLayout(self.barre_nav)
        layout_principal.addWidget(barre_superieure)
        
        # Zone de contenu avec onglets
        self.onglets = QTabWidget()
        self.onglets.setObjectName("onglets")
        self.onglets.setTabsClosable(True)
        self.onglets.tabCloseRequested.connect(self.fermer_onglet)
        
        # Premier onglet - navigateur web
        self.web = QWebEngineView()
        self.web.urlChanged.connect(self.mettre_a_jour_url)
        self.web.loadProgress.connect(self.mettre_a_jour_progression)
        
        # Configurer les téléchargements
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.gerer_telechargement)
        
        self.onglets.addTab(self.web, "🌐 Nouvel onglet")
        
        layout_principal.addWidget(self.onglets)
        
        # Barre de progression
        self.barre_progression = QProgressBar()
        self.barre_progression.setObjectName("barreProgression")
        self.barre_progression.setMaximumHeight(3)
        self.barre_progression.setTextVisible(False)
        self.barre_progression.hide()
        layout_principal.addWidget(self.barre_progression)
        
        # Barre de statut
        self.barre_statut = QLabel("Prêt")
        self.barre_statut.setObjectName("barreStatut")
        self.barre_statut.setFixedHeight(25)
        self.barre_statut.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout_principal.addWidget(self.barre_statut)
        
        # Charger Google par défaut
        self.charger_url()
        
        # Mode sombre par défaut
        self.mode_sombre = True
    
    def appliquer_theme_sombre(self):
        """Applique un thème sombre élégant"""
        style = """
        QMainWindow {
            background-color: #1e1e1e;
        }
        
        QWidget#barreSuperieure {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 #2d2d30, stop:1 #252526);
            border-bottom: 1px solid #3e3e42;
        }
        
        QLabel#titreApp {
            color: #ffffff;
            font-size: 16px;
            font-weight: bold;
        }
        
        QPushButton#btnNav {
            background-color: #3e3e42;
            border: 1px solid #555555;
            border-radius: 20px;
            color: #ffffff;
            font-size: 18px;
            font-weight: bold;
        }
        
        QPushButton#btnNav:hover {
            background-color: #505050;
            border: 1px solid #666666;
        }
        
        QPushButton#btnNav:pressed {
            background-color: #2d2d30;
        }
        
        QPushButton#btnTheme {
            background-color: #0e639c;
            border: none;
            border-radius: 20px;
            color: #ffffff;
            font-weight: bold;
        }
        
        QPushButton#btnTheme:hover {
            background-color: #1177bb;
        }
        
        QPushButton#btnTelecharge {
            background-color: #2d7d2d;
            border: none;
            border-radius: 20px;
            color: #ffffff;
            font-weight: bold;
        }
        
        QPushButton#btnTelecharge:hover {
            background-color: #359535;
        }
        
        QPushButton#btnNouveau {
            background-color: #9c640e;
            border: 1px solid #b87a1a;
            border-radius: 20px;
            color: #ffffff;
            font-size: 20px;
            font-weight: bold;
        }
        
        QPushButton#btnNouveau:hover {
            background-color: #b87a1a;
        }
        
        QLineEdit#barreAdresse {
            background-color: #3e3e42;
            border: 2px solid #555555;
            border-radius: 20px;
            color: #ffffff;
            padding: 8px 15px;
            font-size: 13px;
        }
        
        QLineEdit#barreAdresse:focus {
            border: 2px solid #0e639c;
            background-color: #2d2d30;
        }
        
        QProgressBar#barreProgression {
            background-color: #252526;
            border: none;
        }
        
        QProgressBar#barreProgression::chunk {
            background-color: #0e639c;
        }
        
        QLabel#barreStatut {
            background-color: #007acc;
            color: #ffffff;
            padding-left: 10px;
            font-size: 11px;
        }
        
        QTabWidget#onglets::pane {
            border: none;
            background-color: #1e1e1e;
        }
        
        QTabWidget#onglets QTabBar::tab {
            background-color: #2d2d30;
            color: #cccccc;
            border: none;
            padding: 10px 20px;
            margin-right: 2px;
        }
        
        QTabWidget#onglets QTabBar::tab:selected {
            background-color: #1e1e1e;
            color: #ffffff;
            border-bottom: 2px solid #007acc;
        }
        
        QTabWidget#onglets QTabBar::tab:hover {
            background-color: #3e3e42;
        }
        
        QListWidget {
            background-color: #252526;
            color: #cccccc;
            border: 1px solid #3e3e42;
            border-radius: 4px;
            padding: 5px;
        }
        
        QListWidget::item {
            padding: 8px;
            border-bottom: 1px solid #3e3e42;
        }
        
        QListWidget::item:hover {
            background-color: #2d2d30;
        }
        
        QMessageBox {
            background-color: #2d2d30;
            color: #ffffff;
        }
        
        QMessageBox QPushButton {
            background-color: #0e639c;
            color: #ffffff;
            border: none;
            border-radius: 4px;
            padding: 6px 20px;
            min-width: 80px;
        }
        
        QMessageBox QPushButton:hover {
            background-color: #1177bb;
        }
        """
        self.setStyleSheet(style)
    
    def appliquer_theme_clair(self):
        """Applique un thème clair moderne"""
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QWidget#barreSuperieure {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 #ffffff, stop:1 #f0f0f0);
            border-bottom: 1px solid #d0d0d0;
        }
        
        QLabel#titreApp {
            color: #2c3e50;
            font-size: 16px;
            font-weight: bold;
        }
        
        QPushButton#btnNav {
            background-color: #e8e8e8;
            border: 1px solid #c0c0c0;
            border-radius: 20px;
            color: #2c3e50;
            font-size: 18px;
            font-weight: bold;
        }
        
        QPushButton#btnNav:hover {
            background-color: #d0d0d0;
            border: 1px solid #a0a0a0;
        }
        
        QPushButton#btnNav:pressed {
            background-color: #c0c0c0;
        }
        
        QPushButton#btnTheme {
            background-color: #3498db;
            border: none;
            border-radius: 20px;
            color: #ffffff;
            font-weight: bold;
        }
        
        QPushButton#btnTheme:hover {
            background-color: #2980b9;
        }
        
        QPushButton#btnTelecharge {
            background-color: #27ae60;
            border: none;
            border-radius: 20px;
            color: #ffffff;
            font-weight: bold;
        }
        
        QPushButton#btnTelecharge:hover {
            background-color: #229954;
        }
        
        QPushButton#btnNouveau {
            background-color: #e67e22;
            border: 1px solid #d35400;
            border-radius: 20px;
            color: #ffffff;
            font-size: 20px;
            font-weight: bold;
        }
        
        QPushButton#btnNouveau:hover {
            background-color: #d35400;
        }
        
        QLineEdit#barreAdresse {
            background-color: #ffffff;
            border: 2px solid #d0d0d0;
            border-radius: 20px;
            color: #2c3e50;
            padding: 8px 15px;
            font-size: 13px;
        }
        
        QLineEdit#barreAdresse:focus {
            border: 2px solid #3498db;
        }
        
        QProgressBar#barreProgression {
            background-color: #e0e0e0;
            border: none;
        }
        
        QProgressBar#barreProgression::chunk {
            background-color: #3498db;
        }
        
        QLabel#barreStatut {
            background-color: #3498db;
            color: #ffffff;
            padding-left: 10px;
            font-size: 11px;
        }
        
        QTabWidget#onglets::pane {
            border: none;
            background-color: #f5f5f5;
        }
        
        QTabWidget#onglets QTabBar::tab {
            background-color: #e8e8e8;
            color: #2c3e50;
            border: none;
            padding: 10px 20px;
            margin-right: 2px;
        }
        
        QTabWidget#onglets QTabBar::tab:selected {
            background-color: #ffffff;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
        }
        
        QTabWidget#onglets QTabBar::tab:hover {
            background-color: #d0d0d0;
        }
        
        QListWidget {
            background-color: #ffffff;
            color: #2c3e50;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            padding: 5px;
        }
        
        QListWidget::item {
            padding: 8px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        QListWidget::item:hover {
            background-color: #f0f0f0;
        }
        """
        self.setStyleSheet(style)
    
    def basculer_theme(self):
        """Bascule entre thème sombre et clair"""
        if self.mode_sombre:
            self.appliquer_theme_clair()
            self.btn_theme.setText("🌙 Mode Sombre")
            self.mode_sombre = False
        else:
            self.appliquer_theme_sombre()
            self.btn_theme.setText("☀️ Mode Clair")
            self.mode_sombre = True
    
    def charger_url(self):
        """Charge l'URL entrée dans la barre d'adresse"""
        url = self.barre_adresse.text().strip()
        
        # Si c'est une recherche et non une URL
        if " " in url or ("." not in url and not url.startswith("http")):
            url = f"https://www.google.com/search?q={url}"
        elif not url.startswith("http"):
            url = "https://" + url
        
        self.web.load(QUrl(url))
        self.barre_statut.setText(f"Chargement de {url}...")
    
    def mettre_a_jour_url(self, url):
        """Met à jour la barre d'adresse avec l'URL actuelle"""
        self.barre_adresse.setText(url.toString())
        index = self.onglets.currentIndex()
        if index >= 0:
            # Extraire le titre de la page
            titre = url.host() if url.host() else "Nouvel onglet"
            self.onglets.setTabText(index, f"🌐 {titre[:20]}")
        
        # Ajouter à l'historique
        self.ajouter_historique(url.toString(), self.web.title() or url.host())
    
    def mettre_a_jour_progression(self, progression):
        """Met à jour la barre de progression"""
        if progression < 100:
            self.barre_progression.show()
            self.barre_progression.setValue(progression)
            self.barre_statut.setText(f"Chargement... {progression}%")
        else:
            self.barre_progression.hide()
            self.barre_statut.setText("✓ Page chargée")
    
    def retour(self):
        """Retourne à la page précédente"""
        self.web.back()
    
    def avancer(self):
        """Avance à la page suivante"""
        self.web.forward()
    
    def actualiser(self):
        """Actualise la page actuelle"""
        self.web.reload()
        self.barre_statut.setText("Actualisation de la page...")
    
    def aller_accueil(self):
        """Retourne à la page d'accueil"""
        self.barre_adresse.setText("https://www.google.com")
        self.charger_url()
    
    def fermer_onglet(self, index):
        """Ferme un onglet"""
        if self.onglets.count() > 1:
            self.onglets.removeTab(index)
    
    def gerer_telechargement(self, telechargement):
        """Gère les téléchargements"""
        # Demander où sauvegarder le fichier
        chemin = QFileDialog.getSaveFileName(
            self, 
            "Enregistrer le fichier", 
            os.path.expanduser(f"~/Downloads/{telechargement.suggestedFileName()}")
        )
        
        if chemin[0]:
            telechargement.setPath(chemin[0])
            telechargement.accept()
            
            # Ajouter à la liste des téléchargements
            info_telechargement = {
                'nom': telechargement.suggestedFileName(),
                'chemin': chemin[0],
                'item': telechargement
            }
            self.telechargements.append(info_telechargement)
            
            # Connecter les signaux
            telechargement.downloadProgress.connect(
                lambda recu, total: self.progression_telechargement(recu, total, info_telechargement)
            )
            telechargement.finished.connect(
                lambda: self.telechargement_termine(info_telechargement)
            )
            
            self.barre_statut.setText(f"📥 Téléchargement démarré: {telechargement.suggestedFileName()}")
    
    def progression_telechargement(self, recu, total, info):
        """Met à jour la progression du téléchargement"""
        if total > 0:
            pourcentage = int((recu / total) * 100)
            taille_mo = recu / (1024 * 1024)
            total_mo = total / (1024 * 1024)
            self.barre_statut.setText(
                f"📥 Téléchargement: {info['nom']} - {pourcentage}% ({taille_mo:.1f}/{total_mo:.1f} Mo)"
            )
    
    def telechargement_termine(self, info):
        """Appelé quand un téléchargement est terminé"""
        self.barre_statut.setText(f"✓ Téléchargement terminé: {info['nom']}")
        
        # Message de confirmation
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Téléchargement terminé")
        msg.setText(f"Le fichier '{info['nom']}' a été téléchargé avec succès !")
        msg.setInformativeText(f"Emplacement: {info['chemin']}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def afficher_telechargements(self):
        """Affiche la liste des téléchargements"""
        if not self.telechargements:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Téléchargements")
            msg.setText("Aucun téléchargement en cours ou terminé.")
            msg.exec_()
        else:
            # Créer une fenêtre pour afficher les téléchargements
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Téléchargements")
            dialog.setIcon(QMessageBox.Information)
            
            texte = "Téléchargements :\n\n"
            for i, t in enumerate(self.telechargements, 1):
                texte += f"{i}. {t['nom']}\n   📁 {t['chemin']}\n\n"
            
            dialog.setText(texte)
            dialog.exec_()
    
    def charger_donnees(self):
        """Charge l'historique et les favoris depuis le fichier"""
        try:
            chemin_fichier = os.path.expanduser("~/lulyos_navigator_data.json")
            if os.path.exists(chemin_fichier):
                with open(chemin_fichier, 'r', encoding='utf-8') as f:
                    donnees = json.load(f)
                    self.historique = donnees.get('historique', [])
                    self.favoris = donnees.get('favoris', [])
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
    
    def sauvegarder_donnees(self):
        """Sauvegarde l'historique et les favoris dans un fichier"""
        try:
            chemin_fichier = os.path.expanduser("~/lulyos_navigator_data.json")
            donnees = {
                'historique': self.historique[-500:],  # Garder les 500 dernières entrées
                'favoris': self.favoris
            }
            with open(chemin_fichier, 'w', encoding='utf-8') as f:
                json.dump(donnees, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des données: {e}")
    
    def ajouter_historique(self, url, titre):
        """Ajoute une URL à l'historique"""
        if url and url.startswith('http'):
            entree = {
                'url': url,
                'titre': titre or url,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            # Éviter les doublons consécutifs
            if not self.historique or self.historique[-1]['url'] != url:
                self.historique.append(entree)
                self.sauvegarder_donnees()
    
    def afficher_historique(self):
        """Affiche l'historique de navigation"""
        dialog = QDialog(self)
        dialog.setWindowTitle("📜 Historique de navigation")
        dialog.setGeometry(200, 200, 700, 500)
        
        layout = QVBoxLayout()
        
        # En-tête
        titre = QLabel("Historique de navigation")
        titre.setFont(QFont("Segoe UI", 14, QFont.Bold))
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)
        
        # Liste de l'historique
        liste = QListWidget()
        liste.setObjectName("listeHistorique")
        
        # Remplir la liste (plus récent en premier)
        for entree in reversed(self.historique[-100:]):  # 100 dernières entrées
            item_text = f"🌐 {entree['titre']}\n   {entree['url']}\n   🕒 {entree['date']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, entree['url'])
            liste.addItem(item)
        
        liste.itemDoubleClicked.connect(lambda item: self.ouvrir_depuis_historique(item, dialog))
        layout.addWidget(liste)
        
        # Boutons
        boutons_layout = QHBoxLayout()
        
        btn_ouvrir = QPushButton("🌐 Ouvrir")
        btn_ouvrir.clicked.connect(lambda: self.ouvrir_depuis_historique(liste.currentItem(), dialog))
        boutons_layout.addWidget(btn_ouvrir)
        
        btn_effacer = QPushButton("🗑️ Effacer l'historique")
        btn_effacer.clicked.connect(lambda: self.effacer_historique(dialog))
        boutons_layout.addWidget(btn_effacer)
        
        btn_fermer = QPushButton("❌ Fermer")
        btn_fermer.clicked.connect(dialog.close)
        boutons_layout.addWidget(btn_fermer)
        
        layout.addLayout(boutons_layout)
        dialog.setLayout(layout)
        dialog.exec_()
    
    def ouvrir_depuis_historique(self, item, dialog):
        """Ouvre une URL depuis l'historique"""
        if item:
            url = item.data(Qt.UserRole)
            self.barre_adresse.setText(url)
            self.charger_url()
            dialog.close()
    
    def effacer_historique(self, dialog):
        """Efface tout l'historique"""
        reponse = QMessageBox.question(
            self,
            "Confirmer",
            "Voulez-vous vraiment effacer tout l'historique ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reponse == QMessageBox.Yes:
            self.historique = []
            self.sauvegarder_donnees()
            dialog.close()
            QMessageBox.information(self, "Historique", "L'historique a été effacé.")
    
    def ajouter_favori(self):
        """Ajoute la page actuelle aux favoris"""
        url = self.barre_adresse.text()
        titre = self.web.title() or self.web.url().host()
        
        if not url or not url.startswith('http'):
            QMessageBox.warning(self, "Favoris", "Aucune page à ajouter aux favoris.")
            return
        
        # Vérifier si déjà dans les favoris
        for fav in self.favoris:
            if fav['url'] == url:
                QMessageBox.information(self, "Favoris", "Cette page est déjà dans vos favoris.")
                return
        
        # Demander un nom personnalisé
        nom, ok = QInputDialog.getText(
            self,
            "Ajouter aux favoris",
            "Nom du favori:",
            QLineEdit.Normal,
            titre
        )
        
        if ok and nom:
            favori = {
                'url': url,
                'titre': nom,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.favoris.append(favori)
            self.sauvegarder_donnees()
            QMessageBox.information(self, "Favoris", f"'{nom}' a été ajouté aux favoris !")
    
    def afficher_favoris(self):
        """Affiche la liste des favoris"""
        dialog = QDialog(self)
        dialog.setWindowTitle("⭐ Mes Favoris")
        dialog.setGeometry(200, 200, 700, 500)
        
        layout = QVBoxLayout()
        
        # En-tête
        titre = QLabel("⭐ Mes Favoris")
        titre.setFont(QFont("Segoe UI", 14, QFont.Bold))
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)
        
        # Liste des favoris
        liste = QListWidget()
        liste.setObjectName("listeFavoris")
        
        for fav in self.favoris:
            item_text = f"⭐ {fav['titre']}\n   {fav['url']}\n   📅 Ajouté le {fav['date']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, fav['url'])
            liste.addItem(item)
        
        liste.itemDoubleClicked.connect(lambda item: self.ouvrir_depuis_favoris(item, dialog))
        layout.addWidget(liste)
        
        # Boutons
        boutons_layout = QHBoxLayout()
        
        btn_ouvrir = QPushButton("🌐 Ouvrir")
        btn_ouvrir.clicked.connect(lambda: self.ouvrir_depuis_favoris(liste.currentItem(), dialog))
        boutons_layout.addWidget(btn_ouvrir)
        
        btn_supprimer = QPushButton("🗑️ Supprimer")
        btn_supprimer.clicked.connect(lambda: self.supprimer_favori(liste))
        boutons_layout.addWidget(btn_supprimer)
        
        btn_fermer = QPushButton("❌ Fermer")
        btn_fermer.clicked.connect(dialog.close)
        boutons_layout.addWidget(btn_fermer)
        
        layout.addLayout(boutons_layout)
        dialog.setLayout(layout)
        dialog.exec_()
    
    def ouvrir_depuis_favoris(self, item, dialog):
        """Ouvre une URL depuis les favoris"""
        if item:
            url = item.data(Qt.UserRole)
            self.barre_adresse.setText(url)
            self.charger_url()
            dialog.close()
    
    def supprimer_favori(self, liste):
        """Supprime un favori sélectionné"""
        item = liste.currentItem()
        if item:
            url = item.data(Qt.UserRole)
            self.favoris = [f for f in self.favoris if f['url'] != url]
            self.sauvegarder_donnees()
            liste.takeItem(liste.currentRow())
            QMessageBox.information(self, "Favoris", "Le favori a été supprimé.")
    
    def nouvel_onglet(self):
        """Crée un nouvel onglet"""
        nouveau_web = QWebEngineView()
        nouveau_web.urlChanged.connect(self.mettre_a_jour_url)
        nouveau_web.loadProgress.connect(self.mettre_a_jour_progression)
        
        # Configurer le profil pour les téléchargements
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.gerer_telechargement)
        
        index = self.onglets.addTab(nouveau_web, "🌐 Nouvel onglet")
        self.onglets.setCurrentIndex(index)
        
        # Charger la page d'accueil
        nouveau_web.load(QUrl("https://www.google.com"))
        
        # Mettre à jour la référence web courante
        self.web = nouveau_web
    
    def closeEvent(self, event):
        """Sauvegarde les données avant de fermer"""
        self.sauvegarder_donnees()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("LulyOS Navigator")
    
    # Police par défaut
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    navigateur = Navigateur()
    navigateur.show()
    sys.exit(app.exec_())
