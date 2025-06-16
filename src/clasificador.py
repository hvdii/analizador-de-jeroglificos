class Clasificador:
    """
    Clase responsable de clasificar jeroglíficos basándose en sus características.
    """
    
    def clasificar(self, caracteristicas):
        """
        Clasifica los jeroglíficos según sus características.
        
        Args:
            caracteristicas (list): Lista de diccionarios con características de cada jeroglífico.
            
        Returns:
            list: Lista de letras que representan los jeroglíficos clasificados.
        """
        letras = []
        
        for caracteristica in caracteristicas:
            letra = self._clasificar_jeroglifico(caracteristica)
            if letra:
                letras.append(letra)
        
        # Ordenar las letras alfabéticamente antes de devolverlas
        letras.sort()
        return letras
    
    def _clasificar_jeroglifico(self, caracteristica):
        """
        Clasifica un jeroglífico individual según sus características.
        
        Args:
            caracteristica (dict): Características del jeroglífico.
            
        Returns:
            str: Letra que representa el jeroglífico clasificado.
        """
        num_agujeros = caracteristica['num_agujeros']
        
        # Reglas de clasificación basadas únicamente en el número de agujeros
        if num_agujeros == 0:
            return 'W'  # Was
        elif num_agujeros == 1:
            return 'A'  # Ankh
        elif num_agujeros == 2:
            return 'K'  # Akhet
        elif num_agujeros == 3:
            return 'J'  # Wedjat
        elif num_agujeros == 4:
            return 'S'  # Scarab
        elif num_agujeros == 5:
            return 'D'  # Djed
        
        return None  # No clasificado (no debería ocurrir según especificaciones)