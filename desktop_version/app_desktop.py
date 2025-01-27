import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, 
                            QVBoxLayout, QWidget, QLabel, QComboBox, QDoubleSpinBox, 
                            QCheckBox, QListWidget, QProgressBar, QMessageBox)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QSize
from PySide6.QtGui import QFont, QIcon, QFontDatabase
import pandas as pd
import os

class PriceUpdaterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculateur de Prix v2.0")
        self.setMinimumSize(1000, 700)
        
        # Chargement des polices
        QFontDatabase.addApplicationFont("desktop_version/fonts/Poppins-Regular.ttf")
        QFontDatabase.addApplicationFont("desktop_version/fonts/Poppins-Bold.ttf")
        
        # Configuration des polices
        self.title_font = QFont("Poppins", 24, QFont.Bold)
        self.normal_font = QFont("Poppins", 16)
        
        # Configuration des icônes
        self.file_icon = QIcon("desktop_version/icons/file.png")
        self.calc_icon = QIcon("desktop_version/icons/calculator.png")
        self.settings_icon = QIcon("desktop_version/icons/settings.png")
        
        # Variables principales
        self.df = None
        self.selected_columns = []
        
        # Interface principale
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        main_widget.setLayout(layout)
        
        # Titre avec animation
        title = QLabel("Calculateur de Prix")
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")
        self.title_animation = QPropertyAnimation(title, b"pos")
        self.title_animation.setDuration(1000)
        self.title_animation.setStartValue(QPoint(0, -50))
        self.title_animation.setEndValue(QPoint(0, 0))
        self.title_animation.setEasingCurve(QEasingCurve.OutBack)
        self.title_animation.start()
        
        # Étape 1: Sélection du fichier
        step1_label = QLabel("Étape 1: Sélectionner le fichier")
        step1_label.setFont(self.normal_font)
        self.file_label = QLabel("Aucun fichier sélectionné")
        self.file_button = QPushButton("Sélectionner un fichier Excel")
        self.file_button.setIcon(self.file_icon)
        self.file_button.setIconSize(QSize(24, 24))
        self.file_button.setFont(self.normal_font)
        self.file_button.setMinimumHeight(50)
        self.file_button.clicked.connect(self.select_file)
        
        # Étape 2: Sélection des colonnes
        step2_label = QLabel("Étape 2: Sélectionner les colonnes")
        step2_label.setFont(self.normal_font)
        self.columns_group = QWidget()
        columns_layout = QVBoxLayout()
        self.keep_all_checkbox = QCheckBox("Garder toutes les colonnes")
        self.keep_all_checkbox.setChecked(True)
        self.keep_all_checkbox.stateChanged.connect(self.toggle_columns_list)
        self.columns_list = QListWidget()
        self.columns_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.columns_list.setMaximumHeight(200)  # Limite la hauteur
        self.columns_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        columns_layout.addWidget(self.keep_all_checkbox)
        columns_layout.addWidget(self.columns_list)
        self.columns_group.setLayout(columns_layout)
        self.columns_group.hide()
        
        # Étape 3: Configuration du calcul
        step3_label = QLabel("Étape 3: Configurer le calcul")
        step3_label.setFont(self.normal_font)
        self.price_group = QWidget()
        price_layout = QVBoxLayout()
        self.price_column_label = QLabel("Sélectionnez la colonne des prix:")
        self.price_column_combo = QComboBox()
        self.price_column_combo.setMinimumHeight(40)
        self.percentage_label = QLabel("Pourcentage d'augmentation:")
        self.percentage_spin = QDoubleSpinBox()
        self.percentage_spin.setRange(-100, 100)
        self.percentage_spin.setDecimals(2)
        self.percentage_spin.setSuffix("%")
        self.percentage_spin.setMinimumHeight(40)
        self.calculate_button = QPushButton("Calculer")
        self.calculate_button.setIcon(self.calc_icon)
        self.calculate_button.setIconSize(QSize(24, 24))
        self.calculate_button.setFont(self.normal_font)
        self.calculate_button.setMinimumHeight(50)
        self.calculate_button.clicked.connect(self.process_file)
        
        price_layout.addWidget(self.price_column_label)
        price_layout.addWidget(self.price_column_combo)
        price_layout.addWidget(self.percentage_label)
        price_layout.addWidget(self.percentage_spin)
        price_layout.addSpacing(20)
        price_layout.addWidget(self.calculate_button)
        self.price_group.setLayout(price_layout)
        self.price_group.hide()
        
        # Barre de progression
        self.progress = QProgressBar()
        self.progress.hide()
        
        # Ajout des widgets au layout principal
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(step1_label)
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_button)
        layout.addSpacing(20)
        layout.addWidget(step2_label)
        layout.addWidget(self.columns_group)
        layout.addSpacing(20)
        layout.addWidget(step3_label)
        layout.addWidget(self.price_group)
        layout.addWidget(self.progress)
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background: #1e293b;
            }
            
            QLabel {
                color: white;
                font-size: 16px;
                margin: 15px 0;
            }
            
            QComboBox {
                background-color: #2d3748;
                color: white;
                padding: 12px;
                border: 2px solid #4361ee;
                border-radius: 8px;
                min-height: 45px;
                font-size: 16px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #2d3748;
                color: white;
                selection-background-color: #4361ee;
                selection-color: white;
                border: 2px solid #4361ee;
            }
            
            QComboBox::drop-down {
                border: none;
            }
            
            QComboBox::down-arrow {
                image: url(desktop_version/icons/arrow-down.png);
                width: 12px;
                height: 12px;
            }
            
            QListWidget {
                background-color: #2d3748;
                color: white;
                border: 2px solid #4361ee;
                border-radius: 8px;
                padding: 10px;
            }
            
            QListWidget::item {
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
                background: rgba(255, 255, 255, 0.1);
            }
            
            QListWidget::item:selected {
                background: #4361ee;
            }
            
            QPushButton {
                background-color: #4361ee;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                min-height: 45px;
            }
            
            QPushButton:hover {
                background-color: #3730a3;
            }
            
            QCheckBox {
                color: white;
                font-size: 16px;
            }
        """)

        # Style pour les popups
        self.setStyleSheet(self.styleSheet() + """
            QMessageBox {
                background-color: #1e293b;
            }
            
            QMessageBox QLabel {
                color: white;
                font-size: 16px;
                padding: 20px;
                min-width: 300px;
            }
            
            QMessageBox QPushButton {
                background-color: #4361ee;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #3730a3;
            }
            
            QFileDialog {
                background-color: #1e293b;
                color: white;
            }
            
            QFileDialog QLabel {
                color: white;
            }
            
            QFileDialog QComboBox {
                background-color: #2d3748;
                color: white;
                border: 1px solid #4361ee;
            }
            
            QFileDialog QListView {
                background-color: #2d3748;
                color: white;
            }
            
            QFileDialog QPushButton {
                background-color: #4361ee;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
        """)

        # Style pour la scrollbar
        self.setStyleSheet(self.styleSheet() + """
            QScrollBar:vertical {
                border: none;
                background: #2d3748;
                width: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background: #4361ee;
                border-radius: 5px;
                min-height: 20px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QListWidget {
                max-height: 200px;
            }
        """)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier Excel", 
            os.path.expanduser("~"),
            "Fichiers Excel (*.xlsx);;Anciens fichiers Excel (*.xls);;Tous les fichiers (*.*)"
        )
        if file_name:
            try:
                self.df = pd.read_excel(file_name)
                self.file_label.setText(f"Fichier sélectionné: {os.path.basename(file_name)}")
                self.file_label.setStyleSheet("color: green;")
                self.update_columns()
                self.columns_group.show()
                self.price_group.show()
            except Exception as e:
                self.file_label.setText(f"Erreur: {str(e)}")
                self.file_label.setStyleSheet("color: red;")
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la lecture du fichier: {str(e)}")

    def update_columns(self):
        if self.df is not None:
            columns = self.df.columns.tolist()
            self.columns_list.clear()
            self.price_column_combo.clear()
            
            # Mise à jour de la liste des colonnes
            for column in columns:
                self.columns_list.addItem(column)
                # Vérifier si la colonne contient des nombres
                if pd.to_numeric(self.df[column], errors='coerce').notna().any():
                    self.price_column_combo.addItem(column)
            
            # Cocher la case "Garder toutes les colonnes" par défaut
            self.keep_all_checkbox.setChecked(True)
            
            # Sélectionner toutes les colonnes par défaut
            for i in range(self.columns_list.count()):
                self.columns_list.item(i).setSelected(True)

    def toggle_columns_list(self, state):
        if state == Qt.CheckState.Checked.value:
            self.columns_list.hide()
        else:
            self.columns_list.show()

    def process_file(self):
        if self.df is None:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord sélectionner un fichier.")
            return
        
        try:
            self.progress.show()
            self.progress.setValue(0)
            
            # Récupérer les colonnes sélectionnées
            if self.keep_all_checkbox.isChecked():
                selected_columns = self.df.columns.tolist()
            else:
                selected_columns = [item.text() for item in self.columns_list.selectedItems()]
            
            if not selected_columns:
                QMessageBox.warning(self, "Attention", "Veuillez sélectionner au moins une colonne.")
                return
            
            self.progress.setValue(30)
            
            # Récupérer la colonne de prix sélectionnée
            original_price_column = self.price_column_combo.currentText()
            percentage = self.percentage_spin.value()
            
            # Créer une copie du DataFrame avec les colonnes sélectionnées
            df_selected = self.df[selected_columns].copy()
            
            # Convertir la colonne de prix en numérique
            try:
                df_selected[original_price_column] = pd.to_numeric(df_selected[original_price_column], errors='coerce')
            except Exception as e:
                QMessageBox.critical(self, "Erreur", 
                    f"Erreur lors de la conversion des prix: {str(e)}")
                return
            
            self.progress.setValue(60)
            
            # Créer une copie de la colonne de prix pour les nouveaux prix
            df_selected["Prix de vente"] = df_selected[original_price_column].copy()
            
            # Appliquer l'augmentation sur la nouvelle colonne
            mask = df_selected["Prix de vente"].notna()
            df_selected.loc[mask, "Prix de vente"] *= (1 + percentage/100)
            
            # Appliquer les règles d'arrondi
            def round_price(x):
                if pd.isna(x):
                    return x
                if x % 1 < 0.4:
                    return float(round(x))
                elif x % 1 > 0.5 and x % 1 < 0.6:
                    return float(round(x))
                elif x % 1 == 0.5:
                    return float(round(x + 0.5))
                else:
                    return float(round(x + 1))
            
            df_selected["Prix de vente"] = df_selected["Prix de vente"].apply(round_price)
            
            # Renommer la colonne originale en dernier
            df_selected = df_selected.rename(columns={original_price_column: "Prix d'achat"})
            
            self.progress.setValue(80)
            
            # Sauvegarder le fichier
            save_name, _ = QFileDialog.getSaveFileName(
                self,
                "Sauvegarder le fichier",
                "prix_modifies.xlsx",
                "Excel Files (*.xlsx);;CSV Files (*.csv)"
            )
            
            if save_name:
                if save_name.endswith('.csv'):
                    df_selected.to_csv(save_name, index=False)
                else:
                    writer = pd.ExcelWriter(save_name, engine='xlsxwriter')
                    df_selected.to_excel(writer, index=False, sheet_name='Sheet1')
                    
                    workbook = writer.book
                    worksheet = writer.sheets['Sheet1']
                    
                    # Formats pour les colonnes de prix
                    price_format = workbook.add_format({
                        'num_format': '#,##0.00'
                    })
                    
                    green_format = workbook.add_format({
                        'font_color': '#006400',
                        'bold': True,
                        'num_format': '#,##0.00'
                    })
                    
                    # Appliquer les formats
                    achat_col_idx = df_selected.columns.get_loc("Prix d'achat")
                    vente_col_idx = df_selected.columns.get_loc("Prix de vente")
                    
                    worksheet.set_column(achat_col_idx, achat_col_idx, None, price_format)
                    worksheet.set_column(vente_col_idx, vente_col_idx, None, green_format)
                    
                    writer.close()
                    
                self.progress.setValue(100)
                QMessageBox.information(self, "Succès", "Traitement terminé avec succès!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", 
                f"Erreur lors du traitement: {str(e)}\n\nDétails: {type(e).__name__}")
        finally:
            self.progress.hide()

    def animate_button(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(200)
        animation.setStartValue(button.geometry())
        new_geometry = button.geometry()
        new_geometry.translate(0, -2)
        animation.setEndValue(new_geometry)
        animation.start()

def main():
    # Forcer l'utilisation de X11 au lieu de Wayland
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    
    app = QApplication(sys.argv)
    window = PriceUpdaterApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()