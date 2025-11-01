# engine/rules_manager.py
# Gestor de reglas personalizadas para el sistema experto

import json
import os
from datetime import datetime

class RulesManager:
    """
    Clase para gestionar las reglas personalizadas del sistema.
    Permite agregar, editar, eliminar y cargar reglas desde JSON.
    """
    
    def __init__(self, rules_file='knowledge/rules_data.json'):
        """
        Inicializa el gestor de reglas.
        
        Args:
            rules_file: Ruta al archivo JSON de reglas
        """
        self.rules_file = rules_file
        self.rules = []
        self.load_rules()
    
    def load_rules(self):
        """Carga las reglas desde el archivo JSON"""
        try:
            ruta = os.path.join(os.path.dirname(__file__), '..', self.rules_file)
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.rules = data.get('reglas_personalizadas', [])
            return True
        except FileNotFoundError:
            print(f"Archivo {self.rules_file} no encontrado. Creando uno nuevo...")
            self.rules = []
            self.save_rules()
            return False
        except Exception as e:
            print(f"Error al cargar reglas: {e}")
            return False
    
    def save_rules(self):
        """Guarda las reglas en el archivo JSON"""
        try:
            ruta = os.path.join(os.path.dirname(__file__), '..', self.rules_file)
            data = {'reglas_personalizadas': self.rules}
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar reglas: {e}")
            return False
    
    def get_all_rules(self):
        """Retorna todas las reglas"""
        return self.rules
    
    def get_active_rules(self):
        """Retorna solo las reglas activas"""
        return [regla for regla in self.rules if regla.get('activa', True)]
    
    def get_rule_by_id(self, id_regla):
        """
        Busca una regla por su ID.
        
        Args:
            id_regla: ID de la regla a buscar
            
        Returns:
            La regla si se encuentra, None en caso contrario
        """
        for regla in self.rules:
            if regla.get('id_regla') == id_regla:
                return regla
        return None
    
    def add_rule(self, nombre, palabras_clave, tipo, prioridad, asignado_a, activa=True):
        """
        Agrega una nueva regla al sistema.
        
        Args:
            nombre: Nombre descriptivo de la regla
            palabras_clave: Lista de palabras clave que activan la regla
            tipo: Tipo de ticket (HARDWARE, SOFTWARE, REDES, SEGURIDAD)
            prioridad: Prioridad del ticket (Alta, Media, Baja)
            asignado_a: Equipo o persona asignada
            activa: Estado de la regla (True/False)
            
        Returns:
            True si se agregó exitosamente, False en caso contrario
        """
        try:
            # Generar ID único
            if self.rules:
                # Obtener el número más alto de las reglas existentes
                ids_existentes = [int(r['id_regla'][1:]) for r in self.rules if r['id_regla'].startswith('R')]
                nuevo_num = max(ids_existentes) + 1 if ids_existentes else 1
            else:
                nuevo_num = 1
            
            nuevo_id = f"R{nuevo_num:02d}"
            
            # Crear la nueva regla
            nueva_regla = {
                'id_regla': nuevo_id,
                'nombre': nombre,
                'palabras_clave': palabras_clave,
                'tipo': tipo,
                'prioridad': prioridad,
                'asignado_a': asignado_a,
                'activa': activa,
                'fecha_creacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Agregar a la lista
            self.rules.append(nueva_regla)
            
            # Guardar en archivo
            return self.save_rules()
        
        except Exception as e:
            print(f"Error al agregar regla: {e}")
            return False
    
    def update_rule(self, id_regla, nombre=None, palabras_clave=None, tipo=None, 
                   prioridad=None, asignado_a=None, activa=None):
        """
        Actualiza una regla existente.
        
        Args:
            id_regla: ID de la regla a actualizar
            Los demás parámetros son opcionales y actualizan solo si se proporcionan
            
        Returns:
            True si se actualizó exitosamente, False en caso contrario
        """
        try:
            regla = self.get_rule_by_id(id_regla)
            if not regla:
                print(f"Regla {id_regla} no encontrada")
                return False
            
            # Actualizar campos proporcionados
            if nombre is not None:
                regla['nombre'] = nombre
            if palabras_clave is not None:
                regla['palabras_clave'] = palabras_clave
            if tipo is not None:
                regla['tipo'] = tipo
            if prioridad is not None:
                regla['prioridad'] = prioridad
            if asignado_a is not None:
                regla['asignado_a'] = asignado_a
            if activa is not None:
                regla['activa'] = activa
            
            regla['fecha_modificacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return self.save_rules()
        
        except Exception as e:
            print(f"Error al actualizar regla: {e}")
            return False
    
    def delete_rule(self, id_regla):
        """
        Elimina una regla del sistema.
        
        Args:
            id_regla: ID de la regla a eliminar
            
        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        try:
            regla = self.get_rule_by_id(id_regla)
            if not regla:
                print(f"Regla {id_regla} no encontrada")
                return False
            
            self.rules.remove(regla)
            return self.save_rules()
        
        except Exception as e:
            print(f"Error al eliminar regla: {e}")
            return False
    
    def toggle_rule_status(self, id_regla):
        """
        Cambia el estado activo/inactivo de una regla.
        
        Args:
            id_regla: ID de la regla
            
        Returns:
            True si se cambió exitosamente, False en caso contrario
        """
        try:
            regla = self.get_rule_by_id(id_regla)
            if not regla:
                return False
            
            regla['activa'] = not regla.get('activa', True)
            return self.save_rules()
        
        except Exception as e:
            print(f"Error al cambiar estado de regla: {e}")
            return False
    
    def get_statistics(self):
        """
        Retorna estadísticas sobre las reglas.
        
        Returns:
            Diccionario con estadísticas
        """
        total = len(self.rules)
        activas = len([r for r in self.rules if r.get('activa', True)])
        inactivas = total - activas
        
        # Contar por tipo
        tipos = {}
        for regla in self.rules:
            tipo = regla.get('tipo', 'Desconocido')
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        # Contar por prioridad
        prioridades = {}
        for regla in self.rules:
            prioridad = regla.get('prioridad', 'Desconocida')
            prioridades[prioridad] = prioridades.get(prioridad, 0) + 1
        
        return {
            'total': total,
            'activas': activas,
            'inactivas': inactivas,
            'por_tipo': tipos,
            'por_prioridad': prioridades
        }
