# engine/areas_manager.py
# Gestor de áreas de la empresa

import json
import os
from datetime import datetime

class AreasManager:
    """
    Clase para gestionar las áreas de la empresa.
    Permite agregar, editar, eliminar y cargar áreas desde JSON.
    """
    
    def __init__(self, areas_file='knowledge/areas_empresa.json'):
        """
        Inicializa el gestor de áreas.
        
        Args:
            areas_file: Ruta al archivo JSON de áreas
        """
        self.areas_file = areas_file
        self.areas = []
        self.load_areas()
    
    def load_areas(self):
        """Carga las áreas desde el archivo JSON"""
        try:
            ruta = os.path.join(os.path.dirname(__file__), '..', self.areas_file)
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.areas = data.get('areas', [])
            return True
        except FileNotFoundError:
            print(f"Archivo {self.areas_file} no encontrado. Creando uno nuevo...")
            self.areas = []
            self.save_areas()
            return False
        except Exception as e:
            print(f"Error al cargar áreas: {e}")
            return False
    
    def save_areas(self):
        """Guarda las áreas en el archivo JSON"""
        try:
            ruta = os.path.join(os.path.dirname(__file__), '..', self.areas_file)
            data = {'areas': self.areas}
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar áreas: {e}")
            return False
    
    def get_all_areas(self):
        """Retorna todas las áreas"""
        return self.areas
    
    def get_areas_names(self):
        """Retorna solo los nombres de las áreas"""
        return [area['nombre'] for area in self.areas]
    
    def get_area_by_id(self, id_area):
        """
        Busca un área por su ID.
        
        Args:
            id_area: ID del área a buscar
            
        Returns:
            El área si se encuentra, None en caso contrario
        """
        for area in self.areas:
            if area.get('id_area') == id_area:
                return area
        return None
    
    def get_area_by_name(self, nombre):
        """
        Busca un área por su nombre.
        
        Args:
            nombre: Nombre del área a buscar
            
        Returns:
            El área si se encuentra, None en caso contrario
        """
        for area in self.areas:
            if area.get('nombre').lower() == nombre.lower():
                return area
        return None
    
    def add_area(self, nombre, descripcion=""):
        """
        Agrega una nueva área al sistema.
        
        Args:
            nombre: Nombre del área
            descripcion: Descripción opcional del área
            
        Returns:
            True si se agregó exitosamente, False en caso contrario
        """
        try:
            # Verificar si ya existe
            if self.get_area_by_name(nombre):
                print(f"El área '{nombre}' ya existe")
                return False
            
            # Generar ID único
            if self.areas:
                # Obtener el número más alto de las áreas existentes
                ids_existentes = [int(a['id_area'][1:]) for a in self.areas if a['id_area'].startswith('A')]
                nuevo_num = max(ids_existentes) + 1 if ids_existentes else 1
            else:
                nuevo_num = 1
            
            nuevo_id = f"A{nuevo_num:03d}"
            
            # Crear el nuevo área
            nueva_area = {
                'id_area': nuevo_id,
                'nombre': nombre,
                'descripcion': descripcion,
                'fecha_creacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Agregar a la lista
            self.areas.append(nueva_area)
            
            # Guardar en archivo
            return self.save_areas()
        
        except Exception as e:
            print(f"Error al agregar área: {e}")
            return False
    
    def update_area(self, id_area, nombre=None, descripcion=None):
        """
        Actualiza un área existente.
        
        Args:
            id_area: ID del área a actualizar
            nombre: Nuevo nombre (opcional)
            descripcion: Nueva descripción (opcional)
            
        Returns:
            True si se actualizó exitosamente, False en caso contrario
        """
        try:
            area = self.get_area_by_id(id_area)
            if not area:
                print(f"Área {id_area} no encontrada")
                return False
            
            # Actualizar campos proporcionados
            if nombre is not None:
                # Verificar que el nuevo nombre no exista ya
                area_existente = self.get_area_by_name(nombre)
                if area_existente and area_existente['id_area'] != id_area:
                    print(f"Ya existe un área con el nombre '{nombre}'")
                    return False
                area['nombre'] = nombre
            
            if descripcion is not None:
                area['descripcion'] = descripcion
            
            area['fecha_modificacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return self.save_areas()
        
        except Exception as e:
            print(f"Error al actualizar área: {e}")
            return False
    
    def delete_area(self, id_area):
        """
        Elimina un área del sistema.
        
        Args:
            id_area: ID del área a eliminar
            
        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        try:
            area = self.get_area_by_id(id_area)
            if not area:
                print(f"Área {id_area} no encontrada")
                return False
            
            self.areas.remove(area)
            return self.save_areas()
        
        except Exception as e:
            print(f"Error al eliminar área: {e}")
            return False
    
    def get_statistics(self):
        """
        Retorna estadísticas sobre las áreas.
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            'total': len(self.areas),
            'nombres': self.get_areas_names()
        }
