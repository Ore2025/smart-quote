"""Générateur d'images avec design moderne et professionnel"""
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ImageGenerator:
    """Générateur d'images de citations avec styles multiples et personnalisables"""
    
    # Constantes de configuration
    DEFAULT_SIZE = (1080, 1080)
    FONT_SIZES = {
        'quote': {'small': 48, 'medium': 42, 'large': 36, 'xlarge': 32},
        'author': 32,
        'decorative': 72
    }
    
    PADDING_BY_STYLE = {
        'minimal': 80,
        'moderne': 100,
        'elegant': 120
    }
    
    def __init__(self, size: Tuple[int, int] = DEFAULT_SIZE):
        """Initialise le générateur d'images
        
        Args:
            size: Dimensions de l'image (largeur, hauteur)
        """
        self.size = size
        self.fonts_cache = {}
        self.available_fonts = self._discover_system_fonts()
        logger.info(f"ImageGenerator initialisé - Taille: {size}, Polices: {len(self.available_fonts)}")
    
    def _discover_system_fonts(self) -> dict:
        """Découvre et indexe les polices système disponibles"""
        fonts = {}
        
        font_paths = [
            # DejaVu (Ubuntu/Debian)
            ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVu Sans', 'regular'),
            ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'DejaVu Sans', 'bold'),
            ('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 'DejaVu Serif', 'regular'),
            ('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 'DejaVu Serif', 'bold'),
            
            # Liberation (RedHat/Fedora)
            ('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 'Liberation Sans', 'regular'),
            ('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 'Liberation Sans', 'bold'),
            ('/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf', 'Liberation Serif', 'regular'),
            ('/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf', 'Liberation Serif', 'bold'),
            
            # Ubuntu
            ('/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf', 'Ubuntu', 'regular'),
            ('/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf', 'Ubuntu', 'bold'),
            
            # Noto
            ('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 'Noto Sans', 'regular'),
            ('/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf', 'Noto Sans', 'bold'),
        ]
        
        for path, family, weight in font_paths:
            if Path(path).exists():
                if family not in fonts:
                    fonts[family] = {}
                fonts[family][weight] = path
        
        return fonts if fonts else {'DejaVu Sans': {'regular': None, 'bold': None}}
    
    def _get_font(self, size: int, weight: str = 'regular', family: str = 'DejaVu Sans') -> ImageFont.FreeTypeFont:
        """Charge une police avec mise en cache
        
        Args:
            size: Taille de la police
            weight: 'regular' ou 'bold'
            family: Famille de police
            
        Returns:
            Police chargée
        """
        cache_key = f"{family}_{weight}_{size}"
        
        if cache_key in self.fonts_cache:
            return self.fonts_cache[cache_key]
        
        try:
            # Chercher la police demandée
            if family in self.available_fonts and weight in self.available_fonts[family]:
                font_path = self.available_fonts[family][weight]
                if font_path and Path(font_path).exists():
                    font = ImageFont.truetype(font_path, size)
                    self.fonts_cache[cache_key] = font
                    return font
            
            # Fallback vers weight regular si bold non disponible
            if weight == 'bold' and family in self.available_fonts:
                if 'regular' in self.available_fonts[family]:
                    font_path = self.available_fonts[family]['regular']
                    if font_path and Path(font_path).exists():
                        font = ImageFont.truetype(font_path, size)
                        self.fonts_cache[cache_key] = font
                        return font
            
            # Fallback vers DejaVu Sans
            fallback_paths = [
                f"/usr/share/fonts/truetype/dejavu/DejaVuSans-{weight.capitalize()}.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            ]
            
            for path in fallback_paths:
                if Path(path).exists():
                    font = ImageFont.truetype(path, size)
                    self.fonts_cache[cache_key] = font
                    logger.warning(f"Utilisation police fallback: {path}")
                    return font
            
            # Dernier recours
            font = ImageFont.load_default()
            logger.error("Aucune police TrueType disponible, utilisation police par défaut")
            return font
            
        except Exception as e:
            logger.error(f"Erreur chargement police: {e}")
            return ImageFont.load_default()
    
    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Découpe intelligente du texte en lignes
        
        Args:
            text: Texte à découper
            font: Police utilisée
            max_width: Largeur maximale en pixels
            
        Returns:
            Liste de lignes
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines or [text]
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convertit couleur hexadécimale en RGB
        
        Args:
            hex_color: Couleur au format #RRGGBB
            
        Returns:
            Tuple (R, G, B)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _create_gradient_background(self, color1: str, color2: str) -> Image.Image:
        """Crée un fond avec dégradé vertical
        
        Args:
            color1: Couleur de départ (hex)
            color2: Couleur de fin (hex)
            
        Returns:
            Image avec dégradé
        """
        img = Image.new('RGB', self.size)
        draw = ImageDraw.Draw(img)
        
        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)
        
        for y in range(self.size[1]):
            ratio = y / self.size[1]
            r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
            g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
            b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)
            draw.line([(0, y), (self.size[0], y)], fill=(r, g, b))
        
        return img
    
    def _calculate_font_size(self, text_length: int) -> int:
        """Calcule la taille de police optimale selon la longueur du texte
        
        Args:
            text_length: Nombre de caractères
            
        Returns:
            Taille de police en pixels
        """
        if text_length < 60:
            return self.FONT_SIZES['quote']['small']
        elif text_length < 120:
            return self.FONT_SIZES['quote']['medium']
        elif text_length < 180:
            return self.FONT_SIZES['quote']['large']
        else:
            return self.FONT_SIZES['quote']['xlarge']
    
    def _render_minimal_style(
        self,
        img: Image.Image,
        quote_lines: List[str],
        author: str,
        quote_font: ImageFont.FreeTypeFont,
        author_font: ImageFont.FreeTypeFont,
        text_color: Tuple[int, int, int],
        line_spacing: int
    ):
        """Rendu style minimal - épuré et centré"""
        draw = ImageDraw.Draw(img)
        
        # Calculer positions
        total_height = len(quote_lines) * line_spacing + 80
        start_y = (self.size[1] - total_height) // 2
        
        # Dessiner les lignes de citation
        y_pos = start_y
        for line in quote_lines:
            bbox = quote_font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            x_pos = (self.size[0] - line_width) // 2
            draw.text((x_pos, y_pos), line, font=quote_font, fill=text_color)
            y_pos += line_spacing
        
        # Dessiner l'auteur
        author_text = f"— {author}"
        bbox = author_font.getbbox(author_text)
        author_width = bbox[2] - bbox[0]
        author_x = (self.size[0] - author_width) // 2
        draw.text((author_x, y_pos + 40), author_text, font=author_font, fill=text_color)
    
    def _render_moderne_style(
        self,
        img: Image.Image,
        quote_lines: List[str],
        author: str,
        quote_font: ImageFont.FreeTypeFont,
        author_font: ImageFont.FreeTypeFont,
        text_color: Tuple[int, int, int],
        accent_color: Tuple[int, int, int],
        line_spacing: int,
        padding: int
    ):
        """Rendu style moderne - avec guillemets et ligne décorative"""
        draw = ImageDraw.Draw(img)
        
        # Guillemets décoratifs
        decorative_font = self._get_font(self.FONT_SIZES['decorative'], 'bold', 
                                        quote_font.getname()[0] if hasattr(quote_font, 'getname') else 'DejaVu Sans')
        
        # Calculer positions
        total_height = len(quote_lines) * line_spacing + 80
        start_y = (self.size[1] - total_height) // 2
        
        # Guillemet ouvrant
        draw.text((padding - 10, start_y - 45), '"', font=decorative_font, fill=accent_color)
        
        # Dessiner les lignes
        y_pos = start_y
        for line in quote_lines:
            bbox = quote_font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            x_pos = (self.size[0] - line_width) // 2
            draw.text((x_pos, y_pos), line, font=quote_font, fill=text_color)
            y_pos += line_spacing
        
        # Guillemet fermant
        draw.text((self.size[0] - padding - 25, y_pos - 50), '"', font=decorative_font, fill=accent_color)
        
        # Auteur
        author_text = f"— {author}"
        bbox = author_font.getbbox(author_text)
        author_width = bbox[2] - bbox[0]
        author_x = (self.size[0] - author_width) // 2
        draw.text((author_x, y_pos + 40), author_text, font=author_font, fill=text_color)
        
        # Ligne décorative
        line_y = y_pos + 85
        line_start = (self.size[0] // 2) - 70
        line_end = (self.size[0] // 2) + 70
        draw.rectangle([(line_start, line_y), (line_end, line_y + 3)], fill=accent_color)
    
    def _render_elegant_style(
        self,
        img: Image.Image,
        quote_lines: List[str],
        author: str,
        quote_font: ImageFont.FreeTypeFont,
        author_font: ImageFont.FreeTypeFont,
        text_color: Tuple[int, int, int],
        accent_color: Tuple[int, int, int],
        line_spacing: int,
        padding: int
    ):
        """Rendu style élégant - avec bordure et ornements"""
        draw = ImageDraw.Draw(img)
        
        # Bordure élégante
        margin = 45
        draw.rectangle(
            [(margin, margin), (self.size[0] - margin, self.size[1] - margin)],
            outline=accent_color,
            width=2
        )
        
        # Guillemets élégants
        decorative_font = self._get_font(55, 'bold', 
                                        quote_font.getname()[0] if hasattr(quote_font, 'getname') else 'DejaVu Sans')
        
        # Calculer positions
        total_height = len(quote_lines) * line_spacing + 80
        start_y = (self.size[1] - total_height) // 2
        
        # Guillemets
        draw.text((padding + 5, start_y - 35), '"', font=decorative_font, fill=accent_color)
        
        # Lignes de citation
        y_pos = start_y
        for line in quote_lines:
            bbox = quote_font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            x_pos = (self.size[0] - line_width) // 2
            draw.text((x_pos, y_pos), line, font=quote_font, fill=text_color)
            y_pos += line_spacing
        
        draw.text((self.size[0] - padding - 35, y_pos - 45), '"', font=decorative_font, fill=accent_color)
        
        # Auteur avec ornements
        author_text = f"— {author} —"
        bbox = author_font.getbbox(author_text)
        author_width = bbox[2] - bbox[0]
        author_x = (self.size[0] - author_width) // 2
        draw.text((author_x, y_pos + 40), author_text, font=author_font, fill=text_color)
        
        # Losanges décoratifs
        diamond_y = y_pos + 85
        for offset in [-90, 0, 90]:
            cx = (self.size[0] // 2) + offset
            diamond_points = [
                (cx, diamond_y - 4),
                (cx + 4, diamond_y),
                (cx, diamond_y + 4),
                (cx - 4, diamond_y)
            ]
            draw.polygon(diamond_points, fill=accent_color)
    
    def create_image(
        self,
        quote_text: str,
        author: str,
        colors: List[str],
        style: str = 'moderne',
        font_family: str = 'DejaVu Sans'
    ) -> Image.Image:
        """Crée une image de citation professionnelle
        
        Args:
            quote_text: Texte de la citation
            author: Nom de l'auteur
            colors: Liste [background, text, accent] en hex
            style: 'minimal', 'moderne' ou 'elegant'
            font_family: Famille de police à utiliser
            
        Returns:
            Image PIL générée
        """
        logger.info(f"Génération: style={style}, font={font_family}, len={len(quote_text)}")
        
        # Créer le fond
        if style in ['moderne', 'elegant', 'élégant'] and len(colors) >= 2:
            img = self._create_gradient_background(colors[0], colors[0])
        else:
            img = Image.new('RGB', self.size, self._hex_to_rgb(colors[0]))
        
        # Couleurs
        text_color = self._hex_to_rgb(colors[1] if len(colors) > 1 else '#FFFFFF')
        accent_color = self._hex_to_rgb(colors[2] if len(colors) > 2 else colors[1])
        
        # Configuration selon style
        padding = self.PADDING_BY_STYLE.get(style, 100)
        available_width = self.size[0] - (2 * padding)
        
        # Polices
        font_size = self._calculate_font_size(len(quote_text))
        quote_font = self._get_font(font_size, 'bold', font_family)
        author_font = self._get_font(self.FONT_SIZES['author'], 'regular', font_family)
        
        # Découper le texte
        quote_lines = self._wrap_text(quote_text, quote_font, available_width)
        line_spacing = int(font_size * 1.5)
        
        # Rendu selon le style
        if style == 'minimal':
            self._render_minimal_style(img, quote_lines, author, quote_font, 
                                      author_font, text_color, line_spacing)
        elif style == 'moderne':
            self._render_moderne_style(img, quote_lines, author, quote_font,
                                       author_font, text_color, accent_color,
                                       line_spacing, padding)
        elif style in ['elegant', 'élégant']:
            self._render_elegant_style(img, quote_lines, author, quote_font,
                                       author_font, text_color, accent_color,
                                       line_spacing, padding)
        
        logger.info("Image générée avec succès")
        return img
    
    def save_image(
        self,
        img: Image.Image,
        output_path: str,
        format: str = 'PNG',
        quality: int = 95
    ) -> bool:
        """Sauvegarde l'image avec optimisation
        
        Args:
            img: Image à sauvegarder
            output_path: Chemin de destination
            format: Format (PNG, JPEG, etc.)
            quality: Qualité (1-100)
            
        Returns:
            True si succès, False sinon
        """
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            if format.upper() == 'JPEG':
                img = img.convert('RGB')
                img.save(output_path, format=format, quality=quality, optimize=True)
            else:
                img.save(output_path, format=format, optimize=True)
            
            logger.info(f"Image sauvegardée: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Erreur sauvegarde: {e}")
            return False
    
    def get_available_fonts(self) -> List[str]:
        """Retourne la liste des polices disponibles
        
        Returns:
            Liste des noms de familles de polices
        """
        return list(self.available_fonts.keys()) or ['DejaVu Sans']