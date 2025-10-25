# 🤝 Guía de Contribución - F1 Q&A System

¡Gracias por tu interés en contribuir al proyecto F1 Q&A System! Esta guía te ayudará a hacer contribuciones efectivas.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Guías de Estilo](#guías-de-estilo)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)
- [Pull Requests](#pull-requests)

---

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta simple:

- **Sé respetuoso**: Trata a todos con respeto
- **Sé constructivo**: Proporciona feedback constructivo
- **Sé colaborativo**: Trabaja en equipo
- **Sé inclusivo**: Todos son bienvenidos

---

## 🎯 ¿Cómo puedo contribuir?

Hay muchas formas de contribuir:

### 1. Reportar Bugs 🐛

Si encuentras un bug:
- Busca en [Issues](../../issues) si ya fue reportado
- Si no existe, abre un nuevo issue usando la plantilla de bug
- Incluye pasos para reproducir, comportamiento esperado y actual
- Añade capturas de pantalla si es relevante

### 2. Sugerir Features ✨

Si tienes una idea:
- Revisa el [Roadmap](README.md#roadmap-futuro)
- Abre un issue con la etiqueta "enhancement"
- Describe claramente el problema que resuelve
- Propón una solución o implementación

### 3. Mejorar Documentación 📝

- Corregir typos
- Clarificar secciones confusas
- Añadir ejemplos
- Traducir a otros idiomas

### 4. Contribuir Código 💻

- Implementar features del roadmap
- Arreglar bugs
- Optimizar rendimiento
- Añadir tests

---

## 🔄 Proceso de Desarrollo

### Setup Inicial

1. **Fork el repositorio**
   ```bash
   # En GitHub, haz click en "Fork"
   ```

2. **Clona tu fork**
   ```bash
   git clone https://github.com/TU_USUARIO/f1-qa-semantic-network.git
   cd f1-qa-semantic-network
   ```

3. **Configura upstream**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/f1-qa-semantic-network.git
   ```

4. **Instala dependencias**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Volver a raíz
   cd ..
   ```

### Flujo de Trabajo

1. **Crea una rama**
   ```bash
   git checkout -b feature/nombre-descriptivo
   # o
   git checkout -b fix/descripcion-del-bug
   ```

2. **Haz tus cambios**
   - Escribe código limpio y comentado
   - Sigue las guías de estilo
   - Añade tests si aplica

3. **Prueba tus cambios**
   ```bash
   # Backend
   cd backend
   pytest tests/ -v
   
   # Sistema completo
   docker-compose up --build
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "tipo: descripción clara del cambio"
   ```

5. **Mantén tu rama actualizada**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

6. **Push a tu fork**
   ```bash
   git push origin feature/nombre-descriptivo
   ```

7. **Abre un Pull Request**
   - Ve a GitHub y abre un PR
   - Llena la plantilla de PR
   - Enlaza issues relacionados

---

## 📐 Guías de Estilo

### Python (Backend)

**Estándar**: PEP 8

```python
# ✅ Bueno
def calculate_confidence(nodes: List[Node], parsed_query: ParsedQuery) -> float:
    """
    Calcula el nivel de confianza de una respuesta.
    
    Args:
        nodes: Lista de nodos encontrados
        parsed_query: Consulta parseada
        
    Returns:
        float: Confianza entre 0.0 y 1.0
    """
    if not nodes:
        return 0.0
    
    score = 0.5
    if len(nodes) == 1:
        score += 0.3
    
    return min(1.0, score)


# ❌ Malo
def calc(n,p):
    if not n: return 0.0
    s=0.5
    if len(n)==1: s+=0.3
    return min(1.0,s)
```

**Reglas**:
- Usa type hints
- Docstrings para funciones públicas
- Nombres descriptivos en inglés
- Máximo 88 caracteres por línea
- 2 líneas en blanco entre clases/funciones

### JavaScript (Frontend)

**Estándar**: Airbnb Style Guide adaptado

```javascript
// ✅ Bueno
/**
 * Renderiza un mensaje en el chat
 * @param {Object} message - Objeto mensaje
 * @param {boolean} isBot - Si es mensaje del bot
 */
function renderMessage(message, isBot = false) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
    
    messageEl.innerHTML = `
        <div class="message-content">
            <p>${escapeHtml(message.text)}</p>
        </div>
    `;
    
    return messageEl;
}

// ❌ Malo
function render(m,b){
    var el=document.createElement('div');
    el.className=b?'bot-message':'user-message';
    el.innerHTML='<div>'+m.text+'</div>';
    return el;
}
```

**Reglas**:
- ES6+ sintaxis
- const/let en vez de var
- Arrow functions cuando sea apropiado
- JSDoc para funciones públicas
- Nombres descriptivos en inglés
- Punto y coma al final de statements
- 2 espacios de indentación

### CSS

**Metodología**: BEM adaptado

```css
/* ✅ Bueno */
.message {
    padding: var(--spacing-md);
    border-radius: 8px;
}

.message__content {
    display: flex;
    align-items: center;
}

.message__avatar {
    width: 40px;
    height: 40px;
}

.message--bot {
    background-color: var(--gray-100);
}

.message--user {
    background-color: var(--primary-color);
    color: white;
}

/* ❌ Malo */
.msg { padding:10px; border-radius:8px; }
.msgContent { display:flex; align-items:center; }
#avatar { width:40px; height:40px; }
.botMsg { background-color:#F3F4F6; }
```

**Reglas**:
- BEM para nomenclatura
- Variables CSS para valores repetidos
- Mobile-first media queries
- Evitar !important
- Agrupar propiedades relacionadas

### Mensajes de Commit

**Formato**: Conventional Commits

```
tipo(scope): descripción corta

Descripción detallada opcional.

Closes #123
```

**Tipos**:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato, punto y coma, etc
- `refactor`: Refactorización de código
- `perf`: Mejora de rendimiento
- `test`: Añadir o corregir tests
- `chore`: Tareas de mantenimiento

**Ejemplos**:
```bash
feat(backend): añadir endpoint para comparar pilotos
fix(frontend): corregir scroll en mobile
docs(readme): actualizar instrucciones de instalación
style(backend): formatear con black
refactor(nlp): simplificar extracción de entidades
perf(network): optimizar búsqueda de nodos
test(api): añadir tests para endpoint /ask
chore(deps): actualizar FastAPI a 0.104.1
```

---

## 🐛 Reportar Bugs

### Antes de Reportar

1. Busca en [Issues existentes](../../issues)
2. Actualiza a la última versión
3. Revisa la [documentación](README.md)

### Template de Bug Report

```markdown
**Descripción del Bug**
Una descripción clara del problema.

**Pasos para Reproducir**
1. Ir a '...'
2. Hacer click en '...'
3. Scroll down to '...'
4. Ver error

**Comportamiento Esperado**
Qué esperabas que sucediera.

**Comportamiento Actual**
Qué sucedió realmente.

**Screenshots**
Si aplica, añade capturas de pantalla.

**Entorno**
- OS: [ej. macOS 14.0]
- Browser: [ej. Chrome 120]
- Versión Python: [ej. 3.11]
- Docker: [ej. 24.0]

**Logs**
```
Pega logs relevantes aquí
```

**Contexto Adicional**
Cualquier otra información relevante.
```

---

## 💡 Sugerir Mejoras

### Template de Feature Request

```markdown
**¿El feature resuelve un problema?**
Una descripción clara del problema. Ej: "Siempre me frustro cuando [...]"

**Solución Propuesta**
Una descripción clara de lo que quieres que suceda.

**Alternativas Consideradas**
Otras soluciones o features que consideraste.

**Contexto Adicional**
Screenshots, mockups, ejemplos, etc.

**¿Estarías dispuesto a implementarlo?**
Sí/No/Con ayuda
```

---

## 🔀 Pull Requests

### Checklist de PR

Antes de abrir un PR, verifica:

- [ ] El código funciona localmente
- [ ] Los tests pasan (`pytest tests/`)
- [ ] El código sigue las guías de estilo
- [ ] La documentación está actualizada
- [ ] Los commits siguen Conventional Commits
- [ ] No hay conflictos con main
- [ ] El PR describe claramente los cambios
- [ ] Se enlazaron issues relacionados

### Template de PR

```markdown
## Descripción

Breve descripción de los cambios.

## Tipo de Cambio

- [ ] Bug fix (non-breaking change que corrige un issue)
- [ ] Nueva funcionalidad (non-breaking change que añade funcionalidad)
- [ ] Breaking change (fix o feature que causa que funcionalidad existente no funcione)
- [ ] Documentación

## ¿Cómo se ha probado?

Describe las pruebas realizadas.

## Checklist

- [ ] Mi código sigue las guías de estilo
- [ ] He revisado mi propio código
- [ ] He comentado código complejo
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan warnings
- [ ] He añadido tests
- [ ] Los tests pasan localmente

## Screenshots (si aplica)

## Issues Relacionados

Closes #
Related to #
```

### Proceso de Review

1. **Automated Checks**: CI/CD corre automáticamente
2. **Code Review**: Un maintainer revisa tu código
3. **Discusión**: Feedback y discusión si es necesario
4. **Cambios**: Haz cambios solicitados
5. **Aprobación**: Maintainer aprueba el PR
6. **Merge**: Tu código se integra al proyecto

---

## 🧪 Testing

### Backend

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest --cov=src tests/

# Tests específicos
pytest tests/test_nlp.py -v

# Tests con output
pytest tests/ -v -s
```

### Frontend

```bash
# Servidor local
python -m http.server 8080

# Pruebas manuales
# 1. Abrir http://localhost:8080
# 2. Verificar funcionalidad
# 3. Probar en diferentes navegadores
# 4. Probar responsive design
```

### Tests de Integración

```bash
# Levantar sistema completo
docker-compose up --build

# En otra terminal, ejecutar tests
python test_api.py
```

---

## 📦 Áreas que Necesitan Contribuciones

Estas áreas particularmente necesitan ayuda:

### Alta Prioridad 🔴
- [ ] Tests unitarios para servicios
- [ ] Tests de integración para API
- [ ] Mejorar cobertura de tests (objetivo: 80%+)
- [ ] Optimización de consultas NLP
- [ ] Caché de respuestas frecuentes

### Media Prioridad 🟡
- [ ] Dark mode para frontend
- [ ] Exportar conversaciones
- [ ] Visualización del grafo
- [ ] Soporte multiidioma
- [ ] PWA capabilities

### Baja Prioridad 🟢
- [ ] Mejorar diseño móvil
- [ ] Añadir más ejemplos de preguntas
- [ ] Traducir documentación
- [ ] Mejorar mensajes de error
- [ ] Añadir animaciones

---

## 🎓 Recursos para Contribuidores

### Documentación del Proyecto

- [README Principal](README.md)
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)
- [Plan de Desarrollo](DESARROLLO_GITHUB_PLAN.md)

### Tecnologías Utilizadas

**Backend**:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

**Frontend**:
- [MDN Web Docs](https://developer.mozilla.org/)
- [JavaScript.info](https://javascript.info/)
- [CSS Tricks](https://css-tricks.com/)

**DevOps**:
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

## ❓ Preguntas

Si tienes preguntas:

1. Revisa la [documentación](README.md)
2. Busca en [Issues](../../issues)
3. Abre una [Discussion](../../discussions)
4. Contacta a los maintainers

---

## 🙏 Agradecimientos

¡Gracias por contribuir al proyecto! Cada contribución, grande o pequeña, es valiosa.

---

<p align="center">
  <strong>¡Feliz Coding! 🏎️💨</strong>
</p>

