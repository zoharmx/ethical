# Ethica.AI - Guía de Despliegue

## Resumen del Proyecto

Se ha creado una **aplicación web moderna de primer nivel** para el framework Ethica.AI con las siguientes características:

### Tecnologías Implementadas
- **Frontend**: Next.js 14 + React 18 + TypeScript
- **Diseño**: Tailwind CSS + Shadcn/ui
- **Animaciones**: Framer Motion
- **Backend API**: FastAPI (Python)
- **Framework Core**: Ethica Framework (Multi-provider AI)

### Características Principales
1. **Landing Page Moderna**: Diseño tipo SaaS profesional con animaciones suaves
2. **Dashboard Interactivo**: Análisis en tiempo real con visualización de progreso
3. **10 Módulos de Análisis**: Pipeline completo visualizado paso a paso
4. **Multi-Provider AI**: Gemini, Mistral y DeepSeek integrados
5. **Métricas Cuantitativas**: Scores, gráficos y visualizaciones profesionales
6. **Responsive Design**: Optimizado para todos los dispositivos
7. **Efectos Visuales**: Glass morphism, gradientes, transiciones suaves

---

## Estructura del Proyecto

```
ethica-framework/
├── web-app/                    # Aplicación web Next.js
│   ├── src/
│   │   ├── app/               # Páginas y rutas
│   │   │   ├── page.tsx       # Landing page
│   │   │   ├── dashboard/     # Dashboard de análisis
│   │   │   └── api/           # API routes
│   │   ├── components/ui/     # Componentes reutilizables
│   │   ├── lib/              # Utilidades
│   │   └── styles/           # Estilos globales
│   ├── api/                  # Backend FastAPI
│   │   ├── main.py          # API server
│   │   └── requirements.txt
│   └── package.json
├── ethica-framework/         # Framework Python original
│   └── src/                 # Código del framework
└── sefirot/                 # Framework Kabbalah (legacy)
```

---

## Despliegue en Vercel

### Opción 1: Despliegue Automático desde GitHub

1. **Accede a Vercel**
   - Ve a https://vercel.com
   - Inicia sesión con tu cuenta de GitHub

2. **Importa el Repositorio**
   - Click en "Add New Project"
   - Selecciona el repositorio: `zoharmx/ethical`
   - Framework Preset: **Next.js**
   - Root Directory: `web-app`

3. **Configura Variables de Entorno**
   En el dashboard de Vercel, agrega estas variables:
   ```
   NEXT_PUBLIC_API_URL=https://tu-api-backend.vercel.app
   GEMINI_API_KEY=AIzaSyBxSQ6GGcujsIqNznxNQjJt-kKG4Wcuogo
   MISTRAL_API_KEY=cqrcNINDiUWdfsRkUk9BBCq52XzphD1V
   DEEPSEEK_API_KEY=sk-181034ba355c4292ad7f149d569ce4e7
   ```

4. **Deploy**
   - Click en "Deploy"
   - Espera 2-3 minutos
   - Tu aplicación estará en: `https://ethical-xxxx.vercel.app`

### Opción 2: Despliegue desde CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Navegar al directorio web-app
cd web-app

# Deploy
vercel

# Para producción
vercel --prod
```

---

## Despliegue del Backend (FastAPI)

### Opción A: Vercel (Serverless)

1. Crea `web-app/api/vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/main.py"
    }
  ]
}
```

2. Deploy:
```bash
cd web-app
vercel
```

### Opción B: Railway

1. Ve a https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Selecciona el repositorio
4. Root: `web-app/api`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Opción C: Render

1. Ve a https://render.com
2. "New Web Service"
3. Conecta el repositorio
4. Root: `web-app/api`
5. Build: `pip install -r requirements.txt`
6. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## Configuración Post-Despliegue

### 1. Actualizar URL del API

Una vez desplegado el backend, actualiza la variable de entorno en Vercel:
```
NEXT_PUBLIC_API_URL=https://tu-backend-url.com
```

### 2. Configurar Dominio Personalizado (Opcional)

En Vercel Dashboard:
- Settings → Domains
- Agrega tu dominio: `ethica.ai` o `app.ethica.ai`
- Configura DNS según instrucciones

### 3. Verificar Funcionamiento

Accede a tu aplicación:
- Landing: `https://tu-app.vercel.app`
- Dashboard: `https://tu-app.vercel.app/dashboard`
- API Health: `https://tu-api.vercel.app/health`

---

## Testing Local

### Frontend

```bash
cd web-app
npm install
npm run dev
```

Accede a: http://localhost:3000

### Backend

```bash
cd web-app/api
pip install -r requirements.txt
python main.py
```

Accede a: http://localhost:8000

API Docs: http://localhost:8000/docs

---

## Características Implementadas

### Landing Page (/)
- Hero section con animaciones
- Estadísticas dinámicas
- Features showcase
- Casos de uso reales
- CTA sections
- Footer profesional

### Dashboard (/dashboard)
- Selector de escenarios predefinidos
- Editor de escenario personalizado
- Análisis en tiempo real
- Visualización de 10 módulos
- Progreso animado
- Resultados detallados con métricas
- Scores por capa (Strategic, Operational, Tactical, Execution)
- Decisión final (APPROVED/CONDITIONAL/REJECTED)
- Acciones recomendadas y condiciones

### API Endpoints

**POST /api/analyze**
- Input: Escenario con action, context, stakeholders
- Output: Análisis completo con decisión y métricas
- Fallback: Mock data si framework no disponible

**GET /health**
- Status del sistema

**GET /**
- Info de la API

---

## Estructura de Respuesta de la API

```json
{
  "scenario_id": "ETH-xxxxx",
  "timestamp": "2025-01-06T...",
  "strategic": {
    "impact_score": 0.78,
    "confidence": 0.95
  },
  "operational": {
    "harmony_score": 0.72
  },
  "tactical": {
    "sustainability": 0.75
  },
  "execution": {
    "readiness": 0.74,
    "approved": true
  },
  "decision": {
    "approved": true,
    "approval_type": "CONDITIONAL",
    "confidence": 0.98,
    "reasoning": "...",
    "actions": [...],
    "conditions": [...]
  }
}
```

---

## Mantenimiento y Actualizaciones

### Actualizar la Aplicación

```bash
# Hacer cambios en el código
git add .
git commit -m "Update: descripción de cambios"
git push origin main

# Vercel auto-despliega desde GitHub
```

### Monitoreo

- **Vercel Analytics**: Dashboard automático de métricas
- **Logs**: Vercel Dashboard → Project → Logs
- **Errores**: Vercel Dashboard → Project → Deployments → View Errors

---

## Costos Estimados

### Vercel (Frontend)
- **Hobby Plan**: $0/mes (suficiente para desarrollo)
- **Pro Plan**: $20/mes (recomendado para producción)

### Backend
- **Vercel Serverless**: Incluido en plan
- **Railway**: $5-20/mes según uso
- **Render**: $7-25/mes

### Total Mensual Estimado
- Desarrollo: **$0**
- Producción básica: **$20-30/mes**
- Producción escalable: **$50-100/mes**

---

## Soporte y Documentación

- **Código fuente**: https://github.com/zoharmx/ethical
- **Framework docs**: Ver `ethica-framework/README.md`
- **Next.js docs**: https://nextjs.org/docs
- **Vercel docs**: https://vercel.com/docs

---

## Próximos Pasos Recomendados

1. **Analytics**: Integrar Google Analytics o Vercel Analytics
2. **Autenticación**: Agregar NextAuth.js para login
3. **Base de Datos**: Integrar Postgres/MongoDB para guardar análisis
4. **Exportación**: Agregar exportación a PDF de reportes
5. **Email**: Integrar Resend/SendGrid para notificaciones
6. **Multilenguaje**: Agregar i18n para español/inglés
7. **SEO**: Optimizar meta tags y sitemap

---

## Contacto y Soporte

Para soporte técnico o consultas:
- **GitHub Issues**: https://github.com/zoharmx/ethical/issues
- **Email**: support@ethica.ai

---

**Proyecto completado y desplegado por Claude Code**
Generated with [Claude Code](https://claude.com/claude-code)
